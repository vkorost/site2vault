"""Heading-level chunking metadata.

Computes byte offsets for each heading section in the final written
Markdown file (post-rewrite). This allows Claude Code to read a single
section without loading the whole file.

Must run after Phase 2 (rewrite) since rewriting changes file content.
"""

import json
import logging
import re
from pathlib import Path

log = logging.getLogger("site2vault.chunking")

HEADING_RE = re.compile(r"^(#{1,6})\s+(.+)$", re.MULTILINE)


def compute_heading_offsets(
    notes: list[dict],
    vault_dir: Path,
    meta_dir: Path,
) -> int:
    """Compute byte offsets for heading sections in all notes.

    Reads each final .md file, finds heading positions, and updates
    the headings sidecar JSON with start_byte/end_byte.

    A section starts at its heading line and ends at the next heading
    of equal or lesser level, or EOF.

    Args:
        notes: List of note dicts from the DB.
        vault_dir: Path to vault directory.
        meta_dir: Path to log/meta directory.

    Returns:
        Number of notes processed.
    """
    processed = 0

    for note in notes:
        folder = note.get("folder_path") or ""
        fn = note["filename"]

        if folder:
            note_path = vault_dir / folder / f"{fn}.md"
        else:
            note_path = vault_dir / f"{fn}.md"

        if not note_path.exists():
            continue

        content_bytes = note_path.read_bytes()
        content_text = content_bytes.decode("utf-8")

        headings = _find_headings_with_offsets(content_text, content_bytes)

        if headings:
            _save_headings_with_offsets(headings, meta_dir, fn)
            processed += 1

    log.info("Computed heading offsets for %d notes", processed)
    return processed


def _find_headings_with_offsets(
    text: str,
    raw_bytes: bytes,
) -> list[dict]:
    """Find all headings and compute their byte offsets.

    Each section starts at the heading line and ends at the next heading
    of equal or lesser level, or EOF.
    """
    headings = []

    for match in HEADING_RE.finditer(text):
        level = len(match.group(1))
        heading_text = match.group(2).strip()
        char_start = match.start()

        # Convert character offset to byte offset
        byte_start = len(text[:char_start].encode("utf-8"))

        headings.append({
            "level": level,
            "text": heading_text,
            "slug": _heading_slug(heading_text),
            "start_byte": byte_start,
            "end_byte": 0,  # Will be filled below
        })

    total_bytes = len(raw_bytes)

    # Compute end_byte: next heading of equal or lesser level, or EOF
    for i, h in enumerate(headings):
        end = total_bytes  # Default: EOF
        for j in range(i + 1, len(headings)):
            if headings[j]["level"] <= h["level"]:
                end = headings[j]["start_byte"]
                break
        h["end_byte"] = end

    return headings


def _heading_slug(text: str) -> str:
    """Generate a GitHub-style heading slug."""
    slug = text.lower()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"[\s]+", "-", slug)
    slug = re.sub(r"-+", "-", slug)
    slug = slug.strip("-")
    return slug


def _save_headings_with_offsets(
    headings: list[dict],
    meta_dir: Path,
    filename: str,
) -> None:
    """Save heading data with byte offsets to sidecar JSON."""
    headings_dir = meta_dir / "headings"
    headings_dir.mkdir(parents=True, exist_ok=True)
    path = headings_dir / f"{filename}.json"
    path.write_text(json.dumps(headings, indent=2), encoding="utf-8")
