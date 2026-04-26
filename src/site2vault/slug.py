"""URL/title to filename mapping and collision handling.

Every URL gets exactly one filename for the lifetime of the run.
"""

import hashlib
import re
import unicodedata
from urllib.parse import urlparse

# Characters forbidden in Obsidian filenames (also Windows-safe)
FORBIDDEN_CHARS = re.compile(r'[:/\\|?*"<>#\^\[\]]')
WHITESPACE_RUN = re.compile(r"\s+")
MAX_FILENAME_LEN = 120


def sanitize(title: str) -> str:
    """Sanitize a page title for use as a filename.

    - Unicode NFKC normalize.
    - Remove forbidden chars.
    - Collapse whitespace.
    - Strip leading/trailing dots and spaces.
    - Truncate to 120 chars.
    """
    title = unicodedata.normalize("NFKC", title)
    title = FORBIDDEN_CHARS.sub("", title)
    title = WHITESPACE_RUN.sub(" ", title)
    title = title.strip(". ")
    title = title[:MAX_FILENAME_LEN]
    return title


def slugify(s: str) -> str:
    """Slugify a string for use as a filename.

    - ASCII-fold where possible.
    - Lowercase.
    - Replace non-alphanumeric runs with single hyphens.
    - Trim leading/trailing hyphens.
    """
    # ASCII-fold: decompose then strip combining marks
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = s.strip("-")
    return s


def url_hash(url: str) -> str:
    """Return the hex SHA-1 of a URL."""
    return hashlib.sha1(url.encode("utf-8")).hexdigest()


def last_path_segment(url: str) -> str:
    """Extract the last non-empty path segment from a URL."""
    path = urlparse(url).path.rstrip("/")
    if not path or path == "/":
        return ""
    return path.rsplit("/", 1)[-1]


def assign_filename(
    url: str,
    title: str | None,
    existing_filenames: set[str],
) -> str:
    """Assign a unique filename for a URL.

    Args:
        url: The canonical URL.
        title: The page title (may be None).
        existing_filenames: Set of filenames already assigned.

    Returns:
        A unique filename string (no .md extension).
    """
    if title:
        base = sanitize(title)
    else:
        segment = last_path_segment(url)
        base = slugify(segment) if segment else ""

    if not base:
        base = slugify(url_hash(url)[:8])

    candidate = base
    if candidate not in existing_filenames:
        return candidate

    # Collision: append short hash of full URL
    suffix = url_hash(url)[:6]
    return f"{base}-{suffix}"


def url_to_folder_path(url: str, seed_url: str) -> str:
    """Derive the folder path for a note from its URL path relative to the seed.

    Returns a string like "docs/api" (no leading/trailing slashes).
    Returns "" for root-level pages.
    """
    parsed = urlparse(url)
    path_parts = [p for p in parsed.path.strip("/").split("/") if p]

    # Remove the last segment (that's the page itself)
    if path_parts:
        path_parts = path_parts[:-1]

    return "/".join(slugify(p) for p in path_parts)
