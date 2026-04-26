"""Boilerplate stripping: static rules and cross-page detection.

Stage 1: Static rule pass — removes known boilerplate elements from HTML
using CSS selectors and trailing text patterns.

Stage 2: Cross-page detection — identifies paragraphs that appear in >50%
of notes (configurable) and removes them. Auto-disabled below 20 notes.
"""

import hashlib
import logging
import re
from collections import Counter

from bs4 import BeautifulSoup

from site2vault.boilerplate_patterns import CSS_SELECTORS, TRAILING_TEXT_PATTERNS

log = logging.getLogger("site2vault.boilerplate")


def strip_static_boilerplate(html: str) -> str:
    """Stage 1: Remove known boilerplate elements from extracted HTML.

    Runs after trafilatura extraction, before markdown conversion.

    Args:
        html: Extracted HTML content.

    Returns:
        Cleaned HTML with boilerplate elements removed.
    """
    soup = BeautifulSoup(html, "lxml")
    removed = 0

    # Apply CSS selectors
    for selector in CSS_SELECTORS:
        try:
            for el in soup.select(selector):
                el.decompose()
                removed += 1
        except Exception:
            # Invalid selector or parsing issue — skip silently
            pass

    # Strip trailing paragraphs matching known patterns
    patterns = [re.compile(p, re.IGNORECASE) for p in TRAILING_TEXT_PATTERNS]
    for p_tag in soup.find_all("p"):
        text = p_tag.get_text(strip=True)
        if any(pat.search(text) for pat in patterns):
            p_tag.decompose()
            removed += 1

    if removed:
        log.debug("Static boilerplate: removed %d elements", removed)

    body = soup.find("body")
    if body:
        return body.decode_contents()
    return soup.decode_contents()


def detect_cross_page_boilerplate(
    notes: list[dict],
    vault_dir,
    threshold: float = 0.5,
) -> set[str]:
    """Stage 2: Detect paragraphs that appear in >threshold fraction of notes.

    Args:
        notes: List of note dicts with 'filename' and 'folder_path'.
        vault_dir: Path to vault directory.
        threshold: Fraction of notes a paragraph must appear in to be flagged.

    Returns:
        Set of paragraph hashes flagged as boilerplate.
    """
    from pathlib import Path

    if len(notes) < 20:
        log.info("Cross-page boilerplate: skipped (only %d notes, need >=20)", len(notes))
        return set()

    para_counts: Counter = Counter()
    total_notes = 0

    for note in notes:
        folder = note.get("folder_path") or ""
        fn = note["filename"]
        if folder:
            path = Path(vault_dir) / folder / f"{fn}.md"
        else:
            path = Path(vault_dir) / f"{fn}.md"

        if not path.exists():
            continue

        content = path.read_text(encoding="utf-8")
        body = _strip_frontmatter(content)

        # Extract paragraphs outside code blocks
        paragraphs = _extract_paragraphs(body)

        # Deduplicate within a single note (same paragraph appearing twice
        # in one note shouldn't count double)
        note_hashes = set()
        for para in paragraphs:
            h = _hash_paragraph(para)
            note_hashes.add(h)

        for h in note_hashes:
            para_counts[h] += 1

        total_notes += 1

    if total_notes == 0:
        return set()

    # Flag paragraphs exceeding threshold
    cutoff = threshold * total_notes
    flagged = {h for h, count in para_counts.items() if count >= cutoff}

    if flagged:
        log.info("Cross-page boilerplate: flagged %d paragraph patterns (threshold=%.0f%%)",
                 len(flagged), threshold * 100)

    return flagged


def remove_cross_page_boilerplate(
    notes: list[dict],
    vault_dir,
    flagged_hashes: set[str],
) -> int:
    """Remove flagged boilerplate paragraphs from all notes.

    Args:
        notes: List of note dicts.
        vault_dir: Path to vault directory.
        flagged_hashes: Set of paragraph hashes to remove.

    Returns:
        Number of notes modified.
    """
    from pathlib import Path

    if not flagged_hashes:
        return 0

    modified = 0

    for note in notes:
        folder = note.get("folder_path") or ""
        fn = note["filename"]
        if folder:
            path = Path(vault_dir) / folder / f"{fn}.md"
        else:
            path = Path(vault_dir) / f"{fn}.md"

        if not path.exists():
            continue

        content = path.read_text(encoding="utf-8")

        # Split into frontmatter and body
        fm, body = _split_frontmatter(content)

        # Remove flagged paragraphs
        new_body = _remove_flagged_paragraphs(body, flagged_hashes)

        if new_body != body:
            path.write_text(fm + new_body, encoding="utf-8")
            modified += 1

    if modified:
        log.info("Cross-page boilerplate: cleaned %d notes", modified)

    return modified


def _strip_frontmatter(content: str) -> str:
    """Strip YAML frontmatter from content."""
    if content.startswith("---"):
        end = content.find("---", 3)
        if end != -1:
            return content[end + 3:].strip()
    return content


def _split_frontmatter(content: str) -> tuple[str, str]:
    """Split content into (frontmatter_with_delimiters, body)."""
    if content.startswith("---"):
        end = content.find("---", 3)
        if end != -1:
            return content[:end + 3] + "\n", content[end + 3:]
    return "", content


def _extract_paragraphs(body: str) -> list[str]:
    """Extract paragraph texts from markdown, excluding code blocks."""
    lines = body.split("\n")
    paragraphs = []
    in_code_block = False
    current_para = []

    for line in lines:
        stripped = line.strip()

        # Toggle code block state
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            if current_para:
                paragraphs.append(" ".join(current_para))
                current_para = []
            continue

        if in_code_block:
            continue

        # Skip headings
        if stripped.startswith("#"):
            if current_para:
                paragraphs.append(" ".join(current_para))
                current_para = []
            continue

        # Blank line ends paragraph
        if not stripped:
            if current_para:
                paragraphs.append(" ".join(current_para))
                current_para = []
            continue

        current_para.append(stripped)

    if current_para:
        paragraphs.append(" ".join(current_para))

    return [p for p in paragraphs if len(p) >= 10]  # Ignore very short fragments


def _hash_paragraph(text: str) -> str:
    """Hash a paragraph after normalizing whitespace."""
    normalized = " ".join(text.split()).lower()
    return hashlib.sha256(normalized.encode()).hexdigest()[:16]


def _remove_flagged_paragraphs(body: str, flagged: set[str]) -> str:
    """Remove paragraphs whose hashes are in the flagged set."""
    lines = body.split("\n")
    result_lines = []
    in_code_block = False
    current_para_lines = []
    current_para_start = 0

    def flush_para():
        if not current_para_lines:
            return
        text = " ".join(line.strip() for line in current_para_lines)
        h = _hash_paragraph(text)
        if h not in flagged or len(text) < 10:
            result_lines.extend(current_para_lines)

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("```"):
            flush_para()
            current_para_lines = []
            in_code_block = not in_code_block
            result_lines.append(line)
            continue

        if in_code_block:
            result_lines.append(line)
            continue

        if stripped.startswith("#"):
            flush_para()
            current_para_lines = []
            result_lines.append(line)
            continue

        if not stripped:
            flush_para()
            current_para_lines = []
            result_lines.append(line)
            continue

        current_para_lines.append(line)

    flush_para()

    return "\n".join(result_lines)
