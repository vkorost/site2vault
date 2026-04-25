# Build Assignment: `site2vault`

Build a cross-platform Python CLI that mirrors any website into a linked Obsidian vault in the current working directory. One command in, folder of connected markdown notes out. Text only. No images, no binary assets.

---

## 1. Product spec

**Input:** a single URL.

**Output:** a folder in the current working directory containing markdown notes with Obsidian wikilinks, YAML frontmatter, and an index note. The folder can be opened directly as an Obsidian vault or dropped into an existing vault.

**Command shape:**

```
site2vault https://example.com [options]
```

**Default output path:** `./<sanitized-domain>/` (e.g. `./example-com/`). Overridable via `--out`.

**Core invariants:**
- Every page that gets scraped becomes exactly one `.md` file containing the extracted text.
- Every internal hyperlink between scraped pages becomes an Obsidian wikilink.
- Every internal hyperlink pointing to a page outside the crawl scope stays a standard markdown link with the full URL.
- Every external hyperlink stays a standard markdown link.
- Images are dropped entirely. No alt text, no placeholders, no binary downloads.
- No file is ever overwritten silently. Collisions are resolved with a short hash suffix.
- The run is resumable. Killing it mid-crawl and restarting continues where it left off.
- The crawler is polite by default and adapts to server feedback.

---

## 2. Tech stack

- **Language:** Python 3.11+.
- **CLI framework:** `typer`.
- **HTTP:** `httpx` with async client, HTTP/2 enabled, connection pooling per host.
- **HTML parsing:** `beautifulsoup4` + `lxml` parser.
- **Content extraction:** `trafilatura` for main-content isolation.
- **HTML to markdown:** `markdownify`.
- **robots.txt parser:** `urllib.robotparser` (stdlib), extended with `Crawl-delay` support via custom wrapper.
- **JS rendering (optional):** `playwright` behind a `--render-js` flag, lazy-imported.
- **State:** `sqlite3` (stdlib).
- **Frontmatter:** `pyyaml`.
- **Logging:** `rich` for console, rotating file handler for `site2vault.log` inside the output folder.
- **Packaging:** `pyproject.toml`, installable via `pip install -e .`, entry point `site2vault`.

No scrapy, no requests, no headless browser framework beyond Playwright.

---

## 3. Project layout

```
site2vault/
  pyproject.toml
  README.md
  src/site2vault/
    __init__.py
    cli.py              # Typer entry point, arg parsing, orchestration
    config.py           # Dataclass holding run config
    canonical.py        # URL canonicalization
    slug.py             # URL/title to filename mapping, collision handling
    crawler.py          # Async fetch loop, frontier
    politeness.py       # Rate limiting, jitter, adaptive backoff, circuit breaker
    robots.py           # robots.txt parsing and caching
    antibot.py          # Anti-bot / challenge / trap detection
    render_js.py        # Optional Playwright fetcher (lazy import)
    extract.py          # Trafilatura wrapper, strips boilerplate and images
    convert.py          # HTML to markdown, capturing link references
    rewrite.py          # Second-pass link rewriter (the core of the app)
    frontmatter.py      # YAML frontmatter builder
    index.py            # Generates Index.md MOC at vault root
    state.py            # SQLite schema and accessors
    logging_setup.py
  tests/
    test_canonical.py
    test_slug.py
    test_rewrite.py
    test_extract.py
    test_politeness.py
    test_antibot.py
    fixtures/
      static_site/      # small self-contained HTML corpus for offline testing
```

---

## 4. CLI interface

```
site2vault URL [OPTIONS]

Arguments:
  URL                          Seed URL. Required.

Options:
  --out PATH                   Output directory. Default: ./<domain-slug>/
  --depth INT                  Max crawl depth from seed. Default: 3.
  --max-pages INT              Hard cap on total pages. Default: 2000.
  --include PATTERN            Regex; only crawl URLs matching. Repeatable.
  --exclude PATTERN            Regex; skip URLs matching. Repeatable.
  --same-domain / --any-domain Stay on seed domain. Default: same-domain.
  --subdomain-policy {strict,include,any}
                               strict=exact host, include=include subdomains
                               of seed, any=no restriction. Default: include.
  --rate FLOAT                 Target requests per second. Default: 1.0.
  --concurrency INT            Parallel fetch workers. Default: 2.
  --jitter FLOAT               Random delay factor 0.0-1.0. Default: 0.3.
  --min-delay FLOAT            Hard minimum seconds between requests per host.
                               Default: 0.5.
  --max-errors INT             Circuit breaker threshold per 50-req window.
                               Default: 10. Pauses 60s on breach.
  --ignore-robots              Skip robots.txt. Default: respect.
  --render-js                  Use Playwright instead of httpx.
  --user-agent STRING          Override UA. Default identifies site2vault.
  --resume                     Continue previous run in --out. Default: auto.
  --force                      Re-crawl pages even if already in state.
  --flat                       Write all notes at vault root, no subfolders.
  --link-style {shortest,path} Wikilink style. Default: shortest.
  --verbose / -v               Debug logging.
  --dry-run                    Discover and list URLs, do not write files.
```

Examples:

```
site2vault https://docs.example.com
site2vault https://blog.example.com --depth 2 --exclude '/tag/' --rate 0.5
site2vault https://spa.example.com --render-js --out ./vault/spa
```

---

## 5. Obsidian output conventions

**Folder structure (default, non-flat):**

```
<out>/
  Index.md                      # MOC, links to top-level sections
  _meta/
    site2vault.sqlite           # resumable state
    url-map.json                # URL -> note path, human-readable
    site2vault.log
    link-index/                 # per-note link sidecars for the rewriter
    headings/                   # per-note heading sidecars for anchor resolution
  <section1>/
    <page>.md
    <page>.md
    <subsection>/
      <page>.md
  <section2>/
    ...
```

In flat mode, all notes live at the vault root; subfolder paths are squashed into the filename using two consecutive hyphens as separator. The converter must escape any literal double-hyphen runs in extracted content so they cannot collide with the path separator.

**Wikilink style:**
- Default `--link-style shortest`: use bare filename `[[page]]` when the filename is unique across the vault, fall back to path form `[[section/page]]` when not.
- `--link-style path`: always use path form for determinism.
- Use the alias form `[[target|anchor text]]` whenever the original link text differs from the note title.

**Heading anchors:**
- Obsidian heading links use the literal heading text: `[[page#Installation]]`.
- The converter must track every H1 through H6 in each generated note, and during the rewrite pass map web anchor IDs (`#install-guide`) back to the nearest heading text.

**Images:**
- All `<img>`, `<picture>`, `<figure>` with only image content, `<svg>`, and embedded image data are stripped during extraction.
- Image alt text is dropped. Captions inside `<figcaption>` are preserved as regular paragraphs since they are textual content.
- CSS background images, inline style backgrounds, and `<video poster="...">` are ignored.

**Filenames:**
- Use the page `<title>` element when available, sanitized.
- Fall back to the last URL path segment slugified.
- Always suffix with `-<6-char-hash>` if a collision would occur.
- Strip all Obsidian-forbidden characters: `: / \ | ? * " < > #  ^ [ ]`.
- Collapse whitespace runs to single spaces.
- Trim to 120 chars hard max.
- Preserve case for readability.

---

## 6. URL canonicalization

Implemented in `canonical.py` as a pure function `canonicalize(url: str) -> str`. Every URL entering the crawler passes through this first.

**Rules, applied in order:**

1. Lowercase scheme and host.
2. Strip default ports (`:80` for http, `:443` for https).
3. Force `https` when both `http` and `https` versions resolve to the same host and the seed uses `https`. Skip if the seed itself is `http`.
4. Drop the URL fragment for crawl-identity purposes, but retain it separately for anchor resolution in the link rewriter.
5. Remove `www.` prefix only if the seed host does not use `www.`.
6. Remove trailing slash unless the path is exactly `/`.
7. Strip tracking and session query parameters: `utm_*`, `fbclid`, `gclid`, `mc_eid`, `mc_cid`, `ref`, `ref_src`, `_hsenc`, `_hsmi`, `igshid`, `_ga`, `yclid`, `sid`, `sess`, `phpsessid`, `jsessionid`, `sessionid`. Maintain this list as a module-level constant.
8. Sort remaining query parameters alphabetically.
9. Percent-encode path segments per RFC 3986.
10. Follow HTTP redirects (up to 5) before canonicalizing. Store both original and final URL. Internal links pointing at the original URL must resolve to the note derived from the final URL.

Unit tests must cover: mixed case, trailing slashes, tracking params, session IDs, equivalent `www`/non-`www`, fragment separation, redirect chains.

---

## 7. Filename and slug rules

`slug.py` owns the URL-to-filename assignment. Every URL gets one and only one filename for the lifetime of the run.

**Algorithm:**

```
def assign_filename(url, title, existing_map, existing_filenames):
    base = sanitize(title) if title else slugify(last_path_segment(url))
    if not base:
        base = slugify(url_hash(url)[:8])
    candidate = base
    if candidate not in existing_filenames:
        return candidate
    # collision: append short hash of full URL
    suffix = sha1(url)[:6]
    return f"{base}-{suffix}"
```

**`sanitize(title)`:**
- Unicode NFKC normalize.
- Remove forbidden chars.
- Collapse whitespace.
- Strip leading/trailing dots and spaces.
- Truncate to 120.

**`slugify(s)`:**
- ASCII-fold where possible (`unicodedata`).
- Lowercase.
- Replace non-alphanumeric runs with single hyphens.
- Trim leading/trailing hyphens.

Persist the mapping in SQLite table `url_notes(url PRIMARY KEY, filename, folder_path, title, content_hash, fetched_at, status)`.

---

## 8. Crawler behavior

`crawler.py` runs an async frontier loop.

**Frontier:** SQLite table `frontier(url PRIMARY KEY, depth, discovered_from, status)` with statuses `pending`, `in_progress`, `done`, `failed`, `skipped`.

**Loop:**

```
seed = canonicalize(arg_url)
check robots.txt for seed host; refuse unless --ignore-robots
insert seed into frontier at depth 0
while frontier has pending and count(done) < max_pages:
    pick up to `concurrency` pending URLs
    politeness gate: wait for token + jitter + per-host delay
    fetch -> detect anti-bot -> extract -> convert -> discover links -> write note
    mark done; enqueue discovered links within depth and scope
```

**Scope rules:**
- `--same-domain` with subdomain policy determines host matching.
- `--include` and `--exclude` regexes applied to canonical URL.
- Skip `mailto:`, `tel:`, `javascript:`, `data:`, and any non-http(s) scheme.
- Skip URLs whose response `Content-Type` is not `text/html`, `application/xhtml+xml`, or `text/plain`.
- Skip binary responses entirely. No image handling, no PDF handling in v0.1.

**HTTP client settings:**
- HTTP/2 enabled.
- Connection keep-alive, single `AsyncClient` reused across the run.
- Per-host connection pool capped at `concurrency`.
- Read timeout 30s, connect timeout 10s, total timeout 60s.

**Retries:** 3 retries on transient errors (connection reset, timeout, 5xx except 501). Permanent errors (4xx except 429, 403, 503) do not retry. 403 and 503 may indicate soft blocks; handled in `antibot.py`.

---

## 9. Content extraction

`extract.py` takes raw HTML and returns a structured payload:

```
{
    "title": str,
    "main_html": str,      # boilerplate-stripped body, images removed
    "headings": [          # for anchor resolution
        {"level": int, "text": str, "id": str | None}
    ],
    "links": [             # every <a href> inside main_html
        {"href": str, "text": str, "anchor_fragment": str | None}
    ],
    "lang": str | None,
    "published": str | None,
    "author": str | None,
    "description": str | None,
}
```

**Pipeline:**

1. Run `trafilatura.extract(..., output_format='xml', include_links=True, include_images=False)`. Explicitly disable images.
2. Parse the XML to build the structured payload.
3. Pre-process the raw HTML to remove `<img>`, `<picture>`, `<svg>`, `<video>`, `<audio>`, `<canvas>`, `<iframe>`, `<object>`, `<embed>` before handing to the fallback extractor.
4. Preserve `<figcaption>` text content as a regular paragraph even when its parent `<figure>` wrapped an image.

**Fallback:** if trafilatura returns nothing useful (very short or empty), fall back to a beautifulsoup-based main-content heuristic that prefers `<article>`, then `<main>`, then the largest `<div>` by text density. Apply the same image-stripping step before extracting text.

**Metadata:** pull from `<meta>` tags (OpenGraph, Twitter Card, Dublin Core) and JSON-LD for author, published date, and description.

---

## 10. HTML to markdown conversion

`convert.py` takes extracted HTML (already image-free) and produces a markdown string plus a link inventory keyed to placeholder tokens.

**Strategy: placeholder-then-rewrite.** The converter cannot know final wikilink targets yet because the full URL-to-filename map does not exist on the first pass. So:

1. Before running `markdownify`, walk the HTML tree and replace every `<a href="X">text</a>` with `<a href="X">S2V_LINK_<n></a>` where `<n>` is a stable index.
2. Record the mapping `{token: original_url}` in a sidecar JSON saved next to the note under `_meta/link-index/<filename>.json`.
3. Run `markdownify` over the modified HTML.
4. Write the note with placeholders still in the body.

The second pass in `rewrite.py` replaces all placeholders with proper wikilinks or markdown links.

**Guard against token collision:** before conversion, scan the raw HTML text for any pre-existing occurrence of the literal string `S2V_LINK_`. If found, bail out with a clear error. Vanishingly rare, but the failure mode is silent corruption.

**Markdownify options:**
- `heading_style='ATX'`.
- `bullets='-'`.
- Strip `script`, `style`, `form`, `iframe`, `noscript`, `svg`, `img`, `picture`, `video`, `audio`, `canvas`.
- Preserve `code`, `pre`, `blockquote`, `table`.

---

## 11. Link rewrite pass, the core of the app

`rewrite.py` runs after the crawl completes.

**Inputs:** the completed `url_notes` table, every written note with its link-index JSON sidecar, the heading tables for each note.

**Per-note algorithm:**

```
for each note file:
    load its link-index sidecar
    for each placeholder (S2V_LINK_<n> -> original_url):
        resolve original_url to absolute form using note's source URL as base
        canonical = canonicalize(absolute_url)
        strip_and_save_fragment(canonical) -> (canonical_no_frag, fragment)

        if canonical_no_frag is in url_notes and status == done:
            target_note = url_notes[canonical_no_frag]
            anchor = resolve_anchor(fragment, target_note.headings)
            display = original_link_text
            wikilink = format_wikilink(target_note, anchor, display, link_style)
            replace placeholder with wikilink
        else:
            # out of scope or failed; keep as external markdown link
            replace placeholder with [display](absolute_url)
```

**`format_wikilink(target, anchor, display, style)`:**
- If `style == shortest` and filename is globally unique: `target.filename` (no extension).
- Else: `target.folder_path/target.filename` with forward slashes.
- If anchor: append `#` + anchor heading text verbatim.
- If display text equals the wikilink target text: `[[target]]`.
- Otherwise: `[[target|display]]`.

**`resolve_anchor(fragment, headings)`:**
- If fragment is None: return None.
- If fragment matches a heading ID exactly: return that heading's text.
- If fragment slugifies to a heading's slug: return that heading's text.
- Else: return None and log a warning. Do not emit broken `#` anchors.

Run the rewrite pass idempotently. Running it twice on the same vault must produce identical output. Write a test for this.

---

## 12. Heading anchor resolution

During conversion, record every heading in the note with both its text and its web-style slug. Store as JSON sidecar `_meta/headings/<filename>.json`:

```
[
    {"level": 2, "text": "Installation", "slug": "installation"},
    {"level": 3, "text": "On Windows", "slug": "on-windows"}
]
```

Slug algorithm must match GitHub's heading slug rules since most sites use variants of it: lowercase, strip non-alphanumerics except spaces and hyphens, replace spaces with hyphens, collapse repeat hyphens.

---

## 13. Frontmatter schema

Every note begins with YAML frontmatter:

```yaml
---
title: "Page title from HTML"
source_url: "https://example.com/docs/install"
retrieved_at: "2026-04-24T14:32:11Z"
site: "example.com"
author: "Jane Doe"          # if detected
published: "2024-03-12"     # if detected
lang: "en"                  # if detected
tags:
  - site2vault
  - site/example-com
  - section/docs
description: "First 160 chars of extracted content, one line, no newlines"
---
```

Tag derivation:
- Always include `site2vault`.
- Include `site/<domain-slug>`.
- Include `section/<first-path-segment-slug>` if path has depth.

---

## 14. State and resumability

All state in `_meta/site2vault.sqlite`. Schema:

```sql
CREATE TABLE run_config (key TEXT PRIMARY KEY, value TEXT);
CREATE TABLE frontier (
    url TEXT PRIMARY KEY,
    depth INTEGER,
    discovered_from TEXT,
    status TEXT CHECK(status IN ('pending','in_progress','done','failed','skipped')),
    error TEXT,
    updated_at TEXT
);
CREATE TABLE url_notes (
    url TEXT PRIMARY KEY,
    filename TEXT NOT NULL,
    folder_path TEXT,
    title TEXT,
    content_hash TEXT,
    fetched_at TEXT,
    status TEXT
);
CREATE TABLE redirects (
    from_url TEXT PRIMARY KEY,
    to_url TEXT NOT NULL
);
CREATE TABLE host_stats (
    host TEXT PRIMARY KEY,
    requests INTEGER DEFAULT 0,
    errors INTEGER DEFAULT 0,
    last_429_at TEXT,
    current_rate REAL,
    backoff_until TEXT
);
CREATE INDEX idx_frontier_status ON frontier(status);
CREATE INDEX idx_url_notes_filename ON url_notes(filename);
```

On startup, detect an existing `_meta/site2vault.sqlite` and continue unless `--force` is passed. Validate that seed URL and config have not changed; refuse to resume with mismatched config unless `--force`.

---

## 15. Anti-blocking and politeness

This is the module that keeps the tool from getting IP-banned and from accidentally harming a small site. Throttling alone is not enough. Production crawlers use layered defenses. This section specifies all of them.

### 15.1 Rate limiting with jitter

Global token-bucket limiter in `politeness.py`, shared across all workers.

- Tokens refill at `--rate` per second.
- Each fetch consumes one token.
- Before consuming, sleep a random `jitter * (1/rate) * U(0,1)` seconds. Default jitter of 0.3 means up to 30% random extra delay per request. This prevents the uniform-interval pattern that trivially identifies bot traffic.
- Per-host minimum delay: even if global tokens are available, a single host is never hit more than once per `--min-delay` seconds (default 0.5s). This prevents a slow global rate from becoming a hot burst on one host during frontier imbalance.

### 15.2 robots.txt

Implemented in `robots.py`.

- Fetch `<scheme>://<host>/robots.txt` once per host and cache in memory for the run.
- Respect `Disallow` rules for the user-agent string site2vault uses.
- Respect `Crawl-delay` directive: if present, override `--min-delay` with `max(min-delay, crawl-delay)` for that host.
- If `robots.txt` returns 404 or 5xx, treat as "no rules" and proceed.
- If `robots.txt` disallows the seed URL itself and `--ignore-robots` is not set, print a clear message and exit with non-zero status before any crawling starts.
- If `--ignore-robots` is set, log a prominent warning and proceed.

### 15.3 User-Agent

Default UA identifies the tool and includes a contact URL placeholder:

```
site2vault/0.1.0 (+https://github.com/<user>/site2vault; personal archival use)
```

Do not spoof a browser UA by default. Spoofing invites blocks from sites that detect inconsistencies between UA and TLS/HTTP fingerprint, and it removes the site operator's ability to contact you or carve out a rule. Users who need to spoof can pass `--user-agent`.

### 15.4 Adaptive backoff

`politeness.py` tracks error signals per host in the `host_stats` table.

- On HTTP 429: read `Retry-After` header. If present, sleep for that duration. If absent, sleep 2s then 4s then 8s then 16s then 30s on successive 429s. Also halve the effective rate for this host for the next 5 minutes.
- On HTTP 503 with `Retry-After`: honor it.
- On HTTP 503 without `Retry-After`: treat as 429.
- On repeated connection reset or timeout to one host (3 in a row): back off 60s, then resume at half rate.
- After 20 successful requests at half rate, restore full rate gradually (restore 10% per 10 successes).

### 15.5 Circuit breaker

Over a rolling window of the last 50 requests to one host:

- If `--max-errors` (default 10) or more error out, open the circuit for that host: pause all requests to it for 60 seconds, log a prominent warning.
- If the circuit opens twice in one run, stop crawling that host entirely and mark remaining URLs as `skipped` with reason `circuit_open`.
- Record every circuit event in the log with a timestamped summary.

### 15.6 Anti-bot challenge detection

`antibot.py` inspects every response. Signals that indicate a block or challenge, not real content:

- **Cloudflare challenge page:** response body contains `cf-browser-verification`, `cf-challenge`, `Just a moment...`, or status 403 with `cf-ray` header.
- **CAPTCHA:** response body contains `g-recaptcha`, `h-captcha`, `turnstile`, or `/recaptcha/api.js`.
- **Login wall redirect:** final URL after redirects differs from requested URL and ends in `/login`, `/signin`, `/auth`, or query contains `returnTo=` or `redirect=`.
- **Consent wall:** body contains GDPR consent framework signatures (`onetrust`, `cookielaw`, `quantcast`) AND the extracted text is under 200 characters (real content was not rendered).
- **Generic block page:** 403 status with body under 2 KB, or 200 status with body containing `access denied`, `forbidden`, `rate limit`, `too many requests` in title or h1.

On detection:
- Mark the URL as `failed` with reason `anti_bot: <signal>`.
- Increment a counter per host.
- If 3 anti-bot hits in a row on one host: stop crawling that host, log, suggest the user try `--render-js` or inspect the site's terms.

### 15.7 Bot-trap detection

Some sites have link patterns that expand infinitely. A faceted filter with 10 facets of 5 options each generates 9.7 million unique URLs.

Heuristics in `antibot.py`:
- **Query explosion:** if more than 100 discovered URLs share the same path but differ only in query parameters, skip all subsequent variants and log once per path.
- **Calendar explosion:** URLs matching `/YYYY/MM/DD/` or `/YYYY-MM-DD/` beyond 10 entries get a date-range filter applied; only entries within 2 years of the most-recent discovered entry are crawled.
- **Session IDs in URLs:** detect query params matching `sid`, `sess`, `phpsessid`, `jsessionid`, `sessionid` and strip them during canonicalization.
- **Infinite depth via duplicate content:** if content hash of a new page matches an existing note, mark as duplicate, do not re-enqueue its links.

### 15.8 HTTP hygiene

- Always send `Accept: text/html,application/xhtml+xml`.
- Always send `Accept-Language: en-US,en;q=0.9`.
- Send `Accept-Encoding: gzip, deflate, br` and handle decompression transparently via httpx.
- Do not send cookies by default. If a 3xx response sets a cookie and the redirect target requires it, follow the redirect with the cookie; otherwise discard.
- Do not persist cookies to disk.
- Send `Referer` set to the URL that led to the current URL (the `discovered_from` in the frontier). Many sites reject requests with a missing or external Referer.

### 15.9 Conservative defaults

The default configuration should be polite enough that a reasonable site admin would not notice the crawl:

- `--rate 1.0` (1 request per second global).
- `--concurrency 2` (two workers).
- `--min-delay 0.5` (half-second minimum between requests to one host).
- `--jitter 0.3`.
- `--max-errors 10`.
- robots.txt respected.
- Identifying UA.

For aggressive extraction of a site the user controls, pass `--rate 10 --concurrency 8`.

### 15.10 Dry-run safety net

`--dry-run` performs the crawl frontier discovery (fetching pages is still required to find links) but writes no files. Use it to preview scope and URL count before committing. In dry-run, after every 100 pages print running totals and pause 5 seconds so the user can Ctrl-C out if the scope is wrong.

---

## 16. JS-rendered sites

`render_js.py` imports Playwright lazily. Behavior:

- Launch a single headless chromium context, reuse across fetches.
- Wait for `networkidle` up to 10 seconds per page.
- Return rendered HTML to the extractor.
- Much slower than httpx; document this in README.
- Politeness layer still applies; rate limiting and anti-bot detection run identically.

If `--render-js` is passed without Playwright installed, print a clear install command and exit.

---

## 17. Index / MOC note generation

`index.py` runs at the end, after the rewrite pass. Produces `Index.md` at vault root:

```markdown
---
title: "<Site name> (mirrored by site2vault)"
source_url: "<seed URL>"
retrieved_at: "<timestamp>"
tags: [site2vault, moc]
---

# <Site name>

Mirrored from <seed URL> on <date>. <N> notes.

## Top-level sections

- [[<section1>/Index|<Section 1 title>]]
- [[<section2>/Index|<Section 2 title>]]

## All notes

<flat list, grouped by folder, one wikilink per line>
```

Each folder also gets its own `Index.md` with wikilinks to the notes inside it. This makes the vault navigable from Obsidian's graph view without the user needing Dataview.

---

## 18. Logging and error handling

- INFO to console via `rich`, formatted progress bar showing pages done / failed / queued / current rate.
- DEBUG to `_meta/site2vault.log`.
- At end of run, emit a summary table:
    - pages discovered, fetched, failed (grouped by reason: 4xx, 5xx, timeout, anti-bot, circuit-open, robots-disallow)
    - skipped URLs grouped by reason
    - hosts encountered with request counts and error counts
    - broken anchor fragments not resolved
    - out-of-scope links preserved as external

Never crash on a single bad page. Catch, log, mark failed in frontier, continue.

---

## 19. Dependencies

`pyproject.toml`:

```toml
[project]
name = "site2vault"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "typer>=0.12",
    "httpx[http2]>=0.27",
    "beautifulsoup4>=4.12",
    "lxml>=5.0",
    "trafilatura>=1.12",
    "markdownify>=0.13",
    "pyyaml>=6.0",
    "rich>=13.0",
]

[project.optional-dependencies]
js = ["playwright>=1.45"]
dev = ["pytest>=8.0", "pytest-asyncio>=0.23", "pytest-httpx>=0.30", "ruff>=0.5"]

[project.scripts]
site2vault = "site2vault.cli:app"
```

---

## 20. Testing

Target: at least 70% line coverage, 100% on `canonical.py`, `slug.py`, `rewrite.py`, and `politeness.py`.

**Required test cases:**

- `test_canonical.py`: mixed case, tracking params, trailing slash, fragment separation, `www` normalization, redirect following (mock httpx), session-id stripping.
- `test_slug.py`: title sanitization, collision handling, unicode titles, forbidden char stripping, 120-char truncation, empty title fallback.
- `test_rewrite.py`: in-scope link becomes wikilink, out-of-scope stays external, heading anchor resolves, missing anchor is dropped gracefully, alias form when display differs, idempotent second pass.
- `test_extract.py`: trafilatura happy path, empty-content fallback, heading extraction preserves order and levels, images are stripped, figcaption text is retained.
- `test_politeness.py`: token bucket honors rate, jitter falls within expected range statistically, adaptive halving on 429, circuit opens at threshold, Retry-After honored, per-host minimum delay enforced.
- `test_antibot.py`: Cloudflare fixture detected, CAPTCHA fixture detected, login-wall redirect detected, generic 403 detected, query-explosion detected, calendar explosion bounded, session IDs stripped.
- **Integration test:** `tests/fixtures/static_site/` is a pre-built 12-page corpus with cross-links, anchors, tracking params, a redirect, a robots.txt, an image tag (must be stripped), and a simulated 429 on one URL. Serve it with `pytest-httpserver`. Run full pipeline and assert the output vault structure matches a checked-in golden reference.

---

## 21. Acceptance criteria

A run against `https://docs.python.org/3/library/pathlib.html` with `--depth 2` must produce:

1. A vault folder with at least 50 notes.
2. Every note begins with valid YAML frontmatter.
3. No note contains image syntax: no `![...](...)`, no `![[...]]`, no `<img>`, no `<svg>`.
4. Opening the folder in Obsidian shows a populated graph view with no orphan notes that should have been linked.
5. At least 80% of in-scope internal links successfully rewritten to wikilinks.
6. Re-running with the same command against the same output folder produces zero changes (resumability + idempotency).
7. Killing the process at 50% completion and restarting completes successfully.
8. `Index.md` renders a valid MOC with clickable wikilinks.
9. Running against a test site that returns 429 on every 10th request completes successfully with no infinite retry loops and a logged backoff history.
10. Running against a test site with a Cloudflare challenge page on one URL marks that URL as `anti_bot` and continues with the rest.

---

## 22. Build sequence

Build in this order. Each step must pass its tests before moving on.

1. `pyproject.toml`, project skeleton, `cli.py` with `--help` working.
2. `canonical.py` + tests. No network.
3. `slug.py` + tests. No network.
4. `state.py`: SQLite schema, create/open/migrate functions + tests.
5. `extract.py` + tests using offline HTML fixtures, verifying image stripping.
6. `convert.py` with placeholder tokens + tests.
7. `politeness.py` + tests. Purely in-memory; no network.
8. `robots.py` + tests.
9. `antibot.py` + tests using fixture HTML.
10. `crawler.py`: async fetcher with politeness layer, no extraction yet. Integration test hits `tests/fixtures/static_site/`.
11. Wire crawler to extractor + converter. Writes notes with placeholders intact. Integration test.
12. `rewrite.py` + tests. Write tests first.
13. `frontmatter.py` + `index.py`.
14. Full end-to-end integration test against `tests/fixtures/static_site/`.
15. `render_js.py` behind optional extra, smoke test only.
16. README with three worked examples, install instructions, and a FAQ covering: robots.txt, JS sites, sites that block crawlers, rate limiting, how to open the output in Obsidian, what to do when a site keeps blocking you.
17. Manual test against a real docs site of user's choosing. Ship.

---

## Notes for the builder

- `rewrite.py` and `politeness.py` are the only novel work in this project. Every other module is a thin wrapper over mature libraries. Spend the proportional effort on these two.
- The placeholder token `S2V_LINK_<n>` must never appear in legitimate source content. Before conversion, scan the raw HTML for any pre-existing occurrence of the literal string `S2V_LINK_` and bail out with a clear error if found.
- Windows path handling: use `pathlib.Path` everywhere, never string concatenation. Forbidden-char stripping must include Windows-specific `<>:"|?*` even when running on Linux so vaults remain portable.
- Emit a `.gitignore` into the vault root on first run. It must exclude `_meta/site2vault.sqlite`, `_meta/site2vault.log`, and `_meta/link-index/` (sidecars are transient; the rewritten notes are the product).
- Log a clear warning if the seed URL's robots.txt disallows the crawl, and exit unless `--ignore-robots` is passed.
- Package name `site2vault` is a valid Python identifier; use it as both the distribution name on PyPI and the importable module name.
- When a site consistently blocks despite polite defaults, the answer is usually not to hammer harder but to stop and reconsider. The tool should communicate this clearly in the final summary rather than silently produce a vault full of `anti_bot` failures.
