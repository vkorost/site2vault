"""Tests for refresh mode."""

import json
from pathlib import Path

import pytest

from site2vault.config import RunConfig
from site2vault.state import StateDB


class TestRequeueForRefresh:
    def test_requeues_done_urls(self, tmp_path):
        out = tmp_path / "vault"
        out.mkdir()
        db = StateDB(out)
        db.initialize()

        db.add_to_frontier("https://example.com/a", depth=0)
        db.mark_done("https://example.com/a")
        db.add_to_frontier("https://example.com/b", depth=1)
        db.mark_done("https://example.com/b")
        db.add_to_frontier("https://example.com/c", depth=1)
        db.mark_failed("https://example.com/c", "http_500")

        requeued = db.requeue_done_for_refresh()
        assert requeued == 2

        pending = db.get_pending_urls(10)
        urls = {p["url"] for p in pending}
        assert "https://example.com/a" in urls
        assert "https://example.com/b" in urls
        # Failed URL should NOT be re-queued
        assert "https://example.com/c" not in urls
        db.close()


class TestRefreshRun:
    @pytest.mark.asyncio
    async def test_refresh_creates_with_existing_vault(self, tmp_path):
        from site2vault.orchestrator import run

        out = tmp_path / "vault"
        out.mkdir()

        # First run
        config1 = RunConfig(seed_url="https://example.com", out=out, max_pages=0)
        db = StateDB(out)
        db.initialize()
        db.save_config(config1)
        db.add_to_frontier("https://example.com/a", depth=0)
        db.mark_done("https://example.com/a")
        db.close()

        # Refresh run
        config2 = RunConfig(seed_url="https://example.com", out=out, refresh=True, max_pages=0)
        code = await run(config2)
        assert code == 0


class TestPruning:
    def test_prune_deletes_404_notes(self, tmp_path):
        from site2vault.orchestrator import _handle_refresh_removals

        out = tmp_path / "vault"
        out.mkdir()

        # Create note file
        (out / "Page A.md").write_text("---\nsource_url: x\n---\nContent.", encoding="utf-8")

        db = StateDB(out)
        db.initialize()
        db.save_note("https://example.com/a", "Page A", "", "Page A", "h1")
        db.add_to_frontier("https://example.com/a", depth=0)
        db.mark_failed("https://example.com/a", "http_404")

        config = RunConfig(seed_url="https://example.com", out=out, prune=True)
        _handle_refresh_removals(config, db)

        assert not (out / "Page A.md").exists()
        db.close()

    def test_no_prune_preserves_files(self, tmp_path):
        from site2vault.orchestrator import _handle_refresh_removals

        out = tmp_path / "vault"
        out.mkdir()

        (out / "Page A.md").write_text("---\nsource_url: x\n---\nContent.", encoding="utf-8")

        db = StateDB(out)
        db.initialize()
        db.save_note("https://example.com/a", "Page A", "", "Page A", "h1")
        db.add_to_frontier("https://example.com/a", depth=0)
        db.mark_failed("https://example.com/a", "http_404")

        config = RunConfig(seed_url="https://example.com", out=out, prune=False)
        _handle_refresh_removals(config, db)

        assert (out / "Page A.md").exists()
        db.close()

    def test_prune_ignores_non_404(self, tmp_path):
        from site2vault.orchestrator import _handle_refresh_removals

        out = tmp_path / "vault"
        out.mkdir()

        (out / "Page A.md").write_text("Content.", encoding="utf-8")

        db = StateDB(out)
        db.initialize()
        db.save_note("https://example.com/a", "Page A", "", "Page A", "h1")
        db.add_to_frontier("https://example.com/a", depth=0)
        db.mark_failed("https://example.com/a", "http_500")

        config = RunConfig(seed_url="https://example.com", out=out, prune=True)
        _handle_refresh_removals(config, db)

        # 500 errors should NOT be pruned
        assert (out / "Page A.md").exists()
        db.close()
