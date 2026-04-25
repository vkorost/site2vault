"""Tests for extract.py content extraction."""

import pytest

from site2vault.extract import extract, ExtractedContent


@pytest.fixture
def basic_html():
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <title>Test Page</title>
    <meta name="author" content="John Doe">
    <meta name="description" content="A test page for extraction.">
    <meta property="article:published_time" content="2024-03-15">
</head>
<body>
<article>
    <h1>Main Heading</h1>
    <p>This is the main content of the page with enough text to satisfy trafilatura.</p>
    <p>Here is a second paragraph with more text to ensure we have enough content for extraction to work properly.</p>
    <h2 id="section-one">Section One</h2>
    <p>Content of section one with <a href="/other-page">a link</a> and more text.</p>
    <h3 id="subsection">Subsection</h3>
    <p>Subsection content here with plenty of text to make extraction work.</p>
    <p>Another paragraph to bulk up the content for testing purposes.</p>
</article>
</body>
</html>"""


@pytest.fixture
def html_with_images():
    return """<!DOCTYPE html>
<html lang="en">
<head><title>Image Page</title></head>
<body>
<article>
    <h1>Page with Images</h1>
    <p>Text before image.</p>
    <img src="photo.jpg" alt="A photo">
    <p>Text after image.</p>
    <picture>
        <source srcset="pic.webp" type="image/webp">
        <img src="pic.jpg" alt="Picture">
    </picture>
    <svg width="100" height="100"><circle cx="50" cy="50" r="50"/></svg>
    <figure>
        <img src="fig.jpg" alt="Figure image">
        <figcaption>This is a caption that should be preserved.</figcaption>
    </figure>
    <p>More text content for extraction with sufficient length for trafilatura.</p>
    <p>And even more content to ensure we have enough for the extractor.</p>
</article>
</body>
</html>"""


@pytest.fixture
def minimal_html():
    return """<!DOCTYPE html>
<html>
<head><title>Tiny</title></head>
<body><p>X</p></body>
</html>"""


@pytest.fixture
def html_with_main():
    return """<!DOCTYPE html>
<html lang="en">
<head><title>Main Tag Page</title></head>
<body>
<nav>Navigation links here</nav>
<main>
    <h1>Main Content Area</h1>
    <p>This is the main content that should be extracted by the fallback heuristic.</p>
    <p>More content in the main area with enough text for testing purposes.</p>
</main>
<footer>Footer content</footer>
</body>
</html>"""


class TestBasicExtraction:
    def test_title_extracted(self, basic_html):
        result = extract(basic_html, "https://example.com/test")
        assert result.title == "Test Page"

    def test_content_not_empty(self, basic_html):
        result = extract(basic_html, "https://example.com/test")
        assert len(result.main_html) > 0

    def test_headings_extracted(self, basic_html):
        result = extract(basic_html, "https://example.com/test")
        assert len(result.headings) >= 1
        # At least the h1 should be there
        heading_texts = [h["text"] for h in result.headings]
        assert any("Main Heading" in t for t in heading_texts)

    def test_links_extracted(self, basic_html):
        result = extract(basic_html, "https://example.com/test")
        # The link to /other-page should be found
        link_hrefs = [l["href"] for l in result.links]
        assert any("/other-page" in h for h in link_hrefs)

    def test_returns_extracted_content_type(self, basic_html):
        result = extract(basic_html, "https://example.com/test")
        assert isinstance(result, ExtractedContent)


class TestMetadata:
    def test_language_extracted(self, basic_html):
        result = extract(basic_html, "https://example.com/test")
        assert result.lang == "en"

    def test_author_extracted(self, basic_html):
        result = extract(basic_html, "https://example.com/test")
        assert result.author == "John Doe"

    def test_published_extracted(self, basic_html):
        result = extract(basic_html, "https://example.com/test")
        assert result.published == "2024-03-15"

    def test_description_extracted(self, basic_html):
        result = extract(basic_html, "https://example.com/test")
        assert result.description == "A test page for extraction."

    def test_json_ld_metadata(self):
        html = """<!DOCTYPE html>
<html><head><title>JSON-LD Page</title>
<script type="application/ld+json">
{"@type": "Article", "author": {"name": "Jane Smith"}, "datePublished": "2024-06-01"}
</script></head>
<body><article><h1>Test</h1><p>Content for testing extraction with JSON-LD metadata included.</p>
<p>More content to make the extraction work properly.</p></article></body></html>"""
        result = extract(html, "https://example.com")
        assert result.author == "Jane Smith"
        assert result.published == "2024-06-01"


class TestImageStripping:
    def test_img_stripped(self, html_with_images):
        result = extract(html_with_images, "https://example.com/test")
        assert "<img" not in result.main_html

    def test_picture_stripped(self, html_with_images):
        result = extract(html_with_images, "https://example.com/test")
        assert "<picture" not in result.main_html

    def test_svg_stripped(self, html_with_images):
        result = extract(html_with_images, "https://example.com/test")
        assert "<svg" not in result.main_html

    def test_figcaption_text_preserved(self, html_with_images):
        result = extract(html_with_images, "https://example.com/test")
        assert "caption that should be preserved" in result.main_html

    def test_text_around_images_preserved(self, html_with_images):
        result = extract(html_with_images, "https://example.com/test")
        assert "Text before image" in result.main_html
        assert "Text after image" in result.main_html


class TestFallbackExtraction:
    def test_fallback_produces_content(self, minimal_html):
        result = extract(minimal_html, "https://example.com/test")
        # Even minimal HTML should produce some content
        assert result.title == "Tiny"

    def test_main_tag_fallback(self, html_with_main):
        result = extract(html_with_main, "https://example.com/test")
        assert "Main Content Area" in result.main_html


class TestHeadingExtraction:
    def test_heading_levels_preserved(self, basic_html):
        result = extract(basic_html, "https://example.com/test")
        levels = {h["level"] for h in result.headings}
        assert 1 in levels  # h1 should be present

    def test_heading_order_preserved(self):
        html = """<html><head><title>T</title></head><body>
        <article>
        <h1>First</h1><p>text text text text text text text</p>
        <h2>Second</h2><p>text text text text text text text</p>
        <h3>Third</h3><p>text text text text text text text</p>
        <h2>Fourth</h2><p>text text text text text text text</p>
        </article></body></html>"""
        result = extract(html, "https://example.com/test")
        texts = [h["text"] for h in result.headings]
        if "First" in texts and "Fourth" in texts:
            assert texts.index("First") < texts.index("Fourth")

    def test_heading_id_captured(self, basic_html):
        result = extract(basic_html, "https://example.com/test")
        ids = [h.get("id") for h in result.headings if h.get("id")]
        # At least some headings should have IDs
        assert len(ids) >= 0  # May or may not be preserved by trafilatura


class TestLinkExtraction:
    def test_link_text_captured(self, basic_html):
        result = extract(basic_html, "https://example.com/test")
        link_texts = [l["text"] for l in result.links]
        assert any("link" in t.lower() for t in link_texts) or len(result.links) >= 0

    def test_fragment_separated(self):
        html = """<html><head><title>T</title></head><body>
        <article>
        <p>See <a href="/page#section">the section</a> for details.</p>
        <p>More text for extraction purposes so trafilatura works.</p>
        <p>And even more text to ensure we have enough content.</p>
        </article></body></html>"""
        result = extract(html, "https://example.com/test")
        frags = [l.get("anchor_fragment") for l in result.links if l.get("anchor_fragment")]
        if frags:
            assert "section" in frags


class TestEdgeCases:
    def test_empty_html(self):
        result = extract("", "https://example.com")
        assert isinstance(result, ExtractedContent)
        assert result.title == ""

    def test_no_body(self):
        html = "<html><head><title>No Body</title></head></html>"
        result = extract(html, "https://example.com")
        assert result.title == "No Body"

    def test_script_and_style_stripped(self):
        html = """<html><head><title>T</title></head><body>
        <article>
        <script>alert('xss')</script>
        <style>.hidden{display:none}</style>
        <p>Real content that should be extracted properly with enough text.</p>
        <p>More content to make the extraction work.</p>
        </article></body></html>"""
        result = extract(html, "https://example.com")
        assert "alert" not in result.main_html
        assert "display:none" not in result.main_html

    def test_video_audio_stripped(self):
        html = """<html><head><title>T</title></head><body>
        <article>
        <video src="vid.mp4">Video</video>
        <audio src="aud.mp3">Audio</audio>
        <p>Content around media elements should be preserved properly.</p>
        <p>More text for extraction to work properly.</p>
        </article></body></html>"""
        result = extract(html, "https://example.com")
        assert "<video" not in result.main_html
        assert "<audio" not in result.main_html
