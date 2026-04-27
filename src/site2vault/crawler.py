"""Async crawler with frontier loop, politeness, and scope enforcement."""

import asyncio
import hashlib
import logging
import re
from pathlib import Path
from urllib.parse import urlparse, urljoin

import httpx

import time as _time

from site2vault.antibot import AntibotDetector
from site2vault.canonical import canonicalize
from site2vault.config import RunConfig
from site2vault.convert import convert, save_link_index, save_headings
from site2vault.extract import extract
from site2vault.frontmatter import build_frontmatter
from site2vault.politeness import PolitenessManager
from site2vault.robots import RobotsChecker
from site2vault.slug import assign_filename, url_to_folder_path
from site2vault.progress import emit as progress_emit
from site2vault.state import StateDB

log = logging.getLogger("site2vault.crawler")

# Non-HTTP schemes to skip
SKIP_SCHEMES = {"mailto", "tel", "javascript", "data", "ftp", "file"}

# Content types we process
ALLOWED_CONTENT_TYPES = {"text/html", "application/xhtml+xml", "text/plain"}

# Max retries for transient errors
MAX_RETRIES = 3

# Status codes that are transient (retryable)
TRANSIENT_STATUS = {500, 502, 503, 504, 429}
# Permanent errors (no retry), except 403 and 503 handled specially
PERMANENT_STATUS = {400, 401, 404, 405, 406, 410, 451}


class Crawler:
    """Async web crawler with politeness and scope enforcement."""

    def __init__(self, config: RunConfig, db: StateDB, robots: RobotsChecker):
        self.config = config
        self.db = db
        self.robots = robots
        self.politeness = PolitenessManager(
            rate=config.rate,
            concurrency=config.concurrency,
            jitter=config.jitter,
            min_delay=config.min_delay,
            max_errors=config.max_errors,
        )
        self.antibot = AntibotDetector()
        self.seed_parsed = urlparse(config.seed_url)
        # Derive the seed path prefix for scope enforcement.
        # e.g. seed "/docs/en/intro" -> prefix "/docs/en/"
        # seed "/docs/en/" -> prefix "/docs/en/"
        # seed "/" or "" -> prefix "/"
        seed_path = self.seed_parsed.path or "/"
        if seed_path.endswith("/"):
            self._seed_path_prefix = seed_path
        else:
            self._seed_path_prefix = seed_path.rsplit("/", 1)[0] + "/"
        self._include_re = [re.compile(p) for p in config.include] if config.include else []
        self._exclude_re = [re.compile(p) for p in config.exclude] if config.exclude else []
        self._dry_run_count = 0
        self._stopped_hosts: set[str] = set()

    def has_stopped_hosts(self) -> bool:
        """Check if any host was permanently stopped during the crawl."""
        return len(self._stopped_hosts) > 0

    async def crawl(self) -> None:
        """Run the main crawl loop."""
        seed = canonicalize(self.config.seed_url)

        # Reset any in-progress URLs from a previous crashed run
        reset_count = self.db.reset_in_progress()
        if reset_count:
            log.info("Resumed: reset %d in-progress URLs to pending", reset_count)

        # Seed the frontier
        self.db.add_to_frontier(seed, depth=0)

        # Apply Crawl-delay from robots.txt
        seed_host = urlparse(seed).hostname
        crawl_delay = self.robots.get_crawl_delay(seed_host)
        if crawl_delay:
            self.politeness.per_host.update_min_delay(seed_host, crawl_delay)

        # Create HTTP client
        limits = httpx.Limits(
            max_connections=self.config.concurrency * 2,
            max_keepalive_connections=self.config.concurrency,
        )
        timeout = httpx.Timeout(
            connect=10.0, read=30.0, write=10.0, pool=60.0
        )

        # Overall timeout tracking
        crawl_deadline = None
        if self.config.timeout:
            crawl_deadline = _time.monotonic() + self.config.timeout * 60

        async with httpx.AsyncClient(
            http2=True,
            limits=limits,
            timeout=timeout,
            follow_redirects=True,
            max_redirects=5,
            headers=self._default_headers(),
        ) as client:
            while True:
                if crawl_deadline and _time.monotonic() >= crawl_deadline:
                    log.info("Reached timeout (%.1f min)", self.config.timeout)
                    break

                done_count = self.db.count_done()
                if done_count >= self.config.max_pages:
                    log.info("Reached max pages (%d)", self.config.max_pages)
                    break

                pending = self.db.get_pending_urls(self.config.concurrency)
                if not pending:
                    break

                tasks = [
                    self._process_url(client, item["url"], item["depth"])
                    for item in pending
                ]
                await asyncio.gather(*tasks, return_exceptions=True)

                # Dry-run pause
                if self.config.dry_run:
                    self._dry_run_count += len(pending)
                    if self._dry_run_count % 100 < len(pending):
                        counts = self.db.count_by_status()
                        log.info(
                            "Dry-run: %d discovered, %d done, %d pending",
                            sum(counts.values()),
                            counts.get("done", 0),
                            counts.get("pending", 0),
                        )
                        await asyncio.sleep(5)

        # Log summary
        self._log_summary()

    async def _process_url(
        self, client: httpx.AsyncClient, url: str, depth: int
    ) -> None:
        """Fetch, extract, convert, and enqueue links for a single URL."""
        host = urlparse(url).hostname or ""

        try:
            self.db.mark_in_progress(url)

            # Politeness gate
            if not await self.politeness.wait_for_slot(host):
                self.db.mark_skipped(url, "host_stopped")
                self._stopped_hosts.add(host)
                return

            # Fetch
            progress_emit("fetch_start", url=url, depth=depth)
            _fetch_t0 = _time.monotonic()
            response = await self._fetch_with_retry(client, url, host)
            if response is None:
                return  # Already marked failed

            # Check content type
            content_type = response.headers.get("content-type", "")
            if not self._is_html_content(content_type):
                self.db.mark_skipped(url, f"non_html:{content_type}")
                return

            body = response.text
            final_url = str(response.url)
            _fetch_ms = round((_time.monotonic() - _fetch_t0) * 1000)
            progress_emit("fetch_done", url=url, status=response.status_code,
                          bytes=len(body.encode("utf-8")), duration_ms=_fetch_ms)

            # Handle meta refresh redirects
            meta_target = self._parse_meta_refresh(body, final_url)
            if meta_target:
                log.debug("Meta refresh redirect: %s -> %s", final_url, meta_target)
                self.db.save_redirect(url, canonicalize(meta_target, self.config.seed_url))
                # Enqueue the target as a new URL at same depth
                self._enqueue_links(
                    [{"href": meta_target, "text": "", "anchor_fragment": None}],
                    final_url, depth - 1 if depth > 0 else 0,
                )
                self.db.mark_done(url)
                return

            # Store redirect if different
            if final_url != url:
                canonical_final = canonicalize(final_url, self.config.seed_url)
                if canonical_final != url:
                    self.db.save_redirect(url, canonical_final)

            # Anti-bot check
            headers_dict = dict(response.headers)
            antibot_signal = self.antibot.check_response(
                url, response.status_code, headers_dict, body, final_url
            )
            if antibot_signal:
                self.db.mark_failed(url, f"anti_bot:{antibot_signal}")
                stopped = await self.politeness.record_antibot(host)
                if stopped:
                    self._stopped_hosts.add(host)
                return

            # Record success
            await self.politeness.record_success(host)
            self.db.update_host_stats(host, requests_delta=1)

            # Extract all links from raw HTML for crawl discovery
            raw_links = self._extract_raw_links(body, final_url)

            # Extract content (trafilatura + BS4)
            extracted = extract(body, url, strip_boilerplate=self.config.static_boilerplate)
            content_hash = hashlib.sha256(extracted.main_html.encode()).hexdigest()[:16]

            # Bot trap check
            existing_hashes = self.db.get_content_hashes()
            trap_reason = self.antibot.check_bot_trap(url, existing_hashes, content_hash)
            if trap_reason:
                self.db.mark_skipped(url, f"bot_trap:{trap_reason}")
                return

            if self.config.dry_run:
                self.db.mark_done(url)
                # Still discover links for scope analysis
                self._enqueue_links(raw_links, final_url, depth)
                return

            # Convert to markdown
            conversion = convert(extracted.main_html, url, extracted.headings)

            # Determine note title based on --title-from
            note_title = self._derive_title(extracted, url)

            # Assign filename
            existing_filenames = self.db.get_all_filenames()
            filename = assign_filename(url, note_title, existing_filenames)
            folder_path = url_to_folder_path(url, self.config.seed_url)

            if self.config.flat:
                if folder_path:
                    filename = folder_path.replace("/", "--") + "--" + filename
                folder_path = ""

            # Build frontmatter
            fm = build_frontmatter(
                title=note_title,
                source_url=url,
                site=urlparse(url).hostname or "",
                author=extracted.author,
                published=extracted.published,
                lang=extracted.lang,
                description=extracted.description,
                tags=self.config.tags or None,
            )

            # Write note
            note_content = fm + "\n" + conversion.markdown
            self._write_note(filename, folder_path, note_content)

            # Save sidecars
            meta_dir = self.config.out / "log"
            save_link_index(conversion.link_index, meta_dir, filename)
            save_headings(conversion.headings, meta_dir, filename)

            # Save to DB (with conditional GET headers for future refreshes)
            resp_etag = response.headers.get("etag")
            resp_last_modified = response.headers.get("last-modified")
            self.db.save_note(url, filename, folder_path, note_title, content_hash,
                              etag=resp_etag, last_modified=resp_last_modified)
            self.db.mark_done(url)

            # Discover and enqueue links from raw HTML (not just extracted content)
            self._enqueue_links(raw_links, final_url, depth)

            file_rel = f"{folder_path}/{filename}.md" if folder_path else f"{filename}.md"
            progress_emit("note_written", url=url, file=file_rel)

        except Exception as e:
            log.error("Error processing %s: %s", url, e, exc_info=True)
            self.db.mark_failed(url, str(e))
            self.db.update_host_stats(host, errors_delta=1)

    async def _fetch_with_retry(
        self, client: httpx.AsyncClient, url: str, host: str
    ) -> httpx.Response | None:
        """Fetch a URL with retries on transient errors."""
        last_error = None

        for attempt in range(MAX_RETRIES + 1):
            try:
                # Set Referer header
                discovered_from = None
                row = self.db.conn.execute(
                    "SELECT discovered_from FROM frontier WHERE url = ?", (url,)
                ).fetchone()
                if row and row[0]:
                    discovered_from = row[0]

                headers = {}
                if discovered_from:
                    headers["Referer"] = discovered_from

                # Conditional GET headers (for resume/refresh)
                cond_headers = self.db.get_conditional_headers(url)
                headers.update(cond_headers)

                response = await client.get(url, headers=headers)

                # Handle 304 Not Modified
                if response.status_code == 304:
                    progress_emit("fetch_unchanged", url=url, via="etag" if cond_headers.get("If-None-Match") else "last-modified")
                    self.db.mark_done(url)
                    return None

                # Handle retryable status codes
                if response.status_code in TRANSIENT_STATUS:
                    if response.status_code == 429:
                        retry_after = self._parse_retry_after(response)
                        await self.politeness.record_error(
                            host, 429, retry_after
                        )
                        if attempt < MAX_RETRIES:
                            continue
                    elif response.status_code == 503:
                        retry_after = self._parse_retry_after(response)
                        await self.politeness.record_error(
                            host, 503, retry_after
                        )
                        if attempt < MAX_RETRIES:
                            continue
                    else:
                        await self.politeness.record_error(host, response.status_code)
                        if attempt < MAX_RETRIES:
                            continue

                if response.status_code in PERMANENT_STATUS:
                    self.db.mark_failed(url, f"http_{response.status_code}")
                    self.db.update_host_stats(host, requests_delta=1, errors_delta=1)
                    return None

                if response.status_code >= 400:
                    if attempt < MAX_RETRIES:
                        continue
                    self.db.mark_failed(url, f"http_{response.status_code}")
                    self.db.update_host_stats(host, requests_delta=1, errors_delta=1)
                    return None

                return response

            except (httpx.ConnectError, httpx.ReadTimeout, httpx.ConnectTimeout,
                    httpx.PoolTimeout, httpx.RemoteProtocolError) as e:
                last_error = e
                await self.politeness.record_error(host, status_code=None)
                if attempt < MAX_RETRIES:
                    await asyncio.sleep(2 ** attempt)
                    continue

            except Exception as e:
                last_error = e
                break

        self.db.mark_failed(url, f"fetch_error:{last_error}")
        self.db.update_host_stats(host, requests_delta=1, errors_delta=1)
        return None

    def _enqueue_links(
        self, links: list[dict], source_url: str, current_depth: int
    ) -> None:
        """Discover and enqueue links from a page."""
        if current_depth >= self.config.depth:
            return

        for link in links:
            href = link.get("href", "")
            if not href:
                continue

            # Resolve relative URLs
            absolute_url = urljoin(source_url, href)

            # Skip non-HTTP schemes
            parsed = urlparse(absolute_url)
            if parsed.scheme.lower() in SKIP_SCHEMES:
                continue
            if parsed.scheme.lower() not in ("http", "https"):
                continue

            # Canonicalize
            canonical = canonicalize(absolute_url, self.config.seed_url)

            # Skip session ID URLs
            if AntibotDetector.has_session_params(canonical):
                continue

            # Scope check
            if not self._in_scope(canonical):
                continue

            # Include/exclude filters
            if self._include_re and not any(r.search(canonical) for r in self._include_re):
                continue
            if self._exclude_re and any(r.search(canonical) for r in self._exclude_re):
                continue

            # Enqueue
            self.db.add_to_frontier(
                canonical,
                depth=current_depth + 1,
                discovered_from=source_url,
            )

    def _in_scope(self, url: str) -> bool:
        """Check if a URL is within the configured crawl scope."""
        if not self.config.same_domain:
            return True

        parsed = urlparse(url)
        url_host = (parsed.hostname or "").lower()
        seed_host = (self.seed_parsed.hostname or "").lower()

        # Host check
        if self.config.subdomain_policy == "strict":
            host_ok = url_host == seed_host
        elif self.config.subdomain_policy == "include":
            host_ok = url_host == seed_host or url_host.endswith(f".{seed_host}")
        else:  # any
            seed_parts = seed_host.rsplit(".", 2)
            url_parts = url_host.rsplit(".", 2)
            seed_base = ".".join(seed_parts[-2:]) if len(seed_parts) >= 2 else seed_host
            url_base = ".".join(url_parts[-2:]) if len(url_parts) >= 2 else url_host
            host_ok = url_base == seed_base

        if not host_ok:
            return False

        # Path prefix check: only follow URLs under the seed's path prefix.
        # e.g. seed "/docs/en/" restricts to URLs starting with "/docs/en/"
        url_path = parsed.path or "/"
        return url_path.startswith(self._seed_path_prefix)

    def _is_html_content(self, content_type: str) -> bool:
        """Check if content type is processable."""
        ct = content_type.lower().split(";")[0].strip()
        return ct in ALLOWED_CONTENT_TYPES

    def _write_note(self, filename: str, folder_path: str, content: str) -> None:
        """Write a markdown note to disk."""
        if folder_path:
            note_dir = self.config.out / folder_path
        else:
            note_dir = self.config.out
        note_dir.mkdir(parents=True, exist_ok=True)
        note_path = note_dir / f"{filename}.md"

        # Collision avoidance: don't overwrite
        if note_path.exists():
            log.debug("Note already exists, skipping: %s", note_path)
            return

        note_path.write_text(content, encoding="utf-8")

    def _default_headers(self) -> dict[str, str]:
        """Default HTTP headers for requests."""
        return {
            "User-Agent": self.config.user_agent,
            "Accept": "text/html,application/xhtml+xml",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
        }

    def _parse_retry_after(self, response: httpx.Response) -> float | None:
        """Parse Retry-After header value."""
        val = response.headers.get("retry-after")
        if val is None:
            return None
        try:
            return float(val)
        except ValueError:
            return None

    def _parse_meta_refresh(self, body: str, base_url: str) -> str | None:
        """Parse meta refresh redirect target from HTML.

        Detects <meta http-equiv="refresh" content="0; url=..."> and returns
        the absolute target URL, or None if not found.
        """
        match = re.search(
            r'<meta\s[^>]*http-equiv\s*=\s*["\']?refresh["\']?[^>]*'
            r'content\s*=\s*["\']?\s*\d+\s*;\s*url\s*=\s*([^"\'\s>]+)',
            body, re.IGNORECASE,
        )
        if match:
            target = match.group(1).strip()
            return urljoin(base_url, target)
        return None

    def _extract_raw_links(self, body: str, base_url: str) -> list[dict]:
        """Extract all <a href> links from raw HTML for crawl discovery.

        Unlike extract() which uses trafilatura (strips nav/sidebar),
        this extracts from the full HTML so the crawler discovers all pages.
        """
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(body, "lxml")
        links = []
        for a in soup.find_all("a", href=True):
            href = a["href"]
            text = a.get_text(strip=True)
            fragment = None
            if "#" in href:
                _, fragment = href.rsplit("#", 1)
            links.append({
                "href": href,
                "text": text,
                "anchor_fragment": fragment,
            })
        return links

    def _derive_title(self, extracted, url: str) -> str:
        """Derive note title based on --title-from config."""
        mode = self.config.title_from
        if mode == "h1":
            for h in extracted.headings:
                if h.get("level") == 1 and h.get("text", "").strip():
                    return h["text"].strip()
            return extracted.title  # fallback to <title>
        elif mode == "url":
            parsed = urlparse(url)
            path = parsed.path.strip("/")
            if path:
                segment = path.rsplit("/", 1)[-1]
                # Strip extensions
                for ext in (".html", ".htm", ".php", ".asp", ".aspx"):
                    if segment.lower().endswith(ext):
                        segment = segment[:-(len(ext))]
                        break
                return segment.replace("-", " ").replace("_", " ").title()
            return parsed.hostname or "Untitled"
        else:  # auto
            return extracted.title

    def _log_summary(self) -> None:
        """Log a summary of the crawl results."""
        counts = self.db.count_by_status()
        total = sum(counts.values())
        log.info(
            "Crawl complete: %d total, %d done, %d failed, %d skipped, %d pending",
            total,
            counts.get("done", 0),
            counts.get("failed", 0),
            counts.get("skipped", 0),
            counts.get("pending", 0),
        )

        # Host stats
        for hs in self.db.get_all_host_stats():
            log.info(
                "  Host %s: %d requests, %d errors",
                hs["host"], hs["requests"], hs["errors"],
            )
