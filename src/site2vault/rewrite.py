"""Second-pass link rewriter - the core of the app.

Replaces S2V_LINK_<n> placeholder tokens in notes with proper
Obsidian wikilinks or external markdown links.
"""

import logging
import re
from pathlib import Path
from urllib.parse import urljoin

from site2vault.canonical import canonicalize
from site2vault.config import RunConfig
from site2vault.convert import (
    PLACEHOLDER_PREFIX,
    heading_slug,
    load_headings,
    load_link_index,
)
from site2vault.state import StateDB

log = logging.getLogger("site2vault.rewrite")

# Pattern to match markdown links with placeholder tokens: [display text](S2V_LINK_N)
MD_LINK_PATTERN = re.compile(r"\[([^\]]*)\]\(S2V_LINK_(\d+)\)")

# Pattern for bare placeholder tokens (not inside a markdown link)
BARE_PLACEHOLDER = re.compile(r"(?<!\]\()S2V_LINK_\d+")


def rewrite_all(config: RunConfig, db: StateDB) -> None:
    """Rewrite all placeholder links in the vault.

    This is idempotent: running it twice produces identical output.
    """
    notes = db.get_all_notes()
    if not notes:
        log.info("No notes to rewrite.")
        return

    meta_dir = config.out / "log"

    # Build lookup maps
    url_to_note = {n["url"]: n for n in notes}

    # Also map redirects to their targets
    for note in notes:
        url = note["url"]
        rows = db.conn.execute(
            "SELECT from_url FROM redirects WHERE to_url = ?", (url,)
        ).fetchall()
        for row in rows:
            url_to_note[row[0]] = note

    # Build filename uniqueness map
    filename_counts: dict[str, int] = {}
    for note in notes:
        fn = note["filename"]
        filename_counts[fn] = filename_counts.get(fn, 0) + 1

    # Build heading maps for each note
    note_headings: dict[str, list[dict]] = {}
    for note in notes:
        note_headings[note["filename"]] = load_headings(meta_dir, note["filename"])

    rewritten_count = 0

    for note in notes:
        filename = note["filename"]
        folder_path = note["folder_path"] or ""
        source_url = note["url"]

        # Load link index
        link_index = load_link_index(meta_dir, filename)
        if not link_index:
            continue

        # Read note file
        if folder_path:
            note_path = config.out / folder_path / f"{filename}.md"
        else:
            note_path = config.out / f"{filename}.md"

        if not note_path.exists():
            log.warning("Note file missing: %s", note_path)
            continue

        content = note_path.read_text(encoding="utf-8")

        # Check if there are any placeholders to replace
        if PLACEHOLDER_PREFIX not in content:
            continue

        # Replace [display](S2V_LINK_N) patterns with proper links
        def replace_md_link(match: re.Match) -> str:
            display_text = match.group(1)
            token_num = match.group(2)
            token = f"{PLACEHOLDER_PREFIX}{token_num}"

            entry = link_index.get(token)
            if entry is None:
                return match.group(0)

            # Support both old format (str) and new format (dict)
            if isinstance(entry, dict):
                original_url = entry["url"]
                original_text = entry.get("text", display_text)
            else:
                original_url = entry
                original_text = display_text

            # Use original link text if markdownify mangled the display
            if not display_text or display_text == token:
                display_text = original_text

            # Cap display text length to avoid absurd wikilinks
            if len(display_text) > 100:
                display_text = display_text[:97] + "..."

            # Resolve relative URL
            absolute_url = urljoin(source_url, original_url)

            # Separate fragment
            fragment = None
            if "#" in absolute_url:
                absolute_url, fragment = absolute_url.rsplit("#", 1)

            canonical = canonicalize(absolute_url, config.seed_url)

            # Check if this URL maps to a note
            target_note = url_to_note.get(canonical)
            if target_note and target_note.get("status") == "done":
                return _format_wikilink(
                    target_note, fragment, display_text,
                    note_headings, filename_counts, config.link_style,
                )
            else:
                # External or failed link - standard markdown link
                full_url = absolute_url
                if fragment:
                    full_url += f"#{fragment}"
                if display_text:
                    return f"[{display_text}]({full_url})"
                else:
                    return f"[{full_url}]({full_url})"

        new_content = MD_LINK_PATTERN.sub(replace_md_link, content)

        # Ensure spaces around wikilinks and markdown links
        # Fix "word[[" -> "word [[" and "]]word" -> "]] word"
        new_content = re.sub(r'(\w)\[\[', r'\1 [[', new_content)
        new_content = re.sub(r'\]\](\w)', r']] \1', new_content)
        # Fix "word[text](url)" -> "word [text](url)"
        new_content = re.sub(r'(\w)\[([^\]]+)\]\(http', r'\1 [\2](http', new_content)
        # Fix "](url)word" -> "](url) word" (markdown link followed by word)
        new_content = re.sub(r'\]\(([^)]+)\)(\w)', r'](\1) \2', new_content)

        # Clean up any remaining bare placeholder tokens
        new_content = BARE_PLACEHOLDER.sub("", new_content)

        if new_content != content:
            note_path.write_text(new_content, encoding="utf-8")
            rewritten_count += 1

    log.info("Rewritten links in %d notes", rewritten_count)


def _format_wikilink(
    target_note: dict,
    fragment: str | None,
    display_text: str,
    note_headings: dict[str, list[dict]],
    filename_counts: dict[str, int],
    link_style: str,
) -> str:
    """Format an Obsidian wikilink to a target note."""
    filename = target_note["filename"]
    folder_path = target_note.get("folder_path", "")

    # Determine wikilink target
    if link_style == "shortest" and filename_counts.get(filename, 0) <= 1:
        target = filename
    else:
        if folder_path:
            target = f"{folder_path}/{filename}"
        else:
            target = filename

    # Resolve anchor
    anchor = None
    if fragment:
        headings = note_headings.get(filename, [])
        anchor = _resolve_anchor(fragment, headings)

    if anchor:
        target = f"{target}#{anchor}"

    # Use alias form if display text differs from target
    if display_text and display_text != target and display_text != filename:
        return f"[[{target}|{display_text}]]"
    return f"[[{target}]]"


def _resolve_anchor(fragment: str, headings: list[dict]) -> str | None:
    """Resolve a web anchor fragment to an Obsidian heading text."""
    if not fragment or not headings:
        return None

    # Exact ID match
    for h in headings:
        if h.get("slug") == fragment:
            return h["text"]

    # Try slugifying the fragment and matching
    frag_slug = heading_slug(fragment)
    for h in headings:
        if h.get("slug") == frag_slug:
            return h["text"]

    log.debug("Unresolved anchor: #%s", fragment)
    return None
