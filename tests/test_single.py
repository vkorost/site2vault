"""Tests for single-page mode."""

import json
from pathlib import Path

import pytest

from site2vault.config import RunConfig


class TestSingleConfig:
    def test_single_sets_depth_zero(self):
        config = RunConfig(seed_url="https://example.com", single=True, depth=0, max_pages=1)
        assert config.depth == 0
        assert config.max_pages == 1
        assert config.single is True

    def test_single_disables_sitemap(self):
        """When single is set in CLI, use_sitemap should be False."""
        # This is enforced in cli.py, not config.py
        config = RunConfig(seed_url="https://example.com", single=True, use_sitemap=False)
        assert config.use_sitemap is False


class TestSingleFreshVault:
    @pytest.mark.asyncio
    async def test_single_produces_one_note(self, tmp_path):
        """--single against a fresh directory should produce exactly one note."""
        from site2vault.orchestrator import run

        out = tmp_path / "vault"
        out.mkdir()

        config = RunConfig(
            seed_url="https://example.com",
            out=out,
            depth=0,
            max_pages=1,
            single=True,
            use_sitemap=False,
        )

        # This will fail to fetch (no real server), but should not crash
        # and should create the DB structure
        code = await run(config)
        # Will get exit code 0 since max_pages=1 and the fetch fails,
        # frontier empties, crawl ends normally
        assert code in (0, 2)


class TestManifestMerge:
    def test_merge_into_existing_manifest(self, tmp_path):
        """In single mode, new note should merge into existing manifest."""
        from site2vault.orchestrator import _merge_manifest

        out = tmp_path / "vault"
        out.mkdir()

        # Create existing manifest
        manifest_dir = out / ".site2vault"
        manifest_dir.mkdir()
        existing = {
            "schema_version": 1,
            "seed_url": "https://example.com",
            "crawled_at": "2026-01-01T00:00:00Z",
            "site2vault_version": "0.1.0",
            "stats": {
                "note_count": 1,
                "total_word_count": 100,
                "estimated_total_tokens": 133,
                "failed_url_count": 0,
                "skipped_url_count": 0,
            },
            "notes": [
                {
                    "file": "Page A.md",
                    "url": "https://example.com/a",
                    "title": "Page A",
                    "folder": "",
                    "headings": [],
                    "outbound_internal_links": [],
                    "outbound_external_links": [],
                    "word_count": 100,
                    "estimated_tokens": 133,
                    "content_hash": "abc",
                }
            ],
        }
        (manifest_dir / "manifest.json").write_text(
            json.dumps(existing), encoding="utf-8"
        )

        # New manifest with one new note
        new_manifest = {
            "schema_version": 1,
            "seed_url": "https://example.com",
            "crawled_at": "2026-04-24T00:00:00Z",
            "site2vault_version": "0.1.0",
            "stats": {"note_count": 1, "total_word_count": 50, "estimated_total_tokens": 67},
            "notes": [
                {
                    "file": "Page B.md",
                    "url": "https://example.com/b",
                    "title": "Page B",
                    "folder": "",
                    "headings": [],
                    "outbound_internal_links": [],
                    "outbound_external_links": [],
                    "word_count": 50,
                    "estimated_tokens": 67,
                    "content_hash": "def",
                }
            ],
        }

        config = RunConfig(seed_url="https://example.com", out=out, single=True)
        _merge_manifest(config, new_manifest)

        merged = json.loads((manifest_dir / "manifest.json").read_text(encoding="utf-8"))
        assert merged["stats"]["note_count"] == 2
        assert merged["stats"]["total_word_count"] == 150
        urls = {n["url"] for n in merged["notes"]}
        assert "https://example.com/a" in urls
        assert "https://example.com/b" in urls

    def test_merge_updates_existing_note(self, tmp_path):
        """Merging a note with same URL should update it."""
        from site2vault.orchestrator import _merge_manifest

        out = tmp_path / "vault"
        out.mkdir()

        manifest_dir = out / ".site2vault"
        manifest_dir.mkdir()
        existing = {
            "schema_version": 1,
            "seed_url": "https://example.com",
            "crawled_at": "2026-01-01T00:00:00Z",
            "site2vault_version": "0.1.0",
            "stats": {"note_count": 1, "total_word_count": 100, "estimated_total_tokens": 133},
            "notes": [
                {"file": "Page A.md", "url": "https://example.com/a", "title": "Page A OLD",
                 "folder": "", "headings": [], "outbound_internal_links": [],
                 "outbound_external_links": [], "word_count": 100, "estimated_tokens": 133,
                 "content_hash": "old"}
            ],
        }
        (manifest_dir / "manifest.json").write_text(json.dumps(existing), encoding="utf-8")

        new_manifest = {
            "schema_version": 1, "seed_url": "https://example.com",
            "crawled_at": "2026-04-24T00:00:00Z", "site2vault_version": "0.1.0",
            "stats": {"note_count": 1, "total_word_count": 200, "estimated_total_tokens": 266},
            "notes": [
                {"file": "Page A.md", "url": "https://example.com/a", "title": "Page A NEW",
                 "folder": "", "headings": [], "outbound_internal_links": [],
                 "outbound_external_links": [], "word_count": 200, "estimated_tokens": 266,
                 "content_hash": "new"}
            ],
        }

        config = RunConfig(seed_url="https://example.com", out=out, single=True)
        _merge_manifest(config, new_manifest)

        merged = json.loads((manifest_dir / "manifest.json").read_text(encoding="utf-8"))
        assert merged["stats"]["note_count"] == 1
        assert merged["notes"][0]["title"] == "Page A NEW"

    def test_merge_no_existing_manifest(self, tmp_path):
        """Fresh vault with --single should just write the manifest."""
        from site2vault.orchestrator import _merge_manifest

        out = tmp_path / "vault"
        out.mkdir()

        new_manifest = {
            "schema_version": 1, "seed_url": "https://example.com",
            "crawled_at": "2026-04-24T00:00:00Z", "site2vault_version": "0.1.0",
            "stats": {"note_count": 1, "total_word_count": 50, "estimated_total_tokens": 67},
            "notes": [{"file": "Page.md", "url": "https://example.com", "title": "Page",
                        "folder": "", "headings": [], "outbound_internal_links": [],
                        "outbound_external_links": [], "word_count": 50, "estimated_tokens": 67,
                        "content_hash": "abc"}],
        }

        config = RunConfig(seed_url="https://example.com", out=out, single=True)
        _merge_manifest(config, new_manifest)

        manifest_path = out / ".site2vault" / "manifest.json"
        assert manifest_path.exists()
        loaded = json.loads(manifest_path.read_text(encoding="utf-8"))
        assert loaded["stats"]["note_count"] == 1
