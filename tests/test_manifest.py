"""Tests for manifest generation."""

import json
from pathlib import Path

import pytest

from site2vault.config import RunConfig
from site2vault.manifest import build_manifest, write_manifest, _strip_frontmatter
from site2vault.state import StateDB


def _make_config(tmp_path: Path, **overrides) -> RunConfig:
    out = tmp_path / "vault"
    out.mkdir()
    return RunConfig(seed_url="https://example.com", out=out, **overrides)


def _make_db(config: RunConfig) -> StateDB:
    db = StateDB(config.out)
    db.initialize()
    return db


def _write_note(out: Path, folder: str, filename: str, content: str):
    if folder:
        d = out / folder
    else:
        d = out
    d.mkdir(parents=True, exist_ok=True)
    (d / f"{filename}.md").write_text(content, encoding="utf-8")


def _write_link_index(out: Path, filename: str, index: dict):
    d = out / "log" / "link-index"
    d.mkdir(parents=True, exist_ok=True)
    (d / f"{filename}.json").write_text(json.dumps(index), encoding="utf-8")


def _write_headings(out: Path, filename: str, headings: list):
    d = out / "log" / "headings"
    d.mkdir(parents=True, exist_ok=True)
    (d / f"{filename}.json").write_text(json.dumps(headings), encoding="utf-8")


class TestBuildManifest:
    def test_basic_manifest_schema(self, tmp_path):
        config = _make_config(tmp_path)
        db = _make_db(config)

        _write_note(config.out, "", "Page A", "---\nsource_url: https://example.com/a\n---\nHello world content here.")
        _write_headings(config.out, "Page A", [{"level": 2, "text": "Section", "slug": "section"}])
        _write_link_index(config.out, "Page A", {})

        db.add_to_frontier("https://example.com/a", depth=0)
        db.mark_done("https://example.com/a")
        db.save_note("https://example.com/a", "Page A", "", "Page A", "abc123")

        manifest = build_manifest(config, db)

        assert manifest["schema_version"] == 1
        assert manifest["seed_url"] == "https://example.com"
        assert "crawled_at" in manifest
        assert manifest["site2vault_version"] == "0.1.0"
        assert manifest["stats"]["note_count"] == 1
        assert manifest["stats"]["total_word_count"] > 0
        assert manifest["stats"]["estimated_total_tokens"] > 0
        db.close()

    def test_note_count_matches_files(self, tmp_path):
        config = _make_config(tmp_path)
        db = _make_db(config)

        for i in range(5):
            name = f"Page{i}"
            url = f"https://example.com/p{i}"
            _write_note(config.out, "", name, f"---\nsource_url: {url}\n---\nContent for page {i}.")
            _write_link_index(config.out, name, {})
            _write_headings(config.out, name, [])
            db.add_to_frontier(url, depth=0)
            db.mark_done(url)
            db.save_note(url, name, "", name, f"hash{i}")

        manifest = build_manifest(config, db)
        assert manifest["stats"]["note_count"] == 5
        assert len(manifest["notes"]) == 5
        db.close()

    def test_outbound_links_resolved(self, tmp_path):
        config = _make_config(tmp_path)
        db = _make_db(config)

        # Page A links to Page B (internal) and external
        _write_note(config.out, "", "Page A", "---\nsource_url: https://example.com/a\n---\nSee [[Page B]].")
        _write_note(config.out, "", "Page B", "---\nsource_url: https://example.com/b\n---\nContent.")
        _write_link_index(config.out, "Page A", {
            "S2V_LINK_0": {"url": "https://example.com/b", "text": "Page B"},
            "S2V_LINK_1": {"url": "https://external.com/x", "text": "External"},
        })
        _write_link_index(config.out, "Page B", {})
        _write_headings(config.out, "Page A", [])
        _write_headings(config.out, "Page B", [])

        db.add_to_frontier("https://example.com/a", depth=0)
        db.mark_done("https://example.com/a")
        db.save_note("https://example.com/a", "Page A", "", "Page A", "h1")

        db.add_to_frontier("https://example.com/b", depth=1)
        db.mark_done("https://example.com/b")
        db.save_note("https://example.com/b", "Page B", "", "Page B", "h2")

        manifest = build_manifest(config, db)
        note_a = next(n for n in manifest["notes"] if n["title"] == "Page A")

        assert "Page B.md" in note_a["outbound_internal_links"]
        assert "https://external.com/x" in note_a["outbound_external_links"]
        db.close()

    def test_word_and_token_counts_nonzero(self, tmp_path):
        config = _make_config(tmp_path)
        db = _make_db(config)

        body = "This is a test note with several words in it for counting purposes."
        _write_note(config.out, "", "Page A", f"---\nsource_url: https://example.com/a\n---\n{body}")
        _write_link_index(config.out, "Page A", {})
        _write_headings(config.out, "Page A", [])

        db.add_to_frontier("https://example.com/a", depth=0)
        db.mark_done("https://example.com/a")
        db.save_note("https://example.com/a", "Page A", "", "Page A", "h1")

        manifest = build_manifest(config, db)
        note = manifest["notes"][0]

        assert note["word_count"] > 0
        assert note["estimated_tokens"] > 0
        assert note["estimated_tokens"] == round(note["word_count"] * 1.33)
        db.close()

    def test_failed_and_skipped_counts(self, tmp_path):
        config = _make_config(tmp_path)
        db = _make_db(config)

        _write_note(config.out, "", "Page A", "---\nsource_url: https://example.com/a\n---\nContent.")
        _write_link_index(config.out, "Page A", {})
        _write_headings(config.out, "Page A", [])

        db.add_to_frontier("https://example.com/a", depth=0)
        db.mark_done("https://example.com/a")
        db.save_note("https://example.com/a", "Page A", "", "Page A", "h1")

        db.add_to_frontier("https://example.com/fail", depth=1)
        db.mark_failed("https://example.com/fail", "http_404")

        db.add_to_frontier("https://example.com/skip", depth=1)
        db.mark_skipped("https://example.com/skip", "non_html")

        manifest = build_manifest(config, db)
        assert manifest["stats"]["failed_url_count"] == 1
        assert manifest["stats"]["skipped_url_count"] == 1
        db.close()

    def test_folder_path_in_file(self, tmp_path):
        config = _make_config(tmp_path)
        db = _make_db(config)

        _write_note(config.out, "docs/api", "Endpoints", "---\nsource_url: https://example.com/docs/api/endpoints\n---\nAPI content.")
        _write_link_index(config.out, "Endpoints", {})
        _write_headings(config.out, "Endpoints", [])

        db.add_to_frontier("https://example.com/docs/api/endpoints", depth=0)
        db.mark_done("https://example.com/docs/api/endpoints")
        db.save_note("https://example.com/docs/api/endpoints", "Endpoints", "docs/api", "Endpoints", "h1")

        manifest = build_manifest(config, db)
        note = manifest["notes"][0]
        assert note["file"] == "docs/api/Endpoints.md"
        assert note["folder"] == "docs/api"
        db.close()

    def test_headings_included(self, tmp_path):
        config = _make_config(tmp_path)
        db = _make_db(config)

        _write_note(config.out, "", "Page A", "---\nsource_url: https://example.com/a\n---\n## Auth\n## Rate Limits")
        _write_headings(config.out, "Page A", [
            {"level": 2, "text": "Auth", "slug": "auth"},
            {"level": 2, "text": "Rate Limits", "slug": "rate-limits"},
        ])
        _write_link_index(config.out, "Page A", {})

        db.add_to_frontier("https://example.com/a", depth=0)
        db.mark_done("https://example.com/a")
        db.save_note("https://example.com/a", "Page A", "", "Page A", "h1")

        manifest = build_manifest(config, db)
        note = manifest["notes"][0]
        assert len(note["headings"]) == 2
        assert note["headings"][0]["text"] == "Auth"
        assert note["headings"][1]["slug"] == "rate-limits"
        db.close()


class TestWriteManifest:
    def test_writes_valid_json(self, tmp_path):
        config = _make_config(tmp_path)
        manifest = {
            "schema_version": 1,
            "seed_url": "https://example.com",
            "crawled_at": "2026-04-24T18:00:00Z",
            "site2vault_version": "0.1.0",
            "stats": {"note_count": 0},
            "notes": [],
        }
        write_manifest(config, manifest)

        manifest_path = config.out / ".site2vault" / "manifest.json"
        assert manifest_path.exists()

        loaded = json.loads(manifest_path.read_text(encoding="utf-8"))
        assert loaded["schema_version"] == 1
        assert loaded["seed_url"] == "https://example.com"

    def test_no_manifest_flag(self, tmp_path):
        config = _make_config(tmp_path, emit_manifest=False)
        assert config.emit_manifest is False
        # Orchestrator would skip manifest generation when emit_manifest=False


class TestStripFrontmatter:
    def test_strips_frontmatter(self):
        content = "---\ntitle: Test\n---\nBody text here."
        assert _strip_frontmatter(content) == "Body text here."

    def test_no_frontmatter(self):
        content = "Just plain text."
        assert _strip_frontmatter(content) == "Just plain text."

    def test_empty_frontmatter(self):
        content = "---\n---\nBody."
        assert _strip_frontmatter(content) == "Body."
