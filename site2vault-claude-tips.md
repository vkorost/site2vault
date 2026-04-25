# Site2Vault — How Claude Should Process Captured Data

This guide is for Claude Code (and similar agentic tools) consuming a site2vault vault. It describes the file structure, where to look first, how to navigate efficiently, and how to minimize token usage when working with mirrored documentation.

---

## 1. Start with the Manifest

**Always read `.site2vault/manifest.json` first.** This single file tells you everything about the vault without scanning any notes.

```
<vault>/.site2vault/manifest.json
```

The manifest contains:

```json
{
  "schema_version": 1,
  "seed_url": "https://docs.example.com",
  "crawled_at": "2026-04-24T18:32:11Z",
  "stats": {
    "note_count": 1274,
    "total_word_count": 2450787,
    "estimated_total_tokens": 3259547,
    "failed_url_count": 65,
    "skipped_url_count": 768
  },
  "notes": [
    {
      "file": "api/rest/Endpoints.md",
      "url": "https://docs.example.com/api/rest/endpoints.html",
      "title": "Endpoints",
      "folder": "api/rest",
      "headings": [
        { "level": 2, "text": "Authentication", "slug": "authentication",
          "start_byte": 1240, "end_byte": 4892 }
      ],
      "outbound_internal_links": ["api/rest/Auth.md", "api/Index.md"],
      "outbound_external_links": ["https://oauth.net/2/"],
      "word_count": 1840,
      "estimated_tokens": 2447,
      "content_hash": "a1b2c3d4..."
    }
  ]
}
```

### What you learn from the manifest alone (without reading any notes):

- **Corpus size**: total notes, word count, estimated token budget
- **Every note's file path, URL, title, and folder**
- **Every heading in every note** with byte offsets for section-level reading
- **Link graph**: which notes link to which (internal) and what external URLs are referenced
- **Per-note token estimates**: know which files are cheap vs. expensive to read

---

## 2. Find Content Without Scanning

### 2.1 Find a topic by heading

Search the manifest's `notes[].headings[].text` to locate which note and section covers a topic:

```python
# Pseudo: find all notes with a heading mentioning "authentication"
for note in manifest["notes"]:
    for h in note["headings"]:
        if "authentication" in h["text"].lower():
            print(f'{note["file"]} -> {h["text"]} (bytes {h["start_byte"]}-{h["end_byte"]})')
```

### 2.2 Find a note by URL

Every note has its original `url`. If you know the documentation URL, look it up directly:

```python
note = next(n for n in manifest["notes"] if "endpoints" in n["url"])
```

### 2.3 Find a note by title

Every note has a `title` field. Search it:

```python
notes = [n for n in manifest["notes"] if "quickstart" in n["title"].lower()]
```

### 2.4 Browse by folder structure

Notes are grouped in folders mirroring the site's URL structure. The `folder` field in each note entry tells you its location. To see what's in a section:

```python
api_notes = [n for n in manifest["notes"] if n["folder"].startswith("api/")]
```

---

## 3. Read Only What You Need

### 3.1 Read a single section, not the whole file

Each heading in the manifest includes `start_byte` and `end_byte`. Use these to read just one section of a file without loading the entire note:

```python
# Read only the "Authentication" section (bytes 1240-4892) from a 50KB file
with open("api/rest/Endpoints.md", "rb") as f:
    f.seek(1240)
    section = f.read(4892 - 1240).decode("utf-8")
```

This is the single most important token-saving technique. A 50KB file might have a 2KB section that answers the question.

### 3.2 Check token estimates before reading

Before reading a large file, check its `estimated_tokens` in the manifest:

- < 1,000 tokens: read freely
- 1,000-5,000 tokens: read if likely relevant
- 5,000+ tokens: prefer section-level reading via byte offsets

### 3.3 Use the link graph to navigate

Each note lists `outbound_internal_links` (file paths to other notes in the vault). When one note references another, follow the link:

```python
# What does this note link to?
note["outbound_internal_links"]
# -> ["api/rest/Auth.md", "api/Index.md"]
```

This is like following hyperlinks on the original site, but without any HTTP requests.

---

## 4. File Structure Reference

```
vault/
├── .site2vault/
│   └── manifest.json          # START HERE - full corpus inventory
├── Index.md                    # Root Map of Content (links to all notes)
├── getting-started/
│   ├── Index.md                # Folder MOC
│   ├── Installation.md         # Note
│   └── Quick Start.md          # Note
├── api/
│   ├── Index.md
│   └── REST Reference.md
└── log/                        # Crawler internals (not for reading)
    ├── site2vault.sqlite       # State DB (frontier, redirects, host stats)
    ├── site2vault-*.log        # Human-readable crawl log
    ├── headings/               # Per-note heading sidecars (byte offsets)
    │   └── <filename>.json
    └── link-index/             # Per-note link sidecars (original URLs)
        └── <filename>.json
```

### What to read, what to skip:

| File/Folder | Read? | Purpose |
|---|---|---|
| `.site2vault/manifest.json` | **Always read first** | Complete corpus index with headings, links, sizes |
| `*.md` notes | Read as needed | The actual documentation content |
| `Index.md` (root) | Skim for overview | Navigable table of contents with wikilinks |
| `*/Index.md` (folder) | Skim for section overview | Per-folder tables of contents |
| `log/` | Skip | Crawler internals, debugging only |
| `log/headings/*.json` | Skip | Already in the manifest |
| `log/link-index/*.json` | Skip | Historical link resolution data |
| `log/site2vault.sqlite` | Skip | Crawler state database |

---

## 5. Note Format

Each note is a Markdown file with YAML frontmatter:

```markdown
---
source_url: https://docs.example.com/api/endpoints
author: Jane Smith
published: 2025-06-15
description: Complete reference for all REST API endpoints.
tags:
  - source/web
---

# API Endpoints

Content here with [[wikilinks]] to other notes in the vault
and [external links](https://example.com) to outside URLs.
```

### Key properties:

- **`source_url`** in frontmatter: the original URL this note was crawled from
- **`[[wikilinks]]`**: internal links to other notes in the vault (Obsidian format)
- **`[text](url)`**: external links to pages not in the vault
- **Headings**: ATX style (`# H1`, `## H2`, etc.)
- **No images**: all media is stripped; only text content is preserved
- **Title = filename**: the note's title is its filename (not in frontmatter)

---

## 6. Multi-Site Vaults

When multiple sites are mirrored into the same vault using `--namespace`, the structure changes:

```
vault/
├── .site2vault/
│   ├── index.json                  # Namespace registry
│   ├── docs/manifest.json          # Per-namespace manifest
│   └── blog/manifest.json
├── docs/                           # Namespace: docs
│   ├── Index.md
│   └── ...
└── blog/                           # Namespace: blog
    ├── Index.md
    └── ...
```

**Start with `.site2vault/index.json`** to discover available namespaces, then read the per-namespace manifest.

---

## 7. Recommended Workflow for Answering Questions

### "How does feature X work in this documentation?"

1. Read `.site2vault/manifest.json`
2. Search `notes[].headings[].text` and `notes[].title` for keywords related to X
3. Use `start_byte`/`end_byte` to read just the relevant sections
4. Follow `outbound_internal_links` if the section references other pages

### "Give me an overview of this documentation site"

1. Read `.site2vault/manifest.json` → check `stats` for corpus size
2. Read root `Index.md` for the navigable table of contents
3. Scan the `notes` array — look at folder structure and titles to understand the site's organization

### "What does this API endpoint do?"

1. Read `.site2vault/manifest.json`
2. Find the note by URL pattern or title keyword
3. Read the specific note file (or just the relevant section via byte offsets)

### "Compare how two pages explain topic Y"

1. Find both notes via manifest search
2. Read the relevant sections from each using byte offsets
3. Compare — the wikilinks between them tell you how the original site connected them

---

## 8. Token Budget Planning

The manifest provides everything you need to plan token usage:

```python
manifest["stats"]["estimated_total_tokens"]  # Total corpus size
# -> 3,259,547 estimated tokens

# Individual note sizes:
sorted_notes = sorted(manifest["notes"], key=lambda n: n["estimated_tokens"], reverse=True)
# Top 5 largest notes:
for n in sorted_notes[:5]:
    print(f'{n["estimated_tokens"]:>6} tokens  {n["file"]}')
```

**Rule of thumb**: Token estimates use `word_count * 1.33`. This is approximate — actual BPE tokenization varies by content type (code vs. prose) and model, but close enough for budget planning.

For a large corpus (1000+ notes, 3M+ tokens), **never read the entire vault**. Use the manifest to identify the 5-10 most relevant notes, then read only those (or sections of those).

---

## 9. Edge Cases and Gotchas

### Collision suffixes in filenames

When multiple pages have the same title, filenames get a hash suffix: `Showcase OpenAI Developers-a1b2c3.md`. The manifest's `url` field tells you which page each file came from.

### Empty or thin notes

Some pages (landing pages, redirect pages, login walls) produce notes with very little content. Check `word_count` in the manifest — notes under 50 words are usually not useful for answering questions.

### Failed URLs

`manifest.stats.failed_url_count` tells you how many pages couldn't be crawled. If you're looking for content that should exist but doesn't, it may be in the failed set. The SQLite database (`log/site2vault.sqlite`) has the `frontier` table with error reasons, but you generally shouldn't need to query it.

### External links

Notes contain `[text](https://...)` links to pages NOT in the vault. These are sites that were out of scope or on different domains. The manifest's `outbound_external_links` array lists them without requiring you to read the note.

### Stale content

Check `crawled_at` in the manifest to know when the vault was last updated. For fast-moving documentation, content may be outdated. The original `source_url` in frontmatter lets you (or the user) verify against the live site if needed.
