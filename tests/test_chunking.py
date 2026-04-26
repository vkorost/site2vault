"""Tests for heading-level chunking metadata."""

import json
from pathlib import Path

import pytest

from site2vault.chunking import compute_heading_offsets, _find_headings_with_offsets


class TestFindHeadingsWithOffsets:
    def test_basic_headings(self):
        text = "---\ntitle: Test\n---\n\n# Title\n\nIntro.\n\n## Section A\n\nContent A.\n\n## Section B\n\nContent B.\n"
        raw_bytes = text.encode("utf-8")
        headings = _find_headings_with_offsets(text, raw_bytes)

        assert len(headings) == 3
        assert headings[0]["text"] == "Title"
        assert headings[0]["level"] == 1
        assert headings[1]["text"] == "Section A"
        assert headings[2]["text"] == "Section B"

    def test_byte_offsets_correct(self):
        text = "# Title\n\nIntro.\n\n## Section A\n\nContent A.\n\n## Section B\n\nContent B.\n"
        raw_bytes = text.encode("utf-8")
        headings = _find_headings_with_offsets(text, raw_bytes)

        # Verify we can read back the expected section
        section_a = raw_bytes[headings[1]["start_byte"]:headings[1]["end_byte"]]
        section_a_text = section_a.decode("utf-8")
        assert "## Section A" in section_a_text
        assert "Content A" in section_a_text
        assert "Section B" not in section_a_text

    def test_last_heading_extends_to_eof(self):
        text = "# Title\n\n## Last Section\n\nFinal content.\n"
        raw_bytes = text.encode("utf-8")
        headings = _find_headings_with_offsets(text, raw_bytes)

        last = headings[-1]
        assert last["end_byte"] == len(raw_bytes)

        section = raw_bytes[last["start_byte"]:last["end_byte"]]
        assert b"Final content" in section

    def test_nested_headings(self):
        text = "## Parent\n\nParent content.\n\n### Child\n\nChild content.\n\n## Sibling\n\nSibling content.\n"
        raw_bytes = text.encode("utf-8")
        headings = _find_headings_with_offsets(text, raw_bytes)

        assert len(headings) == 3
        # Parent section includes the child
        parent = raw_bytes[headings[0]["start_byte"]:headings[0]["end_byte"]]
        assert b"Parent content" in parent
        assert b"Child content" in parent

        # Child section ends at sibling
        child = raw_bytes[headings[1]["start_byte"]:headings[1]["end_byte"]]
        assert b"Child content" in child
        assert b"Sibling content" not in child

    def test_slug_generation(self):
        text = "## Authentication & Rate Limits\n\nContent.\n"
        raw_bytes = text.encode("utf-8")
        headings = _find_headings_with_offsets(text, raw_bytes)

        assert headings[0]["slug"] == "authentication--rate-limits" or "authentication" in headings[0]["slug"]

    def test_unicode_content(self):
        text = "## Einf\u00fchrung\n\n\u00dcberblick \u00fcber das System.\n"
        raw_bytes = text.encode("utf-8")
        headings = _find_headings_with_offsets(text, raw_bytes)

        assert len(headings) == 1
        section = raw_bytes[headings[0]["start_byte"]:headings[0]["end_byte"]]
        assert "\u00dcberblick".encode("utf-8") in section


class TestComputeHeadingOffsets:
    def test_processes_notes(self, tmp_path):
        vault_dir = tmp_path / "vault"
        vault_dir.mkdir()
        meta_dir = vault_dir / "log"
        meta_dir.mkdir()

        # Write a note
        content = "---\nsource_url: x\n---\n\n## Section A\n\nContent A.\n\n## Section B\n\nContent B.\n"
        (vault_dir / "Page.md").write_text(content, encoding="utf-8")

        notes = [{"filename": "Page", "folder_path": ""}]
        processed = compute_heading_offsets(notes, vault_dir, meta_dir)

        assert processed == 1

        # Check sidecar
        sidecar = meta_dir / "headings" / "Page.json"
        assert sidecar.exists()
        headings = json.loads(sidecar.read_text(encoding="utf-8"))
        assert len(headings) == 2
        assert "start_byte" in headings[0]
        assert "end_byte" in headings[0]

    def test_with_folder_path(self, tmp_path):
        vault_dir = tmp_path / "vault"
        (vault_dir / "docs").mkdir(parents=True)
        meta_dir = vault_dir / "log"
        meta_dir.mkdir()

        content = "## Heading\n\nContent.\n"
        (vault_dir / "docs" / "Page.md").write_text(content, encoding="utf-8")

        notes = [{"filename": "Page", "folder_path": "docs"}]
        processed = compute_heading_offsets(notes, vault_dir, meta_dir)
        assert processed == 1

    def test_section_read_back(self, tmp_path):
        """Reading file[start_byte:end_byte] yields the expected section."""
        vault_dir = tmp_path / "vault"
        vault_dir.mkdir()
        meta_dir = vault_dir / "log"
        meta_dir.mkdir()

        content = "# Title\n\nIntro paragraph.\n\n## API Reference\n\nThe API provides...\n\n## Configuration\n\nSet up config...\n"
        note_path = vault_dir / "Page.md"
        note_path.write_text(content, encoding="utf-8")

        notes = [{"filename": "Page", "folder_path": ""}]
        compute_heading_offsets(notes, vault_dir, meta_dir)

        headings = json.loads((meta_dir / "headings" / "Page.json").read_text(encoding="utf-8"))
        raw_bytes = note_path.read_bytes()

        api_section = headings[1]  # "API Reference"
        section_bytes = raw_bytes[api_section["start_byte"]:api_section["end_byte"]]
        section_text = section_bytes.decode("utf-8")
        assert "## API Reference" in section_text
        assert "The API provides" in section_text
        assert "Configuration" not in section_text
