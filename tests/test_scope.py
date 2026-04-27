"""Tests for Crawler._in_scope path prefix enforcement."""

import pytest
from unittest.mock import MagicMock
from site2vault.config import RunConfig
from site2vault.crawler import Crawler


def _make_crawler(seed_url: str, **kwargs) -> Crawler:
    """Create a Crawler with minimal config for scope testing."""
    config = RunConfig(seed_url=seed_url, **kwargs)
    db = MagicMock()
    robots = MagicMock()
    return Crawler(config, db, robots)


class TestPathPrefix:
    """Path prefix should restrict crawl to seed URL's directory."""

    def test_same_path_prefix_allowed(self):
        c = _make_crawler("https://example.com/docs/en/")
        assert c._in_scope("https://example.com/docs/en/intro") is True

    def test_deeper_path_allowed(self):
        c = _make_crawler("https://example.com/docs/en/")
        assert c._in_scope("https://example.com/docs/en/guide/start") is True

    def test_different_path_prefix_rejected(self):
        c = _make_crawler("https://example.com/docs/en/")
        assert c._in_scope("https://example.com/docs/de/intro") is False

    def test_sibling_path_rejected(self):
        c = _make_crawler("https://example.com/docs/en/")
        assert c._in_scope("https://example.com/blog/post") is False

    def test_parent_path_rejected(self):
        c = _make_crawler("https://example.com/docs/en/")
        assert c._in_scope("https://example.com/docs/") is False

    def test_root_seed_allows_all_paths(self):
        c = _make_crawler("https://example.com/")
        assert c._in_scope("https://example.com/anything/here") is True
        assert c._in_scope("https://example.com/docs/de/") is True

    def test_no_trailing_slash_uses_parent_dir(self):
        """Seed /docs/en/intro -> prefix /docs/en/ (parent directory)."""
        c = _make_crawler("https://example.com/docs/en/intro")
        assert c._in_scope("https://example.com/docs/en/other") is True
        assert c._in_scope("https://example.com/docs/de/other") is False

    def test_different_host_rejected(self):
        c = _make_crawler("https://example.com/docs/en/")
        assert c._in_scope("https://other.com/docs/en/page") is False

    def test_subdomain_include_with_path(self):
        c = _make_crawler(
            "https://docs.example.com/api/v2/",
            subdomain_policy="include",
        )
        # Same host, matching path
        assert c._in_scope("https://docs.example.com/api/v2/ref") is True
        # Same host, different path
        assert c._in_scope("https://docs.example.com/api/v1/ref") is False
        # Subdomain, but path doesn't match seed host's path
        # (subdomain is a different host, so its path is independent —
        #  but currently path prefix is only checked against seed host)
        assert c._in_scope("https://sub.docs.example.com/api/v2/ref") is True

    def test_same_domain_false_skips_all_checks(self):
        c = _make_crawler(
            "https://example.com/docs/en/",
            same_domain=False,
        )
        assert c._in_scope("https://other.com/totally/different") is True
