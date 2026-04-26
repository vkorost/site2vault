"""Tests for state.py SQLite database."""

import pytest
from pathlib import Path

from site2vault.state import StateDB
from site2vault.config import RunConfig


@pytest.fixture
def db(tmp_path):
    """Create a fresh StateDB in a temp directory."""
    state = StateDB(tmp_path)
    state.initialize()
    yield state
    state.close()


@pytest.fixture
def config():
    return RunConfig(seed_url="https://example.com", out=Path("/tmp/test"))


class TestInitialization:
    def test_creates_sqlite_file(self, tmp_path):
        db = StateDB(tmp_path)
        db.initialize()
        assert (tmp_path / "log" / "site2vault.sqlite").exists()
        db.close()

    def test_idempotent_initialization(self, db):
        db.initialize()  # second call should not error
        db.initialize()  # third call should not error


class TestRunConfig:
    def test_save_and_check_existing(self, db, config):
        assert not db.has_existing_run()
        db.save_config(config)
        assert db.has_existing_run()

    def test_config_matches(self, db, config):
        db.save_config(config)
        assert db.config_matches(config)

    def test_config_mismatch(self, db, config):
        db.save_config(config)
        other = RunConfig(seed_url="https://other.com", out=Path("/tmp/test"))
        assert not db.config_matches(other)

    def test_config_matches_when_empty(self, db, config):
        assert db.config_matches(config)


class TestFrontier:
    def test_add_and_get_pending(self, db):
        assert db.add_to_frontier("https://example.com/a", 0)
        pending = db.get_pending_urls(10)
        assert len(pending) == 1
        assert pending[0]["url"] == "https://example.com/a"

    def test_duplicate_add_returns_false(self, db):
        assert db.add_to_frontier("https://example.com/a", 0)
        assert not db.add_to_frontier("https://example.com/a", 0)

    def test_ordering_by_depth(self, db):
        db.add_to_frontier("https://example.com/deep", 2)
        db.add_to_frontier("https://example.com/shallow", 0)
        db.add_to_frontier("https://example.com/mid", 1)
        pending = db.get_pending_urls(10)
        assert [p["depth"] for p in pending] == [0, 1, 2]

    def test_limit_respected(self, db):
        for i in range(5):
            db.add_to_frontier(f"https://example.com/{i}", 0)
        assert len(db.get_pending_urls(3)) == 3

    def test_mark_in_progress(self, db):
        db.add_to_frontier("https://example.com/a", 0)
        db.mark_in_progress("https://example.com/a")
        assert len(db.get_pending_urls(10)) == 0

    def test_mark_done(self, db):
        db.add_to_frontier("https://example.com/a", 0)
        db.mark_done("https://example.com/a")
        assert db.count_done() == 1

    def test_mark_failed(self, db):
        db.add_to_frontier("https://example.com/a", 0)
        db.mark_failed("https://example.com/a", "404")
        counts = db.count_by_status()
        assert counts.get("failed") == 1

    def test_mark_skipped(self, db):
        db.add_to_frontier("https://example.com/a", 0)
        db.mark_skipped("https://example.com/a", "circuit_open")
        counts = db.count_by_status()
        assert counts.get("skipped") == 1

    def test_reset_in_progress(self, db):
        db.add_to_frontier("https://example.com/a", 0)
        db.add_to_frontier("https://example.com/b", 0)
        db.mark_in_progress("https://example.com/a")
        db.mark_in_progress("https://example.com/b")
        count = db.reset_in_progress()
        assert count == 2
        assert len(db.get_pending_urls(10)) == 2

    def test_url_in_frontier(self, db):
        assert not db.url_in_frontier("https://example.com/a")
        db.add_to_frontier("https://example.com/a", 0)
        assert db.url_in_frontier("https://example.com/a")

    def test_count_by_status(self, db):
        db.add_to_frontier("https://example.com/a", 0)
        db.add_to_frontier("https://example.com/b", 0)
        db.mark_done("https://example.com/a")
        counts = db.count_by_status()
        assert counts["done"] == 1
        assert counts["pending"] == 1

    def test_discovered_from_stored(self, db):
        db.add_to_frontier("https://example.com/b", 1, "https://example.com/a")
        pending = db.get_pending_urls(10)
        assert pending[0]["discovered_from"] == "https://example.com/a"


class TestUrlNotes:
    def test_save_and_get(self, db):
        db.save_note("https://example.com/a", "Page A", "docs", "Page A", "abc123")
        note = db.get_note_by_url("https://example.com/a")
        assert note is not None
        assert note["filename"] == "Page A"
        assert note["folder_path"] == "docs"
        assert note["content_hash"] == "abc123"

    def test_get_nonexistent(self, db):
        assert db.get_note_by_url("https://example.com/nope") is None

    def test_get_all_notes(self, db):
        db.save_note("https://example.com/a", "A", "", "A", "h1")
        db.save_note("https://example.com/b", "B", "", "B", "h2")
        notes = db.get_all_notes()
        assert len(notes) == 2

    def test_get_all_filenames(self, db):
        db.save_note("https://example.com/a", "FileA", "", "A", "h1")
        db.save_note("https://example.com/b", "FileB", "", "B", "h2")
        filenames = db.get_all_filenames()
        assert filenames == {"FileA", "FileB"}

    def test_get_content_hashes(self, db):
        db.save_note("https://example.com/a", "A", "", "A", "hash1")
        db.save_note("https://example.com/b", "B", "", "B", "hash2")
        hashes = db.get_content_hashes()
        assert hashes == {"hash1", "hash2"}

    def test_upsert_on_save(self, db):
        db.save_note("https://example.com/a", "A", "", "A", "h1")
        db.save_note("https://example.com/a", "A-updated", "", "A", "h2")
        note = db.get_note_by_url("https://example.com/a")
        assert note["filename"] == "A-updated"


class TestRedirects:
    def test_save_and_resolve(self, db):
        db.save_redirect("https://example.com/old", "https://example.com/new")
        assert db.resolve_redirect("https://example.com/old") == "https://example.com/new"

    def test_no_redirect(self, db):
        assert db.resolve_redirect("https://example.com/page") == "https://example.com/page"

    def test_chain_resolution(self, db):
        db.save_redirect("https://example.com/a", "https://example.com/b")
        db.save_redirect("https://example.com/b", "https://example.com/c")
        assert db.resolve_redirect("https://example.com/a") == "https://example.com/c"

    def test_circular_redirect_does_not_loop(self, db):
        db.save_redirect("https://example.com/a", "https://example.com/b")
        db.save_redirect("https://example.com/b", "https://example.com/a")
        # Should not infinite loop
        result = db.resolve_redirect("https://example.com/a")
        assert result in ("https://example.com/a", "https://example.com/b")


class TestHostStats:
    def test_update_creates_entry(self, db):
        db.update_host_stats("example.com", requests_delta=1)
        stats = db.get_host_stats("example.com")
        assert stats is not None
        assert stats["requests"] == 1

    def test_update_increments(self, db):
        db.update_host_stats("example.com", requests_delta=1)
        db.update_host_stats("example.com", requests_delta=2, errors_delta=1)
        stats = db.get_host_stats("example.com")
        assert stats["requests"] == 3
        assert stats["errors"] == 1

    def test_get_nonexistent_host(self, db):
        assert db.get_host_stats("nope.com") is None

    def test_set_backoff(self, db):
        db.update_host_stats("example.com")
        db.set_host_backoff("example.com", "2026-01-01T00:00:00Z")
        stats = db.get_host_stats("example.com")
        assert stats["backoff_until"] == "2026-01-01T00:00:00Z"

    def test_set_rate(self, db):
        db.update_host_stats("example.com")
        db.set_host_rate("example.com", 0.5)
        stats = db.get_host_stats("example.com")
        assert stats["current_rate"] == 0.5

    def test_get_all_host_stats(self, db):
        db.update_host_stats("a.com", requests_delta=1)
        db.update_host_stats("b.com", requests_delta=2)
        all_stats = db.get_all_host_stats()
        assert len(all_stats) == 2
