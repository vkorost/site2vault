"""Tests for rewrite.py - targeting 100% coverage. TDD."""

import json
import pytest
from pathlib import Path

from site2vault.config import RunConfig
from site2vault.convert import save_link_index, save_headings, PLACEHOLDER_PREFIX
from site2vault.rewrite import rewrite_all, _resolve_anchor, _format_wikilink
from site2vault.state import StateDB


@pytest.fixture
def setup_vault(tmp_path):
    """Set up a minimal vault with notes, sidecars, and DB for rewrite testing."""
    out = tmp_path / "vault"
    out.mkdir()
    meta = out / "log"

    config = RunConfig(seed_url="https://example.com", out=out, link_style="shortest")
    db = StateDB(out)
    db.initialize()
    db.save_config(config)

    return out, meta, config, db


def _write_note(out, folder_path, filename, content):
    """Helper to write a note file."""
    if folder_path:
        d = out / folder_path
    else:
        d = out
    d.mkdir(parents=True, exist_ok=True)
    (d / f"{filename}.md").write_text(content, encoding="utf-8")


class TestInScopeWikilink:
    def test_in_scope_link_becomes_wikilink(self, setup_vault):
        out, meta, config, db = setup_vault

        # Create two notes that link to each other
        db.save_note("https://example.com/a", "Page A", "", "Page A", "h1")
        db.save_note("https://example.com/b", "Page B", "", "Page B", "h2")
        db.add_to_frontier("https://example.com/a", 0)
        db.add_to_frontier("https://example.com/b", 0)
        db.mark_done("https://example.com/a")
        db.mark_done("https://example.com/b")

        # Write note A with a placeholder link to B
        _write_note(out, "", "Page A",
                    f"---\ntitle: Page A\n---\nSee [S2V_LINK_0](S2V_LINK_0) for details.")
        save_link_index({"S2V_LINK_0": {"url": "https://example.com/b", "text": "Page B"}}, meta, "Page A")
        save_headings([], meta, "Page A")
        save_headings([], meta, "Page B")

        # Write note B (no links)
        _write_note(out, "", "Page B", "---\ntitle: Page B\n---\nContent here.")

        rewrite_all(config, db)

        content = (out / "Page A.md").read_text(encoding="utf-8")
        assert "[[Page B]]" in content
        assert "S2V_LINK_0" not in content

    def test_out_of_scope_stays_external(self, setup_vault):
        out, meta, config, db = setup_vault

        db.save_note("https://example.com/a", "Page A", "", "Page A", "h1")
        db.add_to_frontier("https://example.com/a", 0)
        db.mark_done("https://example.com/a")

        _write_note(out, "", "Page A",
                    f"---\ntitle: Page A\n---\nSee [S2V_LINK_0](S2V_LINK_0).")
        save_link_index({"S2V_LINK_0": {"url": "https://external.com/page", "text": "external"}}, meta, "Page A")
        save_headings([], meta, "Page A")

        rewrite_all(config, db)

        content = (out / "Page A.md").read_text(encoding="utf-8")
        assert "https://external.com/page" in content
        assert "[[" not in content or "Page A" not in content.split("[[")[1] if "[[" in content else True

    def test_failed_page_stays_external(self, setup_vault):
        out, meta, config, db = setup_vault

        db.save_note("https://example.com/a", "Page A", "", "Page A", "h1")
        # Page B is in url_notes but with failed status
        db.save_note("https://example.com/b", "Page B", "", "Page B", "h2", status="failed")
        db.add_to_frontier("https://example.com/a", 0)
        db.mark_done("https://example.com/a")

        _write_note(out, "", "Page A",
                    f"---\ntitle: Page A\n---\nSee [S2V_LINK_0](S2V_LINK_0).")
        save_link_index({"S2V_LINK_0": {"url": "https://example.com/b", "text": "Page B"}}, meta, "Page A")
        save_headings([], meta, "Page A")
        save_headings([], meta, "Page B")

        rewrite_all(config, db)

        content = (out / "Page A.md").read_text(encoding="utf-8")
        assert "[[Page B]]" not in content


class TestHeadingAnchor:
    def test_anchor_resolves_to_heading(self, setup_vault):
        out, meta, config, db = setup_vault

        db.save_note("https://example.com/a", "Page A", "", "Page A", "h1")
        db.save_note("https://example.com/b", "Page B", "", "Page B", "h2")
        db.add_to_frontier("https://example.com/a", 0)
        db.add_to_frontier("https://example.com/b", 0)
        db.mark_done("https://example.com/a")
        db.mark_done("https://example.com/b")

        _write_note(out, "", "Page A",
                    f"---\ntitle: Page A\n---\nSee [S2V_LINK_0](S2V_LINK_0).")
        save_link_index({"S2V_LINK_0": {"url": "https://example.com/b#installation", "text": "install"}}, meta, "Page A")
        save_headings([], meta, "Page A")
        save_headings([
            {"level": 2, "text": "Installation", "slug": "installation"},
        ], meta, "Page B")

        _write_note(out, "", "Page B", "---\ntitle: Page B\n---\n## Installation\nContent.")

        rewrite_all(config, db)

        content = (out / "Page A.md").read_text(encoding="utf-8")
        assert "[[Page B#Installation|install]]" in content

    def test_missing_anchor_dropped_gracefully(self, setup_vault):
        out, meta, config, db = setup_vault

        db.save_note("https://example.com/a", "Page A", "", "Page A", "h1")
        db.save_note("https://example.com/b", "Page B", "", "Page B", "h2")
        db.add_to_frontier("https://example.com/a", 0)
        db.add_to_frontier("https://example.com/b", 0)
        db.mark_done("https://example.com/a")
        db.mark_done("https://example.com/b")

        _write_note(out, "", "Page A",
                    f"---\ntitle: Page A\n---\nSee [S2V_LINK_0](S2V_LINK_0).")
        save_link_index({"S2V_LINK_0": {"url": "https://example.com/b#nonexistent", "text": "missing"}}, meta, "Page A")
        save_headings([], meta, "Page A")
        save_headings([
            {"level": 2, "text": "Installation", "slug": "installation"},
        ], meta, "Page B")

        _write_note(out, "", "Page B", "---\ntitle: Page B\n---\n## Installation\nContent.")

        rewrite_all(config, db)

        content = (out / "Page A.md").read_text(encoding="utf-8")
        # Should link without anchor, no broken #
        assert "[[Page B|missing]]" in content
        assert "#nonexistent" not in content


class TestIdempotent:
    def test_rewrite_is_idempotent(self, setup_vault):
        out, meta, config, db = setup_vault

        db.save_note("https://example.com/a", "Page A", "", "Page A", "h1")
        db.save_note("https://example.com/b", "Page B", "", "Page B", "h2")
        db.add_to_frontier("https://example.com/a", 0)
        db.add_to_frontier("https://example.com/b", 0)
        db.mark_done("https://example.com/a")
        db.mark_done("https://example.com/b")

        _write_note(out, "", "Page A",
                    f"---\ntitle: Page A\n---\nSee [S2V_LINK_0](S2V_LINK_0).")
        _write_note(out, "", "Page B", "---\ntitle: Page B\n---\nContent.")
        save_link_index({"S2V_LINK_0": {"url": "https://example.com/b", "text": "Page B"}}, meta, "Page A")
        save_headings([], meta, "Page A")
        save_headings([], meta, "Page B")

        # First rewrite
        rewrite_all(config, db)
        first_pass = (out / "Page A.md").read_text(encoding="utf-8")

        # Second rewrite
        rewrite_all(config, db)
        second_pass = (out / "Page A.md").read_text(encoding="utf-8")

        assert first_pass == second_pass


class TestPathStyleLinks:
    def test_path_style_uses_folder(self, setup_vault):
        out, meta, config, db = setup_vault
        config.link_style = "path"

        db.save_note("https://example.com/a", "Page A", "", "Page A", "h1")
        db.save_note("https://example.com/docs/b", "Page B", "docs", "Page B", "h2")
        db.add_to_frontier("https://example.com/a", 0)
        db.add_to_frontier("https://example.com/docs/b", 0)
        db.mark_done("https://example.com/a")
        db.mark_done("https://example.com/docs/b")

        _write_note(out, "", "Page A",
                    f"---\ntitle: Page A\n---\nSee [S2V_LINK_0](S2V_LINK_0).")
        _write_note(out, "docs", "Page B", "---\ntitle: Page B\n---\nContent.")
        save_link_index({"S2V_LINK_0": {"url": "https://example.com/docs/b", "text": "docs B"}}, meta, "Page A")
        save_headings([], meta, "Page A")
        save_headings([], meta, "Page B")

        rewrite_all(config, db)

        content = (out / "Page A.md").read_text(encoding="utf-8")
        assert "[[docs/Page B|docs B]]" in content


class TestResolveAnchor:
    def test_exact_slug_match(self):
        headings = [
            {"level": 2, "text": "Installation", "slug": "installation"},
        ]
        assert _resolve_anchor("installation", headings) == "Installation"

    def test_slug_variation_match(self):
        headings = [
            {"level": 2, "text": "On Windows", "slug": "on-windows"},
        ]
        assert _resolve_anchor("on-windows", headings) == "On Windows"

    def test_no_match_returns_none(self):
        headings = [
            {"level": 2, "text": "Installation", "slug": "installation"},
        ]
        assert _resolve_anchor("nonexistent", headings) is None

    def test_empty_headings_returns_none(self):
        assert _resolve_anchor("something", []) is None

    def test_none_fragment_returns_none(self):
        assert _resolve_anchor(None, [{"level": 1, "text": "X", "slug": "x"}]) is None


class TestRedirectResolution:
    def test_redirect_resolves_to_target_note(self, setup_vault):
        out, meta, config, db = setup_vault

        db.save_note("https://example.com/a", "Page A", "", "Page A", "h1")
        db.save_note("https://example.com/new-b", "Page B", "", "Page B", "h2")
        db.save_redirect("https://example.com/old-b", "https://example.com/new-b")
        db.add_to_frontier("https://example.com/a", 0)
        db.add_to_frontier("https://example.com/new-b", 0)
        db.mark_done("https://example.com/a")
        db.mark_done("https://example.com/new-b")

        _write_note(out, "", "Page A",
                    f"---\ntitle: Page A\n---\nSee [S2V_LINK_0](S2V_LINK_0).")
        _write_note(out, "", "Page B", "---\ntitle: Page B\n---\nContent.")
        save_link_index({"S2V_LINK_0": {"url": "https://example.com/old-b", "text": "old B"}}, meta, "Page A")
        save_headings([], meta, "Page A")
        save_headings([], meta, "Page B")

        rewrite_all(config, db)

        content = (out / "Page A.md").read_text(encoding="utf-8")
        assert "[[Page B|old B]]" in content
