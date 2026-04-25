"""Tests for structured exit codes."""

import pytest

from site2vault import exit_codes
from site2vault.config import RunConfig
from site2vault.state import StateDB


class TestExitCodeConstants:
    def test_success(self):
        assert exit_codes.SUCCESS == 0

    def test_fatal(self):
        assert exit_codes.FATAL == 1

    def test_partial(self):
        assert exit_codes.PARTIAL == 2

    def test_user_abort(self):
        assert exit_codes.USER_ABORT == 3

    def test_resume_conflict(self):
        assert exit_codes.RESUME_CONFLICT == 4


class TestResumeConflict:
    @pytest.mark.asyncio
    async def test_resume_conflict_returns_4(self, tmp_path):
        from site2vault.orchestrator import run

        out = tmp_path / "vault"
        out.mkdir()

        # First run with one seed URL
        config1 = RunConfig(seed_url="https://example.com", out=out, max_pages=0)
        db = StateDB(out)
        db.initialize()
        db.save_config(config1)
        db.close()

        # Second run with a different seed URL, no --force
        config2 = RunConfig(seed_url="https://other.com", out=out, force=False)

        code = await run(config2)
        assert code == exit_codes.RESUME_CONFLICT

    @pytest.mark.asyncio
    async def test_force_overrides_conflict(self, tmp_path):
        """--force should bypass resume conflict and return 0."""
        from site2vault.orchestrator import run

        out = tmp_path / "vault"
        out.mkdir()

        config1 = RunConfig(seed_url="https://example.com", out=out, max_pages=0)
        db = StateDB(out)
        db.initialize()
        db.save_config(config1)
        db.close()

        # Force with max_pages=0 so it exits immediately
        config2 = RunConfig(seed_url="https://other.com", out=out, force=True, max_pages=0)
        code = await run(config2)
        assert code == exit_codes.SUCCESS


class TestPartialSuccess:
    def test_crawler_tracks_stopped_hosts(self):
        """Crawler.has_stopped_hosts() reflects host stops."""
        from site2vault.crawler import Crawler
        from site2vault.robots import RobotsChecker

        config = RunConfig(seed_url="https://example.com", out=".")
        db_mock = type("MockDB", (), {
            "reset_in_progress": lambda self: 0,
            "add_to_frontier": lambda self, *a, **k: True,
            "count_done": lambda self: 0,
            "get_pending_urls": lambda self, n: [],
            "count_by_status": lambda self: {},
            "get_all_host_stats": lambda self: [],
        })()

        robots = RobotsChecker(config)
        crawler = Crawler(config, db_mock, robots)

        assert not crawler.has_stopped_hosts()
        crawler._stopped_hosts.add("example.com")
        assert crawler.has_stopped_hosts()
