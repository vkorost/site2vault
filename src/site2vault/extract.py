"""Content extraction from HTML.

Uses trafilatura for main-content isolation with BS4 fallback.
Strips all images, returns structured payload with headings and links.
"""

import logging
import re
from dataclasses import dataclass, field

from bs4 import BeautifulSoup, Tag

log = logging.getLogger("site2vault.extract")

# Elements to strip entirely
STRIP_ELEMENTS = {
    "img", "picture", "svg", "video", "audio", "canvas",
    "iframe", "object", "embed", "noscript",
}

# Elements that are media containers - strip if they only contain media
MEDIA_CONTAINER_ELEMENTS = {"figure"}


@dataclass
class ExtractedContent:
    title: str
    main_html: str
    headings: list[dict] = field(default_factory=list)
    links: list[dict] = field(default_factory=list)
    lang: str | None = None
    published: str | None = None
    author: str | None = None
    description: str | None = None


def extract(html: str, url: str, strip_boilerplate: bool = True) -> ExtractedContent:
    """Extract content from HTML, stripping images and boilerplate.

    Args:
        html: Raw HTML string.
        url: Source URL (for metadata context).

    Returns:
        ExtractedContent with cleaned HTML, headings, links, metadata.
    """
    soup = BeautifulSoup(html, "lxml")
    metadata = _extract_metadata(soup)
    title = _extract_title(soup)

    # Pre-process: expand tabbed UI into labeled sections
    preprocessed_html = _expand_tabs(html)

    # Pre-process: convert figcaptions to <p> before trafilatura eats them
    preprocessed_html = _preprocess_figcaptions(preprocessed_html)

    # Try trafilatura first
    main_html = _trafilatura_extract(preprocessed_html)

    # Fallback if trafilatura returns nothing useful
    if not main_html or len(main_html.strip()) < 50:
        log.debug("Trafilatura returned insufficient content, falling back to BS4")
        main_html = _bs4_fallback(soup)

    # Static boilerplate stripping (Stage 1)
    if strip_boilerplate:
        from site2vault.boilerplate import strip_static_boilerplate
        main_html = strip_static_boilerplate(main_html)

    # Parse the extracted HTML, strip images, extract headings and links
    content_soup = BeautifulSoup(main_html, "lxml")
    _strip_media(content_soup)
    _preserve_figcaptions(content_soup)

    headings = _extract_headings(content_soup)
    links = _extract_links(content_soup)
    clean_html = _inner_html(content_soup)

    return ExtractedContent(
        title=title,
        main_html=clean_html,
        headings=headings,
        links=links,
        lang=metadata.get("lang"),
        published=metadata.get("published"),
        author=metadata.get("author"),
        description=metadata.get("description"),
    )


def _expand_tabs(html: str) -> str:
    """Expand tabbed UI components into labeled sections.

    Finds role="tablist" + role="tabpanel" patterns and replaces them with
    structured HTML where each tab's content appears under its label as a heading.
    This ensures ALL tab content is captured, not just the active tab.

    Processes innermost tab groups first to handle nesting correctly.
    """
    soup = BeautifulSoup(html, "lxml")
    modified = False

    # Process repeatedly until no more tab groups remain
    while True:
        tablists = soup.find_all(attrs={"role": "tablist"})
        if not tablists:
            break

        # Find a tablist whose tabs have matching tabpanels
        processed_any = False
        for tablist in tablists:
            tabs = tablist.find_all(attrs={"role": "tab"})
            if not tabs:
                continue

            # Collect tab info with aria-controls IDs
            tab_infos = []
            for tab in tabs:
                label = tab.get_text(strip=True)
                controls_id = tab.get("aria-controls", "")
                tab_infos.append({"label": label, "controls_id": controls_id})

            # Find matching tabpanels by ID anywhere in the document
            matched_sections = []
            for tab_info in tab_infos:
                panel = None
                if tab_info["controls_id"]:
                    panel = soup.find(id=tab_info["controls_id"])
                if panel is None:
                    # Fallback: find by aria-labelledby matching
                    # Extract the label key from controls_id (e.g., "panel-terminal-0" -> "terminal")
                    parts = tab_info["controls_id"].replace("panel-", "").rsplit("-", 1)
                    if parts:
                        label_key = parts[0]
                        panel = soup.find(attrs={"role": "tabpanel", "aria-labelledby": label_key})

                if panel is not None:
                    matched_sections.append((tab_info["label"], panel))

            if not matched_sections:
                continue

            # Build replacement HTML
            replacement_parts = []
            for label, panel_el in matched_sections:
                header = soup.new_tag("h4")
                header.string = label
                replacement_parts.append(header)

                content_div = soup.new_tag("div")
                for child in list(panel_el.children):
                    content_div.append(child.extract())
                replacement_parts.append(content_div)

            # Insert after tablist
            insert_point = tablist
            for part in replacement_parts:
                insert_point.insert_after(part)
                insert_point = part

            # Remove original tablist and panels
            tablist.decompose()
            for _, panel_el in matched_sections:
                if panel_el.parent:
                    panel_el.decompose()

            processed_any = True
            modified = True
            break  # Restart loop since DOM changed

        if not processed_any:
            # Remaining tablists have no matching panels, remove them
            for tl in tablists:
                tl.decompose()
            modified = True
            break

    if modified:
        return str(soup)
    return html


def _preprocess_figcaptions(html: str) -> str:
    """Convert figcaptions to <p> tags and unwrap figures before trafilatura strips them."""
    soup = BeautifulSoup(html, "lxml")
    for figure in soup.find_all("figure"):
        # Extract figcaption text as <p> before trafilatura removes the whole figure
        replacement_parts = []
        for figcaption in figure.find_all("figcaption"):
            text = figcaption.get_text(strip=True)
            if text:
                new_p = soup.new_tag("p")
                new_p.string = text
                replacement_parts.append(new_p)
        # Replace figure with just the caption paragraphs
        if replacement_parts:
            for part in replacement_parts:
                figure.insert_before(part)
        figure.decompose()
    return str(soup)


def _extract_title(soup: BeautifulSoup) -> str:
    """Extract page title from <title> or <h1>."""
    title_tag = soup.find("title")
    if title_tag and title_tag.string:
        return title_tag.string.strip()
    h1 = soup.find("h1")
    if h1:
        return h1.get_text(strip=True)
    return ""


def _trafilatura_extract(html: str) -> str:
    """Run trafilatura extraction returning HTML."""
    try:
        import trafilatura

        result = trafilatura.extract(
            html,
            output_format="html",
            include_links=True,
            include_images=False,
            include_tables=True,
        )
        return result or ""
    except Exception as e:
        log.warning("Trafilatura extraction failed: %s", e)
        return ""


def _bs4_fallback(soup: BeautifulSoup) -> str:
    """Fallback content extraction using BS4 heuristics."""
    # Try <article> first
    article = soup.find("article")
    if article:
        return str(article)

    # Try <main>
    main = soup.find("main")
    if main:
        return str(main)

    # Find the largest <div> by text density
    body = soup.find("body")
    if not body:
        return str(soup)

    best_div = None
    best_text_len = 0

    for div in body.find_all("div", recursive=True):
        text_len = len(div.get_text(strip=True))
        if text_len > best_text_len:
            best_text_len = text_len
            best_div = div

    if best_div and best_text_len > 100:
        return str(best_div)

    return str(body)


def _strip_media(soup: BeautifulSoup) -> None:
    """Remove all media elements in-place."""
    for tag_name in STRIP_ELEMENTS:
        for el in soup.find_all(tag_name):
            el.decompose()

    # Strip script, style, form
    for tag_name in ("script", "style", "form"):
        for el in soup.find_all(tag_name):
            el.decompose()

    # Strip figures that only contained images (now empty after media strip)
    for figure in soup.find_all("figure"):
        # Check if figure has any remaining meaningful content besides figcaption
        has_content = False
        for child in figure.children:
            if isinstance(child, Tag):
                if child.name == "figcaption":
                    has_content = True
                elif child.get_text(strip=True):
                    has_content = True
            elif hasattr(child, "strip") and child.strip():
                has_content = True
        if not has_content:
            figure.decompose()


def _preserve_figcaptions(soup: BeautifulSoup) -> None:
    """Unwrap figcaptions from figures, preserving their text as paragraphs."""
    for figcaption in soup.find_all("figcaption"):
        # Replace figcaption with a <p> containing its text
        text = figcaption.get_text(strip=True)
        if text:
            new_p = soup.new_tag("p")
            new_p.string = text
            figcaption.replace_with(new_p)
        else:
            figcaption.decompose()


def _extract_headings(soup: BeautifulSoup) -> list[dict]:
    """Extract all headings with level, text, and id."""
    headings = []
    for level in range(1, 7):
        for h in soup.find_all(f"h{level}"):
            text = h.get_text(strip=True)
            if text:
                headings.append({
                    "level": level,
                    "text": text,
                    "id": h.get("id"),
                })
    # Sort by position in document (find_all returns in document order per level,
    # but we need cross-level ordering)
    # Re-extract in document order
    headings = []
    for h in soup.find_all(re.compile(r"^h[1-6]$")):
        text = h.get_text(strip=True)
        if text:
            level = int(h.name[1])
            headings.append({
                "level": level,
                "text": text,
                "id": h.get("id"),
            })
    return headings


def _extract_links(soup: BeautifulSoup) -> list[dict]:
    """Extract all <a href> links from the content."""
    links = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        text = a.get_text(strip=True)
        # Separate fragment
        fragment = None
        if "#" in href:
            _, fragment = href.rsplit("#", 1)
        links.append({
            "href": href,
            "text": text,
            "anchor_fragment": fragment,
        })
    return links


def _extract_metadata(soup: BeautifulSoup) -> dict:
    """Extract metadata from meta tags, OpenGraph, JSON-LD."""
    meta = {}

    # Language
    html_tag = soup.find("html")
    if html_tag and html_tag.get("lang"):
        meta["lang"] = html_tag["lang"]

    # OpenGraph / Twitter Card
    for tag in soup.find_all("meta"):
        prop = tag.get("property", "") or tag.get("name", "")
        content = tag.get("content", "")
        prop_lower = prop.lower()

        if prop_lower in ("og:author", "author", "dc.creator", "twitter:creator"):
            meta.setdefault("author", content)
        elif prop_lower in ("article:published_time", "dc.date", "date"):
            meta.setdefault("published", content)
        elif prop_lower in ("og:description", "description", "twitter:description"):
            meta.setdefault("description", content)

    # JSON-LD
    for script in soup.find_all("script", type="application/ld+json"):
        try:
            import json
            data = json.loads(script.string or "")
            if isinstance(data, dict):
                if "author" in data:
                    author = data["author"]
                    if isinstance(author, dict):
                        meta.setdefault("author", author.get("name", ""))
                    elif isinstance(author, str):
                        meta.setdefault("author", author)
                if "datePublished" in data:
                    meta.setdefault("published", data["datePublished"])
        except (json.JSONDecodeError, TypeError):
            pass

    return meta


def _inner_html(soup: BeautifulSoup) -> str:
    """Get the inner HTML content, stripping the outer html/body tags."""
    body = soup.find("body")
    if body:
        return body.decode_contents()
    return soup.decode_contents()
