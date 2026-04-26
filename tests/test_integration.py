"""End-to-end integration test against the static_site fixture."""

import asyncio
from pathlib import Path

import pytest
from pytest_httpserver import HTTPServer

from site2vault.config import RunConfig
from site2vault.orchestrator import run

FIXTURES = Path(__file__).parent / "fixtures" / "static_site"

# Map of URL paths to fixture files
PAGES = {
    "/": "index.html",
    "/about": "about.html",
    "/docs": "docs/index.html",
    "/docs/": "docs/index.html",
    "/docs/install": "docs/install.html",
    "/docs/config": "docs/config.html",
    "/docs/api": "docs/api.html",
    "/blog": "blog/index.html",
    "/blog/": "blog/index.html",
    "/blog/first-post": "blog/first-post.html",
    "/blog/second-post": "blog/second-post.html",
    "/blog/announcement": "blog/announcement.html",
    "/redirect-target": "redirect-target.html",
    "/robots.txt": "robots.txt",
}


def _setup_server(httpserver: HTTPServer) -> None:
    """Register all fixture pages with the HTTP server."""
    for path, fixture_file in PAGES.items():
        filepath = FIXTURES / fixture_file
        content = filepath.read_text(encoding="utf-8")
        content_type = "text/plain" if path == "/robots.txt" else "text/html"
        httpserver.expect_request(path).respond_with_data(
            content, content_type=content_type
        )

    # Set up a redirect: /old-page -> /redirect-target
    httpserver.expect_request("/old-page").respond_with_data(
        "", status=301,
        headers={"Location": "/redirect-target"},
    )


@pytest.fixture
def static_server(httpserver):
    """Set up the static site server."""
    _setup_server(httpserver)
    return httpserver


class TestFullPipeline:
    @pytest.mark.asyncio
    async def test_crawl_produces_notes(self, static_server, tmp_path):
        """Full pipeline: crawl, extract, convert, rewrite, index."""
        base_url = static_server.url_for("/")
        out = tmp_path / "vault"

        config = RunConfig(
            seed_url=base_url,
            out=out,
            depth=3,
            max_pages=50,
            rate=100.0,  # Fast for testing
            concurrency=1,
            jitter=0.0,
            min_delay=0.0,
            max_errors=50,
            ignore_robots=True,  # Skip robots.txt validation in test
        )

        from site2vault.logging_setup import setup_logging
        setup_logging(config)

        await run(config)

        # Check that notes were created
        md_files = list(out.glob("**/*.md"))
        # Filter out log directory
        md_files = [f for f in md_files if "\\log\\" not in str(f) and "/log/" not in str(f)]
        assert len(md_files) >= 5, f"Expected >=5 notes, got {len(md_files)}: {md_files}"

        # Check Index.md exists
        assert (out / "Index.md").exists(), "Index.md not found"

        # Check that all notes have YAML frontmatter
        for md_file in md_files:
            content = md_file.read_text(encoding="utf-8")
            assert content.startswith("---"), f"{md_file.name} missing frontmatter"
            # Per-folder Index.md (MOC) won't have source_url
            if md_file.name != "Index.md":
                assert "source_url:" in content, f"{md_file.name} missing source_url"

        # Check no image syntax in any note
        for md_file in md_files:
            content = md_file.read_text(encoding="utf-8")
            assert "![" not in content, f"{md_file.name} contains image markdown syntax"
            assert "<img" not in content, f"{md_file.name} contains <img> tag"
            assert "<svg" not in content, f"{md_file.name} contains <svg> tag"

    @pytest.mark.asyncio
    async def test_wikilinks_created(self, static_server, tmp_path):
        """Verify internal links are rewritten to wikilinks."""
        base_url = static_server.url_for("/")
        out = tmp_path / "vault"

        config = RunConfig(
            seed_url=base_url,
            out=out,
            depth=3,
            max_pages=50,
            rate=100.0,
            concurrency=1,
            jitter=0.0,
            min_delay=0.0,
            max_errors=50,
            ignore_robots=True,
        )

        from site2vault.logging_setup import setup_logging
        setup_logging(config)

        await run(config)

        # Count wikilinks across all notes
        wikilink_count = 0
        md_files = [f for f in out.glob("**/*.md") if "\\log\\" not in str(f) and "/log/" not in str(f)]
        for md_file in md_files:
            content = md_file.read_text(encoding="utf-8")
            wikilink_count += content.count("[[")

        assert wikilink_count >= 3, f"Expected >=3 wikilinks, got {wikilink_count}"

    @pytest.mark.asyncio
    async def test_external_links_preserved(self, static_server, tmp_path):
        """External links should remain as standard markdown links."""
        base_url = static_server.url_for("/")
        out = tmp_path / "vault"

        config = RunConfig(
            seed_url=base_url,
            out=out,
            depth=3,
            max_pages=50,
            rate=100.0,
            concurrency=1,
            jitter=0.0,
            min_delay=0.0,
            max_errors=50,
            ignore_robots=True,
        )

        from site2vault.logging_setup import setup_logging
        setup_logging(config)

        await run(config)

        # Check that external links are preserved as markdown links
        all_content = ""
        md_files = [f for f in out.glob("**/*.md") if "\\log\\" not in str(f) and "/log/" not in str(f)]
        for md_file in md_files:
            all_content += md_file.read_text(encoding="utf-8")

        assert "external.com" in all_content, "External link not preserved"

    @pytest.mark.asyncio
    async def test_state_db_populated(self, static_server, tmp_path):
        """SQLite state DB should be populated after crawl."""
        base_url = static_server.url_for("/")
        out = tmp_path / "vault"

        config = RunConfig(
            seed_url=base_url,
            out=out,
            depth=3,
            max_pages=50,
            rate=100.0,
            concurrency=1,
            jitter=0.0,
            min_delay=0.0,
            max_errors=50,
            ignore_robots=True,
        )

        from site2vault.logging_setup import setup_logging
        setup_logging(config)

        await run(config)

        from site2vault.state import StateDB
        db = StateDB(out)
        db.initialize()
        notes = db.get_all_notes()
        assert len(notes) >= 5
        counts = db.count_by_status()
        assert counts.get("done", 0) >= 5
        db.close()

    @pytest.mark.asyncio
    async def test_log_directory_structure(self, static_server, tmp_path):
        """log directory should contain DB, log files, sidecars."""
        base_url = static_server.url_for("/")
        out = tmp_path / "vault"

        config = RunConfig(
            seed_url=base_url,
            out=out,
            depth=3,
            max_pages=50,
            rate=100.0,
            concurrency=1,
            jitter=0.0,
            min_delay=0.0,
            max_errors=50,
            ignore_robots=True,
        )

        from site2vault.logging_setup import setup_logging
        setup_logging(config)

        await run(config)

        log_dir = out / "log"
        assert log_dir.exists()
        assert (log_dir / "site2vault.sqlite").exists()
        # Timestamped log file
        log_files = list(log_dir.glob("site2vault-*.log"))
        assert len(log_files) >= 1, "No timestamped log file found"
        assert (log_dir / "link-index").exists()
        assert (log_dir / "headings").exists()

    @pytest.mark.asyncio
    async def test_no_placeholder_tokens_remain(self, static_server, tmp_path):
        """No S2V_LINK_ placeholders should remain in any note."""
        base_url = static_server.url_for("/")
        out = tmp_path / "vault"

        config = RunConfig(
            seed_url=base_url,
            out=out,
            depth=3,
            max_pages=50,
            rate=100.0,
            concurrency=1,
            jitter=0.0,
            min_delay=0.0,
            max_errors=50,
            ignore_robots=True,
        )

        from site2vault.logging_setup import setup_logging
        setup_logging(config)

        await run(config)

        md_files = [f for f in out.glob("**/*.md") if "\\log\\" not in str(f) and "/log/" not in str(f)]
        for md_file in md_files:
            content = md_file.read_text(encoding="utf-8")
            assert "S2V_LINK_" not in content, f"Placeholder found in {md_file.name}"
