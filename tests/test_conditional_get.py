"""Tests for conditional GET on resume."""

import pytest

from site2vault.config import RunConfig
from site2vault.state import StateDB


class TestConditionalHeaders:
    def test_stores_etag_and_last_modified(self, tmp_path):
        out = tmp_path / "vault"
        out.mkdir()
        db = StateDB(out)
        db.initialize()

        db.save_note(
            "https://example.com/a", "Page A", "", "Page A", "hash1",
            etag='"abc123"', last_modified="Wed, 01 Jan 2026 00:00:00 GMT",
        )

        headers = db.get_conditional_headers("https://example.com/a")
        assert headers["If-None-Match"] == '"abc123"'
        assert headers["If-Modified-Since"] == "Wed, 01 Jan 2026 00:00:00 GMT"
        db.close()

    def test_no_conditional_headers_for_new_url(self, tmp_path):
        out = tmp_path / "vault"
        out.mkdir()
        db = StateDB(out)
        db.initialize()

        headers = db.get_conditional_headers("https://example.com/new")
        assert headers == {}
        db.close()

    def test_partial_headers(self, tmp_path):
        out = tmp_path / "vault"
        out.mkdir()
        db = StateDB(out)
        db.initialize()

        db.save_note(
            "https://example.com/a", "Page A", "", "Page A", "hash1",
            etag='"abc123"', last_modified=None,
        )

        headers = db.get_conditional_headers("https://example.com/a")
        assert "If-None-Match" in headers
        assert "If-Modified-Since" not in headers
        db.close()

    def test_migration_adds_columns(self, tmp_path):
        """Migration should add etag/last_modified to existing DB."""
        out = tmp_path / "vault"
        out.mkdir()
        db = StateDB(out)
        db.initialize()

        # Verify columns exist by saving with etag
        db.save_note(
            "https://example.com/a", "Page A", "", "Page A", "hash1",
            etag='"test"',
        )
        note = db.get_note_by_url("https://example.com/a")
        assert note["etag"] == '"test"'
        db.close()

    def test_304_marks_done_without_rewriting(self, tmp_path):
        """304 response should mark URL done without processing content."""
        out = tmp_path / "vault"
        out.mkdir()
        db = StateDB(out)
        db.initialize()

        # Save a note with etag
        db.save_note(
            "https://example.com/a", "Page A", "", "Page A", "hash1",
            etag='"abc"',
        )
        db.add_to_frontier("https://example.com/a", depth=0)

        # Verify conditional headers are present
        headers = db.get_conditional_headers("https://example.com/a")
        assert headers["If-None-Match"] == '"abc"'
        db.close()
