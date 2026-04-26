"""Tests for slug.py - targeting 100% coverage."""

import pytest

from site2vault.slug import (
    sanitize,
    slugify,
    url_hash,
    last_path_segment,
    assign_filename,
    url_to_folder_path,
    FORBIDDEN_CHARS,
    MAX_FILENAME_LEN,
)


class TestSanitize:
    def test_basic_title(self):
        assert sanitize("Hello World") == "Hello World"

    def test_forbidden_chars_removed(self):
        assert sanitize('Page: "Test" <foo> [bar]') == "Page Test foo bar"

    def test_unicode_nfkc_normalization(self):
        # Full-width A -> regular A
        assert sanitize("\uff21\uff22\uff23") == "ABC"

    def test_whitespace_collapsed(self):
        assert sanitize("Hello   World\t\nTest") == "Hello World Test"

    def test_leading_trailing_dots_spaces_stripped(self):
        assert sanitize("...Hello World...") == "Hello World"
        assert sanitize("  Hello  ") == "Hello"

    def test_truncation_at_120_chars(self):
        long_title = "A" * 200
        result = sanitize(long_title)
        assert len(result) == MAX_FILENAME_LEN

    def test_empty_string(self):
        assert sanitize("") == ""

    def test_only_forbidden_chars(self):
        assert sanitize(':/\\|?*"<>#^[]') == ""

    def test_hash_symbol_removed(self):
        assert sanitize("Install#Section") == "InstallSection"

    def test_pipe_removed(self):
        assert sanitize("A | B") == "A B"

    def test_preserves_case(self):
        assert sanitize("CamelCase Title") == "CamelCase Title"


class TestSlugify:
    def test_basic_string(self):
        assert slugify("Hello World") == "hello-world"

    def test_special_chars_replaced(self):
        assert slugify("foo@bar!baz") == "foo-bar-baz"

    def test_leading_trailing_hyphens_trimmed(self):
        assert slugify("---hello---") == "hello"

    def test_unicode_ascii_folded(self):
        assert slugify("café") == "cafe"
        assert slugify("über") == "uber"

    def test_empty_string(self):
        assert slugify("") == ""

    def test_consecutive_special_chars(self):
        assert slugify("a!!!b") == "a-b"

    def test_all_special_chars(self):
        assert slugify("@#$%") == ""

    def test_numbers_preserved(self):
        assert slugify("page123") == "page123"


class TestUrlHash:
    def test_deterministic(self):
        h1 = url_hash("https://example.com/page")
        h2 = url_hash("https://example.com/page")
        assert h1 == h2

    def test_different_urls_different_hashes(self):
        h1 = url_hash("https://example.com/a")
        h2 = url_hash("https://example.com/b")
        assert h1 != h2

    def test_hex_string(self):
        h = url_hash("https://example.com")
        assert all(c in "0123456789abcdef" for c in h)
        assert len(h) == 40  # SHA-1 hex digest


class TestLastPathSegment:
    def test_basic_path(self):
        assert last_path_segment("https://example.com/docs/page") == "page"

    def test_trailing_slash(self):
        assert last_path_segment("https://example.com/docs/page/") == "page"

    def test_root_path(self):
        assert last_path_segment("https://example.com/") == ""

    def test_no_path(self):
        assert last_path_segment("https://example.com") == ""

    def test_single_segment(self):
        assert last_path_segment("https://example.com/page") == "page"


class TestAssignFilename:
    def test_title_used_when_available(self):
        result = assign_filename("https://example.com/page", "My Page Title", set())
        assert result == "My Page Title"

    def test_url_segment_fallback(self):
        result = assign_filename("https://example.com/my-page", None, set())
        assert result == "my-page"

    def test_hash_fallback_for_empty_segment(self):
        result = assign_filename("https://example.com/", None, set())
        assert result  # Should be some hash-based name
        assert len(result) > 0

    def test_collision_adds_hash_suffix(self):
        existing = {"My Page"}
        result = assign_filename("https://example.com/page", "My Page", existing)
        assert result.startswith("My Page-")
        assert len(result) == len("My Page-") + 6

    def test_no_collision_returns_base(self):
        existing = {"Other Page"}
        result = assign_filename("https://example.com/page", "My Page", existing)
        assert result == "My Page"

    def test_collision_suffix_is_deterministic(self):
        existing = {"Test"}
        r1 = assign_filename("https://example.com/a", "Test", existing)
        r2 = assign_filename("https://example.com/a", "Test", existing)
        assert r1 == r2

    def test_different_urls_different_collision_suffixes(self):
        existing = {"Test"}
        r1 = assign_filename("https://example.com/a", "Test", existing)
        r2 = assign_filename("https://example.com/b", "Test", existing)
        assert r1 != r2

    def test_empty_title_and_empty_segment(self):
        result = assign_filename("https://example.com/", "", set())
        assert result  # Falls through to hash

    def test_title_with_forbidden_chars(self):
        result = assign_filename("https://example.com/p", 'Test: "Page" <1>', set())
        assert ":" not in result
        assert '"' not in result
        assert "<" not in result


class TestUrlToFolderPath:
    def test_basic_path(self):
        result = url_to_folder_path(
            "https://example.com/docs/api/page", "https://example.com"
        )
        assert result == "docs/api"

    def test_root_page(self):
        result = url_to_folder_path(
            "https://example.com/page", "https://example.com"
        )
        assert result == ""

    def test_root_url(self):
        result = url_to_folder_path(
            "https://example.com/", "https://example.com"
        )
        assert result == ""

    def test_deep_path(self):
        result = url_to_folder_path(
            "https://example.com/a/b/c/d/page", "https://example.com"
        )
        assert result == "a/b/c/d"

    def test_slugifies_path_segments(self):
        result = url_to_folder_path(
            "https://example.com/My Docs/API Guide/page", "https://example.com"
        )
        assert result == "my-docs/api-guide"
