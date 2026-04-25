"""Tests for sitemap discovery and parsing."""

import gzip
import pytest
import httpx

from site2vault.sitemap import (
    SitemapEntry,
    discover_sitemaps,
    parse_sitemap,
    extract_sitemap_urls_from_robots,
)


SIMPLE_SITEMAP = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://example.com/page1</loc>
    <lastmod>2026-01-01</lastmod>
  </url>
  <url>
    <loc>https://example.com/page2</loc>
  </url>
  <url>
    <loc>https://example.com/page3</loc>
    <lastmod>2026-02-15</lastmod>
  </url>
</urlset>"""

SITEMAP_INDEX = """<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap>
    <loc>https://example.com/sitemap-pages.xml</loc>
  </sitemap>
  <sitemap>
    <loc>https://example.com/sitemap-blog.xml</loc>
  </sitemap>
</sitemapindex>"""

SUB_SITEMAP = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://example.com/sub/page1</loc></url>
</urlset>"""


class TestExtractSitemapUrlsFromRobots:
    def test_extracts_sitemap_directives(self):
        text = """User-agent: *
Disallow: /admin/
Sitemap: https://example.com/sitemap.xml
Sitemap: https://example.com/sitemap2.xml
"""
        urls = extract_sitemap_urls_from_robots(text)
        assert len(urls) == 2
        assert "https://example.com/sitemap.xml" in urls
        assert "https://example.com/sitemap2.xml" in urls

    def test_no_sitemaps(self):
        text = "User-agent: *\nDisallow: /admin/\n"
        assert extract_sitemap_urls_from_robots(text) == []

    def test_case_insensitive(self):
        text = "SITEMAP: https://example.com/sitemap.xml\n"
        urls = extract_sitemap_urls_from_robots(text)
        assert len(urls) == 1


class TestParseSitemap:
    @pytest.mark.asyncio
    async def test_parse_simple_sitemap(self, httpx_mock):
        httpx_mock.add_response(
            url="https://example.com/sitemap.xml",
            content=SIMPLE_SITEMAP.encode(),
            headers={"content-type": "application/xml"},
        )

        async with httpx.AsyncClient() as client:
            entries = await parse_sitemap("https://example.com/sitemap.xml", client)

        assert len(entries) == 3
        assert entries[0].loc == "https://example.com/page1"
        assert entries[0].lastmod == "2026-01-01"
        assert entries[1].loc == "https://example.com/page2"
        assert entries[1].lastmod is None

    @pytest.mark.asyncio
    async def test_parse_sitemap_index(self, httpx_mock):
        httpx_mock.add_response(
            url="https://example.com/sitemap.xml",
            content=SITEMAP_INDEX.encode(),
            headers={"content-type": "application/xml"},
        )
        httpx_mock.add_response(
            url="https://example.com/sitemap-pages.xml",
            content=SIMPLE_SITEMAP.encode(),
            headers={"content-type": "application/xml"},
        )
        httpx_mock.add_response(
            url="https://example.com/sitemap-blog.xml",
            content=SUB_SITEMAP.encode(),
            headers={"content-type": "application/xml"},
        )

        async with httpx.AsyncClient() as client:
            entries = await parse_sitemap("https://example.com/sitemap.xml", client)

        # 3 from simple + 1 from sub
        assert len(entries) == 4

    @pytest.mark.asyncio
    async def test_parse_gzipped_sitemap(self, httpx_mock):
        compressed = gzip.compress(SIMPLE_SITEMAP.encode())
        httpx_mock.add_response(
            url="https://example.com/sitemap.xml.gz",
            content=compressed,
            headers={"content-type": "application/x-gzip"},
        )

        async with httpx.AsyncClient() as client:
            entries = await parse_sitemap("https://example.com/sitemap.xml.gz", client)

        assert len(entries) == 3

    @pytest.mark.asyncio
    async def test_html_sitemap_rejected(self, httpx_mock):
        httpx_mock.add_response(
            url="https://example.com/sitemap.xml",
            content=b"<!DOCTYPE html><html><body>Not found</body></html>",
            headers={"content-type": "text/html"},
        )

        async with httpx.AsyncClient() as client:
            entries = await parse_sitemap("https://example.com/sitemap.xml", client)

        assert len(entries) == 0

    @pytest.mark.asyncio
    async def test_404_returns_empty(self, httpx_mock):
        httpx_mock.add_response(
            url="https://example.com/sitemap.xml",
            status_code=404,
        )

        async with httpx.AsyncClient() as client:
            entries = await parse_sitemap("https://example.com/sitemap.xml", client)

        assert len(entries) == 0


class TestDiscoverSitemaps:
    @pytest.mark.asyncio
    async def test_discovers_from_robots(self, httpx_mock):
        httpx_mock.add_response(
            url="https://example.com/sitemap.xml",
            status_code=200,
            headers={"content-type": "application/xml"},
        )
        # Well-known paths return 404
        httpx_mock.add_response(
            url="https://example.com/sitemap_index.xml",
            status_code=404,
        )

        async with httpx.AsyncClient() as client:
            sitemaps = await discover_sitemaps(
                "https://example.com",
                client,
                robots_sitemap_urls=["https://example.com/sitemap.xml"],
            )

        assert "https://example.com/sitemap.xml" in sitemaps

    @pytest.mark.asyncio
    async def test_no_sitemap_available(self, httpx_mock):
        httpx_mock.add_response(
            url="https://example.com/sitemap.xml",
            status_code=404,
        )
        httpx_mock.add_response(
            url="https://example.com/sitemap_index.xml",
            status_code=404,
        )

        async with httpx.AsyncClient() as client:
            sitemaps = await discover_sitemaps("https://example.com", client)

        assert sitemaps == []

    @pytest.mark.asyncio
    async def test_rejects_html_response(self, httpx_mock):
        httpx_mock.add_response(
            url="https://example.com/sitemap.xml",
            status_code=200,
            headers={"content-type": "text/html"},
        )
        httpx_mock.add_response(
            url="https://example.com/sitemap_index.xml",
            status_code=404,
        )

        async with httpx.AsyncClient() as client:
            sitemaps = await discover_sitemaps("https://example.com", client)

        assert sitemaps == []
