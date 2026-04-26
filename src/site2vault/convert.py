"""HTML to markdown conversion with placeholder link tokens.

Strategy: placeholder-then-rewrite. Links are replaced with S2V_LINK_<n> tokens
during conversion, then resolved in the rewrite pass after the full URL map exists.
"""

import json
import logging
import re
from pathlib import Path

from bs4 import BeautifulSoup
from markdownify import markdownify

log = logging.getLogger("site2vault.convert")

PLACEHOLDER_PREFIX = "S2V_LINK_"
PLACEHOLDER_PATTERN = re.compile(r"S2V_LINK_(\d+)")

# Elements to strip during markdown conversion
STRIP_TAGS = ["script", "style", "form", "iframe", "noscript", "svg",
              "img", "picture", "video", "audio", "canvas"]


class ConversionResult:
    """Result of HTML-to-markdown conversion."""

    def __init__(self, markdown: str, link_index: dict[str, str], headings: list[dict]):
        self.markdown = markdown
        self.link_index = link_index  # {token: original_url}
        self.headings = headings  # [{level, text, slug}]


def convert(
    html: str,
    source_url: str,
    headings: list[dict],
) -> ConversionResult:
    """Convert extracted HTML to markdown with placeholder link tokens.

    Args:
        html: Cleaned HTML from the extractor (already image-free).
        source_url: The URL this content was fetched from.
        headings: Headings extracted by extract.py.

    Returns:
        ConversionResult with markdown, link index, and heading data.

    Raises:
        ValueError: If source HTML already contains S2V_LINK_ tokens.
    """
    # Guard against token collision
    if PLACEHOLDER_PREFIX in html:
        raise ValueError(
            f"Source HTML already contains '{PLACEHOLDER_PREFIX}' token. "
            "This would cause silent corruption during link rewriting."
        )

    soup = BeautifulSoup(html, "lxml")

    # Replace all <a> tags with placeholder tokens
    link_index: dict[str, dict] = {}
    counter = 0

    for a_tag in soup.find_all("a", href=True):
        token = f"{PLACEHOLDER_PREFIX}{counter}"
        original_url = a_tag["href"]
        original_text = a_tag.get_text(strip=True)
        # Truncate excessively long link text (e.g., <a> wrapping paragraphs)
        if len(original_text) > 100:
            original_text = original_text[:97] + "..."
        link_index[token] = {"url": original_url, "text": original_text}
        a_tag["href"] = token
        counter += 1

    # Run markdownify
    modified_html = str(soup)
    markdown = markdownify(
        modified_html,
        heading_style="ATX",
        bullets="-",
        strip=STRIP_TAGS,
    )

    # Clean up excessive whitespace
    markdown = _clean_markdown(markdown)

    # Build heading slugs for anchor resolution
    heading_data = _build_heading_data(headings)

    return ConversionResult(
        markdown=markdown,
        link_index=link_index,
        headings=heading_data,
    )


def save_link_index(link_index: dict[str, str], meta_dir: Path, filename: str) -> None:
    """Save link index sidecar JSON."""
    index_dir = meta_dir / "link-index"
    index_dir.mkdir(parents=True, exist_ok=True)
    path = index_dir / f"{filename}.json"
    path.write_text(json.dumps(link_index, indent=2), encoding="utf-8")


def load_link_index(meta_dir: Path, filename: str) -> dict[str, str]:
    """Load link index sidecar JSON."""
    path = meta_dir / "link-index" / f"{filename}.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def save_headings(headings: list[dict], meta_dir: Path, filename: str) -> None:
    """Save heading sidecar JSON."""
    headings_dir = meta_dir / "headings"
    headings_dir.mkdir(parents=True, exist_ok=True)
    path = headings_dir / f"{filename}.json"
    path.write_text(json.dumps(headings, indent=2), encoding="utf-8")


def load_headings(meta_dir: Path, filename: str) -> list[dict]:
    """Load heading sidecar JSON."""
    path = meta_dir / "headings" / f"{filename}.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return []


def heading_slug(text: str) -> str:
    """Generate a GitHub-style heading slug.

    Lowercase, strip non-alphanumerics except spaces and hyphens,
    replace spaces with hyphens, collapse repeat hyphens.
    """
    slug = text.lower()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"[\s]+", "-", slug)
    slug = re.sub(r"-+", "-", slug)
    slug = slug.strip("-")
    return slug


def _build_heading_data(headings: list[dict]) -> list[dict]:
    """Build heading data with slugs for anchor resolution."""
    result = []
    for h in headings:
        result.append({
            "level": h["level"],
            "text": h["text"],
            "slug": heading_slug(h["text"]),
        })
    return result


def _clean_markdown(md: str) -> str:
    """Clean up markdown output from markdownify."""
    # Collapse 3+ consecutive blank lines to 2
    md = re.sub(r"\n{3,}", "\n\n", md)
    # Strip trailing whitespace from lines
    md = "\n".join(line.rstrip() for line in md.split("\n"))
    return md.strip() + "\n"
