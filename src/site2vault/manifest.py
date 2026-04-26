"""Vault manifest builder.

Emits a single machine-readable JSON manifest at .site2vault/manifest.json
listing every note with metadata. Designed for consumption by Claude Code
and similar agentic coding tools.

Token estimation heuristic: word_count * 1.33. This approximates the
typical BPE tokenization ratio for English prose. It is intentionally
simple — actual token counts vary by model and content (code vs. prose),
but this is close enough for budget estimation.
"""

import json
import logging
from datetime import datetime, timezone
from pathlib import Path

from site2vault.config import RunConfig
from site2vault.convert import load_headings, load_link_index
from site2vault.state import StateDB

log = logging.getLogger("site2vault.manifest")


def build_manifest(config: RunConfig, db: StateDB) -> dict:
    """Build the vault manifest dict.

    Args:
        config: Run configuration.
        db: State database with crawl results.

    Returns:
        Manifest dict matching the schema_version 1 spec.
    """
    notes = db.get_all_notes()
    meta_dir = config.out / "log"

    # Build note entries
    note_entries = []
    total_word_count = 0

    # Build URL-to-file map for resolving outbound internal links
    url_to_file = {}
    for note in notes:
        folder = note.get("folder_path") or ""
        fn = note["filename"]
        file_path = f"{folder}/{fn}.md" if folder else f"{fn}.md"
        url_to_file[note["url"]] = file_path

    # Also map redirect sources to their target files
    for note in notes:
        rows = db.conn.execute(
            "SELECT from_url FROM redirects WHERE to_url = ?", (note["url"],)
        ).fetchall()
        for row in rows:
            url_to_file[row[0]] = url_to_file.get(note["url"], "")

    for note in notes:
        folder = note.get("folder_path") or ""
        fn = note["filename"]
        file_path = f"{folder}/{fn}.md" if folder else f"{fn}.md"

        # Read note content for word count
        if folder:
            note_path = config.out / folder / f"{fn}.md"
        else:
            note_path = config.out / f"{fn}.md"

        word_count = 0
        if note_path.exists():
            content = note_path.read_text(encoding="utf-8")
            # Strip frontmatter for word count
            body = _strip_frontmatter(content)
            word_count = len(body.split())

        total_word_count += word_count
        estimated_tokens = round(word_count * 1.33)

        # Load headings
        headings = load_headings(meta_dir, fn)

        # Load link index and resolve outbound links
        link_index = load_link_index(meta_dir, fn)
        internal_links, external_links = _resolve_outbound_links(
            link_index, note["url"], url_to_file, config.seed_url,
        )

        entry = {
            "file": file_path,
            "url": note["url"],
            "title": note.get("title") or fn,
            "folder": folder,
            "headings": headings,
            "outbound_internal_links": sorted(set(internal_links)),
            "outbound_external_links": sorted(set(external_links)),
            "word_count": word_count,
            "estimated_tokens": estimated_tokens,
            "content_hash": note.get("content_hash") or "",
        }
        note_entries.append(entry)

    # Stats from frontier
    counts = db.count_by_status()

    manifest = {
        "schema_version": 1,
        "seed_url": config.seed_url,
        "crawled_at": datetime.now(timezone.utc).isoformat(),
        "site2vault_version": "0.1.0",
        "stats": {
            "note_count": len(notes),
            "total_word_count": total_word_count,
            "estimated_total_tokens": round(total_word_count * 1.33),
            "failed_url_count": counts.get("failed", 0),
            "skipped_url_count": counts.get("skipped", 0),
        },
        "notes": note_entries,
    }

    return manifest


def write_manifest(config: RunConfig, manifest: dict) -> None:
    """Write manifest to .site2vault/manifest.json."""
    manifest_dir = config.out / ".site2vault"
    manifest_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = manifest_dir / "manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    log.info("Manifest written: %s (%d notes)", manifest_path, len(manifest["notes"]))


def _strip_frontmatter(content: str) -> str:
    """Strip YAML frontmatter from note content."""
    if content.startswith("---"):
        end = content.find("---", 3)
        if end != -1:
            return content[end + 3:].strip()
    return content


def _resolve_outbound_links(
    link_index: dict,
    source_url: str,
    url_to_file: dict[str, str],
    seed_url: str,
) -> tuple[list[str], list[str]]:
    """Resolve link index entries into internal and external link lists.

    Returns:
        Tuple of (internal_file_paths, external_urls).
    """
    from urllib.parse import urljoin
    from site2vault.canonical import canonicalize

    internal = []
    external = []

    for _token, entry in link_index.items():
        if isinstance(entry, dict):
            original_url = entry["url"]
        else:
            original_url = entry

        # Resolve relative URL
        absolute_url = urljoin(source_url, original_url)

        # Strip fragment
        if "#" in absolute_url:
            absolute_url = absolute_url.rsplit("#", 1)[0]

        canonical = canonicalize(absolute_url, seed_url)
        target_file = url_to_file.get(canonical)

        if target_file:
            internal.append(target_file)
        else:
            external.append(absolute_url)

    return internal, external
