"""Sitemap.xml discovery and parsing for frontier seeding.

Discovers sitemaps from robots.txt directives and well-known paths,
parses standard sitemap XML and sitemap index files, handles gzipped
sitemaps. All URLs are filtered through canonicalization and scope checks.
"""

import gzip
import logging
import re
from dataclasses import dataclass
from urllib.parse import urljoin, urlparse
from xml.etree import ElementTree

import httpx

log = logging.getLogger("site2vault.sitemap")

SITEMAP_NS = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
MAX_INDEX_DEPTH = 2


@dataclass
class SitemapEntry:
    loc: str
    lastmod: str | None = None


async def discover_sitemaps(
    seed_url: str,
    client: httpx.AsyncClient,
    robots_sitemap_urls: list[str] | None = None,
) -> list[str]:
    """Discover sitemap URLs for a site.

    Discovery order:
    1. robots.txt Sitemap: directives (passed in).
    2. <seed_origin>/sitemap.xml
    3. <seed_origin>/sitemap_index.xml

    Returns:
        List of sitemap URLs to parse.
    """
    sitemaps = []

    # 1. From robots.txt
    if robots_sitemap_urls:
        sitemaps.extend(robots_sitemap_urls)

    # 2. Well-known paths
    parsed = urlparse(seed_url)
    origin = f"{parsed.scheme}://{parsed.hostname}"
    if parsed.port and not (
        (parsed.scheme == "http" and parsed.port == 80) or
        (parsed.scheme == "https" and parsed.port == 443)
    ):
        origin = f"{origin}:{parsed.port}"

    for path in ("/sitemap.xml", "/sitemap_index.xml"):
        url = origin + path
        if url not in sitemaps:
            sitemaps.append(url)

    # Validate which ones actually exist
    valid = []
    for url in sitemaps:
        try:
            resp = await client.head(url, follow_redirects=True)
            if resp.status_code == 200:
                ct = resp.headers.get("content-type", "")
                # Reject HTML responses (404 pages served as 200)
                if "html" not in ct.lower():
                    valid.append(url)
                else:
                    log.debug("Sitemap %s returned HTML, skipping", url)
            else:
                log.debug("Sitemap %s returned %d", url, resp.status_code)
        except Exception as e:
            log.debug("Sitemap %s unreachable: %s", url, e)

    return valid


async def parse_sitemap(
    url: str,
    client: httpx.AsyncClient,
    depth: int = 0,
) -> list[SitemapEntry]:
    """Parse a sitemap XML, recursing into sitemap indexes.

    Args:
        url: Sitemap URL.
        client: HTTP client.
        depth: Current recursion depth (capped at MAX_INDEX_DEPTH).

    Returns:
        List of SitemapEntry with discovered page URLs.
    """
    if depth > MAX_INDEX_DEPTH:
        log.warning("Sitemap index depth exceeded at %s", url)
        return []

    try:
        resp = await client.get(url, follow_redirects=True)
        if resp.status_code != 200:
            log.warning("Sitemap %s returned %d", url, resp.status_code)
            return []

        content = resp.content

        # Handle gzipped content
        if url.endswith(".gz") or resp.headers.get("content-encoding") == "gzip":
            try:
                content = gzip.decompress(content)
            except Exception:
                pass  # May already be decompressed by httpx

        xml_text = content.decode("utf-8", errors="replace")

        # Reject HTML responses
        if xml_text.strip().lower().startswith("<!doctype") or "<html" in xml_text[:500].lower():
            log.debug("Sitemap %s is HTML, not XML", url)
            return []

        return await _parse_xml(xml_text, client, depth)

    except Exception as e:
        log.warning("Failed to parse sitemap %s: %s", url, e)
        return []


async def _parse_xml(
    xml_text: str,
    client: httpx.AsyncClient,
    depth: int,
) -> list[SitemapEntry]:
    """Parse sitemap XML content."""
    try:
        root = ElementTree.fromstring(xml_text)
    except ElementTree.ParseError as e:
        log.warning("Invalid sitemap XML: %s", e)
        return []

    entries = []

    # Check if this is a sitemap index
    sitemap_refs = root.findall(f"{SITEMAP_NS}sitemap")
    if not sitemap_refs:
        # Also try without namespace
        sitemap_refs = root.findall("sitemap")

    if sitemap_refs:
        # This is a sitemap index — recurse
        for sitemap_el in sitemap_refs:
            loc_el = sitemap_el.find(f"{SITEMAP_NS}loc")
            if loc_el is None:
                loc_el = sitemap_el.find("loc")
            if loc_el is not None and loc_el.text:
                sub_entries = await parse_sitemap(loc_el.text.strip(), client, depth + 1)
                entries.extend(sub_entries)
        return entries

    # Regular sitemap — extract URLs
    url_els = root.findall(f"{SITEMAP_NS}url")
    if not url_els:
        url_els = root.findall("url")

    for url_el in url_els:
        loc_el = url_el.find(f"{SITEMAP_NS}loc")
        if loc_el is None:
            loc_el = url_el.find("loc")
        if loc_el is None or not loc_el.text:
            continue

        lastmod_el = url_el.find(f"{SITEMAP_NS}lastmod")
        if lastmod_el is None:
            lastmod_el = url_el.find("lastmod")
        lastmod = lastmod_el.text.strip() if lastmod_el is not None and lastmod_el.text else None

        entries.append(SitemapEntry(loc=loc_el.text.strip(), lastmod=lastmod))

    return entries


def extract_sitemap_urls_from_robots(robots_text: str) -> list[str]:
    """Extract Sitemap: directives from robots.txt content."""
    urls = []
    for line in robots_text.splitlines():
        line = line.strip()
        if line.lower().startswith("sitemap:"):
            url = line.split(":", 1)[1].strip()
            if url:
                urls.append(url)
    return urls
