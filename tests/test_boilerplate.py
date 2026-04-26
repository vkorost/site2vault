"""Tests for boilerplate stripping."""

from pathlib import Path

import pytest

from site2vault.boilerplate import (
    strip_static_boilerplate,
    detect_cross_page_boilerplate,
    remove_cross_page_boilerplate,
    _hash_paragraph,
    _extract_paragraphs,
)


class TestStaticBoilerplate:
    def test_removes_edit_link(self):
        html = '<div><p>Content here.</p><a class="edit-on-github" href="#">Edit</a></div>'
        result = strip_static_boilerplate(html)
        assert "edit-on-github" not in result
        assert "Content here" in result

    def test_removes_feedback_widget(self):
        html = '<div><p>Content.</p><div class="was-this-helpful">Was this helpful?</div></div>'
        result = strip_static_boilerplate(html)
        assert "was-this-helpful" not in result
        assert "Content" in result

    def test_removes_breadcrumb(self):
        html = '<div><nav class="breadcrumb">Home > Docs > Page</nav><p>Content.</p></div>'
        result = strip_static_boilerplate(html)
        assert "breadcrumb" not in result
        assert "Content" in result

    def test_removes_trailing_last_updated(self):
        html = '<div><p>Content.</p><p>Last updated on 2026-04-24</p></div>'
        result = strip_static_boilerplate(html)
        assert "Last updated" not in result
        assert "Content" in result

    def test_removes_edit_this_page(self):
        html = '<div><p>Content.</p><p>Edit this page on GitHub</p></div>'
        result = strip_static_boilerplate(html)
        assert "Edit this page" not in result

    def test_preserves_normal_content(self):
        html = '<div><p>Normal content paragraph.</p><h2>Section</h2><p>More content.</p></div>'
        result = strip_static_boilerplate(html)
        assert "Normal content" in result
        assert "Section" in result
        assert "More content" in result

    def test_removes_cookie_banner(self):
        html = '<div><p>Content.</p><div id="cookie-banner">We use cookies</div></div>'
        result = strip_static_boilerplate(html)
        assert "cookie-banner" not in result

    def test_removes_version_selector(self):
        html = '<div><p>Content.</p><div class="version-selector">v2.0</div></div>'
        result = strip_static_boilerplate(html)
        assert "version-selector" not in result


class TestCrossPageDetection:
    def _setup_notes(self, tmp_path, note_count, common_footer):
        """Create N notes with a common footer paragraph."""
        notes = []
        for i in range(note_count):
            name = f"Page{i}"
            path = tmp_path / f"{name}.md"
            content = f"---\nsource_url: https://example.com/p{i}\n---\n\nUnique content for page {i}.\n\n{common_footer}\n"
            path.write_text(content, encoding="utf-8")
            notes.append({"filename": name, "folder_path": ""})
        return notes

    def test_detects_common_footer(self, tmp_path):
        footer = "Copyright 2026 Example Corp. All rights reserved."
        notes = self._setup_notes(tmp_path, 25, footer)

        flagged = detect_cross_page_boilerplate(notes, tmp_path, threshold=0.5)
        footer_hash = _hash_paragraph(footer)
        assert footer_hash in flagged

    def test_skips_small_corpus(self, tmp_path):
        footer = "Copyright 2026 Example Corp."
        notes = self._setup_notes(tmp_path, 10, footer)

        flagged = detect_cross_page_boilerplate(notes, tmp_path, threshold=0.5)
        assert len(flagged) == 0  # Auto-disabled below 20 notes

    def test_respects_threshold(self, tmp_path):
        """With threshold=0.9, footer on 60% of pages should not be flagged."""
        notes = []
        footer = "Common footer text for testing threshold."
        for i in range(25):
            name = f"Page{i}"
            path = tmp_path / f"{name}.md"
            if i < 15:  # 60% have the footer
                content = f"---\nsource_url: x\n---\nContent {i}.\n\n{footer}\n"
            else:
                content = f"---\nsource_url: x\n---\nContent {i}.\n"
            path.write_text(content, encoding="utf-8")
            notes.append({"filename": name, "folder_path": ""})

        flagged = detect_cross_page_boilerplate(notes, tmp_path, threshold=0.9)
        assert len(flagged) == 0

    def test_ignores_code_blocks(self, tmp_path):
        """Paragraphs inside code blocks should not be flagged."""
        notes = []
        code_content = "import os\nprint('hello world')"
        for i in range(25):
            name = f"Page{i}"
            path = tmp_path / f"{name}.md"
            content = f"---\nsource_url: x\n---\nContent {i}.\n\n```python\n{code_content}\n```\n"
            path.write_text(content, encoding="utf-8")
            notes.append({"filename": name, "folder_path": ""})

        flagged = detect_cross_page_boilerplate(notes, tmp_path, threshold=0.5)
        # The code block content should NOT be flagged
        code_hash = _hash_paragraph(code_content)
        assert code_hash not in flagged

    def test_removal(self, tmp_path):
        """Flagged paragraphs should be removed from notes."""
        footer = "Copyright 2026 Example Corp. All rights reserved."
        notes = self._setup_notes(tmp_path, 25, footer)

        flagged = detect_cross_page_boilerplate(notes, tmp_path, threshold=0.5)
        modified = remove_cross_page_boilerplate(notes, tmp_path, flagged)

        assert modified > 0
        # Verify footer is gone from first note
        content = (tmp_path / "Page0.md").read_text(encoding="utf-8")
        assert "Copyright 2026" not in content
        assert "Unique content for page 0" in content


class TestExtractParagraphs:
    def test_basic(self):
        body = "First paragraph here.\n\nSecond paragraph here.\n"
        paras = _extract_paragraphs(body)
        assert len(paras) == 2

    def test_skips_code_blocks(self):
        body = "Paragraph one.\n\n```python\nimport os\nprint('hi')\n```\n\nParagraph two.\n"
        paras = _extract_paragraphs(body)
        texts = [p.lower() for p in paras]
        assert not any("import os" in t for t in texts)

    def test_skips_headings(self):
        body = "## Heading\n\nParagraph content.\n"
        paras = _extract_paragraphs(body)
        assert len(paras) == 1
        assert "Heading" not in paras[0]

    def test_ignores_short_fragments(self):
        body = "OK\n\nThis is a real paragraph with enough content.\n"
        paras = _extract_paragraphs(body)
        assert len(paras) == 1
