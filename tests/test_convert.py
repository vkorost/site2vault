"""Tests for convert.py HTML-to-markdown conversion."""

import json
import pytest
from pathlib import Path

from site2vault.convert import (
    convert,
    save_link_index,
    load_link_index,
    save_headings,
    load_headings,
    heading_slug,
    ConversionResult,
    PLACEHOLDER_PREFIX,
)


@pytest.fixture
def simple_html():
    return """<h1>Hello World</h1>
<p>This is a paragraph with <a href="/other-page">a link</a> and more text.</p>
<h2 id="section">Section Two</h2>
<p>Another paragraph with <a href="https://external.com">external link</a>.</p>"""


@pytest.fixture
def simple_headings():
    return [
        {"level": 1, "text": "Hello World", "id": None},
        {"level": 2, "text": "Section Two", "id": "section"},
    ]


class TestConvert:
    def test_returns_conversion_result(self, simple_html, simple_headings):
        result = convert(simple_html, "https://example.com/page", simple_headings)
        assert isinstance(result, ConversionResult)

    def test_markdown_not_empty(self, simple_html, simple_headings):
        result = convert(simple_html, "https://example.com/page", simple_headings)
        assert len(result.markdown) > 0

    def test_headings_in_markdown(self, simple_html, simple_headings):
        result = convert(simple_html, "https://example.com/page", simple_headings)
        assert "# Hello World" in result.markdown

    def test_links_replaced_with_placeholders(self, simple_html, simple_headings):
        result = convert(simple_html, "https://example.com/page", simple_headings)
        assert PLACEHOLDER_PREFIX in result.markdown

    def test_link_index_populated(self, simple_html, simple_headings):
        result = convert(simple_html, "https://example.com/page", simple_headings)
        assert len(result.link_index) == 2
        assert "S2V_LINK_0" in result.link_index
        assert result.link_index["S2V_LINK_0"] == {"url": "/other-page", "text": "a link"}
        assert result.link_index["S2V_LINK_1"] == {"url": "https://external.com", "text": "external link"}

    def test_heading_data_includes_slugs(self, simple_html, simple_headings):
        result = convert(simple_html, "https://example.com/page", simple_headings)
        assert len(result.headings) == 2
        assert result.headings[0]["slug"] == "hello-world"
        assert result.headings[1]["slug"] == "section-two"

    def test_raises_on_existing_token(self):
        html = f"<p>Already has {PLACEHOLDER_PREFIX}0 in it.</p>"
        with pytest.raises(ValueError, match="silent corruption"):
            convert(html, "https://example.com", [])

    def test_no_links_produces_empty_index(self):
        html = "<p>No links here.</p>"
        result = convert(html, "https://example.com", [])
        assert result.link_index == {}

    def test_atx_headings(self, simple_html, simple_headings):
        result = convert(simple_html, "https://example.com/page", simple_headings)
        assert result.markdown.startswith("#") or "\n#" in result.markdown

    def test_strips_img_tags(self):
        html = '<p>Text <img src="x.jpg" alt="photo"> more text.</p>'
        result = convert(html, "https://example.com", [])
        assert "<img" not in result.markdown
        assert "photo" not in result.markdown or "Text" in result.markdown


class TestHeadingSlug:
    def test_basic_slug(self):
        assert heading_slug("Installation") == "installation"

    def test_spaces_to_hyphens(self):
        assert heading_slug("On Windows") == "on-windows"

    def test_special_chars_stripped(self):
        assert heading_slug("What's New?") == "whats-new"

    def test_multiple_spaces(self):
        assert heading_slug("A   B   C") == "a-b-c"

    def test_numbers_preserved(self):
        assert heading_slug("Step 1") == "step-1"

    def test_hyphens_preserved(self):
        assert heading_slug("pre-existing") == "pre-existing"

    def test_collapse_hyphens(self):
        assert heading_slug("a - b - c") == "a-b-c"


class TestSidecarIO:
    def test_save_and_load_link_index(self, tmp_path):
        meta_dir = tmp_path / "log"
        index = {"S2V_LINK_0": "/page", "S2V_LINK_1": "https://ext.com"}
        save_link_index(index, meta_dir, "test-page")
        loaded = load_link_index(meta_dir, "test-page")
        assert loaded == index

    def test_load_missing_link_index(self, tmp_path):
        meta_dir = tmp_path / "log"
        assert load_link_index(meta_dir, "nonexistent") == {}

    def test_save_and_load_headings(self, tmp_path):
        meta_dir = tmp_path / "log"
        headings = [
            {"level": 1, "text": "Title", "slug": "title"},
            {"level": 2, "text": "Section", "slug": "section"},
        ]
        save_headings(headings, meta_dir, "test-page")
        loaded = load_headings(meta_dir, "test-page")
        assert loaded == headings

    def test_load_missing_headings(self, tmp_path):
        meta_dir = tmp_path / "log"
        assert load_headings(meta_dir, "nonexistent") == []

    def test_sidecar_files_created_in_correct_dirs(self, tmp_path):
        meta_dir = tmp_path / "log"
        save_link_index({"k": "v"}, meta_dir, "page")
        save_headings([{"level": 1, "text": "T", "slug": "t"}], meta_dir, "page")
        assert (meta_dir / "link-index" / "page.json").exists()
        assert (meta_dir / "headings" / "page.json").exists()


class TestMarkdownCleanup:
    def test_excessive_blank_lines_collapsed(self):
        html = "<p>A</p><p>B</p><p>C</p>"
        result = convert(html, "https://example.com", [])
        # Should not have more than 2 consecutive newlines
        assert "\n\n\n" not in result.markdown

    def test_trailing_whitespace_stripped(self):
        html = "<p>Hello   </p>"
        result = convert(html, "https://example.com", [])
        for line in result.markdown.split("\n"):
            assert line == line.rstrip()
