"""Index / MOC note generation.

Generates Index.md at vault root and per-folder indexes.
"""

import logging
from collections import defaultdict
from datetime import datetime, timezone

import yaml

from site2vault.config import RunConfig
from site2vault.state import StateDB

log = logging.getLogger("site2vault.index")


def generate_index(config: RunConfig, db: StateDB) -> None:
    """Generate Index.md MOC at vault root and per-folder indexes."""
    notes = db.get_all_notes()
    if not notes:
        log.info("No notes for index generation.")
        return

    # Group notes by folder
    by_folder: dict[str, list[dict]] = defaultdict(list)
    for note in notes:
        folder = note.get("folder_path", "") or ""
        by_folder[folder].append(note)

    from urllib.parse import urlparse
    seed_host = urlparse(config.seed_url).hostname or "site"
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    total_notes = len(notes)

    # Root Index.md
    _write_root_index(config, seed_host, timestamp, total_notes, by_folder)

    # Per-folder indexes
    for folder, folder_notes in by_folder.items():
        if folder:
            _write_folder_index(config, folder, folder_notes)

    log.info("Generated index with %d notes", total_notes)


def _write_root_index(
    config: RunConfig,
    seed_host: str,
    timestamp: str,
    total_notes: int,
    by_folder: dict[str, list[dict]],
) -> None:
    """Write the root Index.md."""
    fm = {
        "title": f"{seed_host} (mirrored by site2vault)",
        "source_url": config.seed_url,
    }
    yaml_str = yaml.dump(fm, default_flow_style=False, allow_unicode=True, sort_keys=False)

    lines = [
        f"---\n{yaml_str}---\n",
        f"# {seed_host}\n",
        f"Mirrored from {config.seed_url} on {timestamp}. {total_notes} notes.\n",
    ]

    # Top-level sections (non-root folders)
    folders = sorted(f for f in by_folder if f)
    if folders:
        lines.append("## Top-level sections\n")
        for folder in folders:
            section = folder.split("/")[0]
            lines.append(f"- [[{folder}/Index|{section}]]\n")
        lines.append("")

    # All notes
    lines.append("## All notes\n")
    for folder in sorted(by_folder):
        if folder:
            lines.append(f"### {folder}\n")
        for note in sorted(by_folder[folder], key=lambda n: n["filename"]):
            fn = note["filename"]
            title = note.get("title") or fn
            if folder:
                lines.append(f"- [[{folder}/{fn}|{title}]]\n")
            else:
                lines.append(f"- [[{fn}|{title}]]\n")
        lines.append("")

    content = "\n".join(lines)
    index_path = config.out / "Index.md"
    index_path.write_text(content, encoding="utf-8")


def _write_folder_index(
    config: RunConfig,
    folder: str,
    notes: list[dict],
) -> None:
    """Write an Index.md for a folder."""
    fm = {
        "title": f"{folder} index",
    }
    yaml_str = yaml.dump(fm, default_flow_style=False, allow_unicode=True, sort_keys=False)

    lines = [
        f"---\n{yaml_str}---\n",
        f"# {folder}\n",
    ]

    for note in sorted(notes, key=lambda n: n["filename"]):
        fn = note["filename"]
        title = note.get("title") or fn
        lines.append(f"- [[{fn}|{title}]]\n")

    content = "\n".join(lines)
    folder_path = config.out / folder
    folder_path.mkdir(parents=True, exist_ok=True)
    index_path = folder_path / "Index.md"
    index_path.write_text(content, encoding="utf-8")
