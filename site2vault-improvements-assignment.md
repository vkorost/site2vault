# Site2Vault Improvement Assignment

## Context

Site2Vault is a Python CLI that mirrors websites into Obsidian vaults as linked Markdown. Architecture details are in `site2vault-architecture.md` at the project root. Read it first.

The downstream consumer of the output is **Claude Code** (and similar agentic coding tools), not a human Obsidian user. The app exists to offload site-scraping work from Claude Code so the agent does not burn tokens fetching, parsing, and re-fetching web content. Once a site is mirrored locally, Claude Code reads Markdown files, follows wikilinks, and greps the corpus at near-zero token cost.

Every change in this assignment is justified by one or more of:

1. **Token efficiency for the downstream agent.** Less boilerplate, smaller files, structured metadata.
2. **Retrieval primitives.** Manifest, search index, heading offsets so the agent can find content without scanning.
3. **Plugin integration.** Structured CLI output so an Obsidian plugin frontend can spawn the binary cleanly.
4. **Crawl quality compounding over time.** Sitemap seeding, conditional GET, refresh mode.

Do not add features outside this list. Specifically:

- No embeddings, no vector search, no summarization passes.
- No TUI or web UI.
- No new dependencies unless explicitly required by an item below.

## Working Rules

- Read `site2vault-architecture.md` before writing code.
- Match existing module conventions: dataclass configs in `config.py`, async I/O in `crawler.py`, regex placeholder pattern in `convert.py` and `rewrite.py`, SQLite state in `state.py`.
- Each item below is independently shippable. Implement in the order given. Do not interleave.
- For each item: implement, write tests, run the full suite, commit with a message of the form `feat(scope): one-line summary` or `fix(scope): one-line summary`. Reference the assignment item number in the commit body.
- Tests use `pytest` with `pytest-asyncio` and `pytest-httpx`. The current suite has 249 tests. Do not regress.
- Do not break the existing CLI surface. New flags are additive.

## Item 1: Vault Manifest at Root

**Goal:** Emit a single machine-readable manifest at the vault root listing every note with metadata. Claude Code reads one file and knows the entire corpus shape.

**Output path:** `.site2vault/manifest.json` inside the output directory. The dot-prefix keeps it out of the default Obsidian file tree view while remaining accessible to filesystem tools.

**Schema:**

```json
{
  "schema_version": 1,
  "seed_url": "https://docs.example.com",
  "crawled_at": "2026-04-24T18:32:11Z",
  "site2vault_version": "0.1.0",
  "stats": {
    "note_count": 247,
    "total_word_count": 184320,
    "estimated_total_tokens": 245145,
    "failed_url_count": 3,
    "skipped_url_count": 12
  },
  "notes": [
    {
      "file": "api/rest/Endpoints.md",
      "url": "https://docs.example.com/api/rest/endpoints.html",
      "title": "Endpoints",
      "folder": "api/rest",
      "headings": [
        { "level": 2, "text": "Authentication", "slug": "authentication" },
        { "level": 2, "text": "Rate Limits", "slug": "rate-limits" }
      ],
      "outbound_internal_links": ["api/rest/Auth.md", "api/Index.md"],
      "outbound_external_links": ["https://oauth.net/2/"],
      "word_count": 1840,
      "estimated_tokens": 2447,
      "content_hash": "sha256:..."
    }
  ]
}
```

**Implementation:**

- New module `manifest.py` exposing `build_manifest(vault_dir, state_db, run_config) -> dict` and `write_manifest(vault_dir, manifest)`.
- Wire into `orchestrator.py` as a fourth phase after Index Generation, gated by a new `RunConfig.emit_manifest` field defaulting to `True`.
- Word count: split note body (post frontmatter) on whitespace.
- Token estimate: `round(word_count * 1.33)`. Document this heuristic in the module docstring.
- Outbound links derive from the existing link-index sidecar JSONs already written during Phase 1.
- CLI flag: `--no-manifest` to disable.

**Tests:**

- Manifest schema present and valid JSON.
- Note count matches actual `.md` files in vault.
- Outbound link resolution matches what `rewrite.py` produced.
- Word and token counts are non-zero for non-empty notes.
- `--no-manifest` suppresses the file.

## Item 2: JSON Progress Output

**Goal:** Structured stdout events for plugin consumption. The Obsidian plugin will spawn `site2vault` and parse stdout; regex-parsing human log lines is fragile.

**CLI flag:** `--json-progress`. Mutually exclusive with default Rich logging. When set, stdout receives newline-delimited JSON; stderr receives nothing routine (only fatal errors).

**Event schema:** One JSON object per line.

```
{"event": "run_start", "ts": "...", "config": {...}}
{"event": "phase_start", "ts": "...", "phase": "crawl"}
{"event": "fetch_start", "ts": "...", "url": "...", "depth": 2}
{"event": "fetch_done", "ts": "...", "url": "...", "status": 200, "bytes": 24130, "duration_ms": 412}
{"event": "fetch_failed", "ts": "...", "url": "...", "reason": "timeout", "attempt": 3}
{"event": "note_written", "ts": "...", "url": "...", "file": "api/Foo.md"}
{"event": "phase_end", "ts": "...", "phase": "crawl", "stats": {...}}
{"event": "phase_start", "ts": "...", "phase": "rewrite"}
{"event": "phase_end", "ts": "...", "phase": "rewrite", "stats": {...}}
{"event": "phase_start", "ts": "...", "phase": "index"}
{"event": "phase_end", "ts": "...", "phase": "index"}
{"event": "phase_start", "ts": "...", "phase": "manifest"}
{"event": "phase_end", "ts": "...", "phase": "manifest"}
{"event": "run_end", "ts": "...", "exit_code": 0, "stats": {...}}
```

**Implementation:**

- New module `progress.py` with a `ProgressEmitter` protocol. Two implementations: `RichEmitter` (current behavior) and `JsonEmitter`.
- `logging_setup.py` selects the emitter based on `RunConfig.json_progress`.
- All existing log calls in `crawler.py`, `orchestrator.py`, `rewrite.py`, `index.py` route through the emitter rather than direct logger calls for events that should be machine-visible.
- Routine debug/info logs still go to the rotating log file regardless of mode.

**Tests:**

- `--json-progress` produces valid JSONL on stdout.
- Each event line parses as JSON and contains required fields.
- Default mode unchanged (existing tests still pass).
- Run completion emits `run_end` with exit code.

## Item 3: Structured Exit Codes

**Goal:** Plugin and shell scripts can react to outcomes without log scraping.

**Codes:**

| Code | Meaning |
|---|---|
| 0 | Success. All in-scope URLs processed or properly skipped. |
| 1 | Fatal error before crawl could meaningfully start (config error, seed unreachable, output dir not writable). |
| 2 | Partial success. Crawl completed but at least one host hit the circuit breaker or anti-bot kill switch. |
| 3 | User abort (SIGINT/SIGTERM). |
| 4 | Resume conflict. Existing state DB has incompatible config and `--force` not set. |

**Implementation:**

- New `exit_codes.py` module with named constants.
- `cli.py` catches exceptions at the top level and maps to codes.
- `crawler.py` tracks whether any host was permanently stopped; orchestrator promotes to exit code 2.
- SIGINT handler in `orchestrator.py` ensures clean shutdown returns 3, not 130.

**Tests:**

- Each code reachable via integration test scenarios.
- `--force` resolves resume conflict and returns 0.
- Mocked anti-bot kill switch on a host returns 2.

## Item 4: Sitemap.xml Frontier Seeding

**Goal:** Faster, more complete crawls. When a site provides `sitemap.xml`, use it to pre-populate the frontier instead of relying solely on link discovery from the seed page.

**Implementation:**

- New module `sitemap.py` exposing `discover_sitemaps(seed_url, http_client) -> list[str]` and `parse_sitemap(url, http_client) -> list[SitemapEntry]`.
- Discovery order:
  1. `robots.txt` `Sitemap:` directives (already fetched in `robots.py`, expose them).
  2. `<seed_origin>/sitemap.xml`.
  3. `<seed_origin>/sitemap_index.xml`.
- Handle sitemap index files (recursive parse, cap depth at 2).
- Handle gzipped sitemaps (`.xml.gz`).
- All discovered URLs run through `canonicalize()` and scope filters before frontier insertion. Existing dedup logic prevents double-fetching when link discovery later finds the same URLs.
- Sitemap entries enter the frontier at `depth=0` so they are not depth-truncated.
- CLI flag: `--no-sitemap` to disable. Default enabled.
- New event: `{"event": "sitemap_discovered", "url": "...", "url_count": 1820}`.

**Edge cases:**

- Sitemap fetch fails: log warning, continue with link-discovery-only crawl.
- Sitemap returns HTML (404 page served as 200): detect, treat as missing.
- Sitemap contains URLs outside the seed scope: filter normally.
- Sitemap declares more URLs than `--max-pages`: respect the cap.

**Tests:**

- Mock site with valid `sitemap.xml` populates frontier correctly.
- Mock site with `sitemap_index.xml` recurses one level.
- Gzipped sitemap parsed correctly.
- `--no-sitemap` falls back to link discovery only.
- Out-of-scope URLs in sitemap filtered.

## Item 5: Single-Page Mode

**Goal:** Ad-hoc usage. User mid-task wants exactly one page added to the vault, not a recrawl.

**CLI flag:** `--single`. Forces `--depth 0`, disables sitemap discovery, processes only the seed URL.

**Implementation:**

- `cli.py` validates that `--single` is incompatible with `--depth` (other than 0) and `--max-pages` (other than 1).
- `orchestrator.py` skips Phase 3 (Index generation) in single-page mode if the vault has only the new note. If the vault is pre-existing, regenerate indexes normally to incorporate the new note.
- Manifest update: in single-page mode against an existing vault, merge the new note into the existing manifest rather than overwriting.

**Tests:**

- `--single` against fresh directory produces one note.
- `--single` against existing vault adds note and updates manifest.
- Index files regenerated in append-to-existing case.

## Item 6: Boilerplate Stripping Pass

**Goal:** Reduce per-note token count by removing repeated cruft that trafilatura misses. Documentation sites repeat persistent footers, "Edit on GitHub" links, "Was this helpful?" widgets, version selectors, breadcrumb duplicates.

**Implementation:**

Two-stage approach.

**Stage 1: Static rule pass in `extract.py`.** New function `_strip_known_boilerplate(html)` runs after trafilatura extraction. Targets known patterns by CSS selector or text match:

- Elements with class/id containing `edit-this-page`, `edit-on-github`, `feedback`, `was-this-helpful`, `last-updated`, `version-selector`, `breadcrumb`, `cookie-banner`, `consent`.
- Trailing paragraphs matching `^(Last updated|Last modified|Edit this page|Was this helpful)`.
- "On this page" / "Table of contents" sidebars when they duplicate the page's own H2/H3 set.

Patterns live in `boilerplate_patterns.py` as a list of selectors and regex rules so they are easy to extend.

**Stage 2: Cross-page boilerplate detection.** New phase between Crawl and Rewrite (call it Phase 1.5: Deboilerplate). Algorithm:

1. After all notes are written, hash each paragraph (text only, normalized whitespace) per note.
2. Build a frequency map of paragraph hashes across the corpus.
3. Any paragraph appearing on more than 50% of notes (configurable via `--boilerplate-threshold`, default 0.5) is flagged as boilerplate.
4. Run a second pass to remove flagged paragraphs from each note.

**CLI flags:**

- `--no-static-boilerplate` to skip Stage 1.
- `--no-cross-page-boilerplate` to skip Stage 2.
- `--boilerplate-threshold FLOAT` for Stage 2 threshold.

**Caveats:**

- Cross-page detection can over-trigger on small crawls (< 20 notes). Auto-disable Stage 2 below 20 notes.
- Never remove paragraphs inside code blocks. Hash only paragraphs outside fenced code.
- Emit a progress event listing boilerplate patterns detected and removal counts so the user can audit.

**Tests:**

- Static rules remove known elements.
- Cross-page detection identifies a footer present on 100% of mock pages.
- Cross-page detection ignores paragraphs in code blocks.
- Threshold flag respected.
- Small corpus auto-disables Stage 2.

## Item 7: Heading-Level Chunking Metadata

**Goal:** Let Claude Code read a single section of a long page without loading the whole file. Headings sidecar data already exists; add byte offsets.

**Implementation:**

- Modify the headings sidecar writer (in `convert.py` or `extract.py`, wherever it currently lives) to record `start_byte` and `end_byte` of each heading's section in the **final written Markdown file** (post frontmatter, post link rewriting).
- Because rewriting changes byte offsets, this must run during or after Phase 2 (Rewrite), not Phase 1.
- Sidecar schema becomes:

```json
{
  "headings": [
    {
      "level": 2,
      "text": "Authentication",
      "slug": "authentication",
      "start_byte": 1240,
      "end_byte": 4892
    }
  ]
}
```

- Section ends at: next heading of equal or lesser level, or EOF.
- Manifest (Item 1) references `start_byte`/`end_byte` per heading so a single file read tells Claude Code exactly where each section lives.

**Tests:**

- Byte offsets correctly identify section boundaries.
- Reading `file[start_byte:end_byte]` yields the expected section content.
- Last heading extends to EOF.

## Item 8: Conditional GET on Resume

**Goal:** Cheap re-crawls. When refreshing an existing vault, skip pages that have not changed.

**Implementation:**

- Extend `url_notes` table with `etag TEXT` and `last_modified TEXT` columns. Add migration.
- `crawler.py` stores `ETag` and `Last-Modified` response headers when writing a note.
- On resume runs (or new `--refresh` mode, see Item 9), the crawler sends `If-None-Match` and `If-Modified-Since` headers using stored values.
- 304 response: mark URL as `done`, do not rewrite the note, do not update manifest entry beyond `last_seen_at`.
- 200 response: process normally, overwrite the note, update headers.
- New event: `{"event": "fetch_unchanged", "url": "...", "via": "etag"}`.

**Tests:**

- 304 path: note unchanged, frontier marked done.
- 200 with new content: note overwritten.
- Missing ETag and Last-Modified: full fetch (no conditional headers sent).

## Item 9: Refresh Mode

**Goal:** Maintain a living mirror of a documentation site. One command to keep the vault current.

**CLI flag:** `--refresh`. Requires existing vault with state DB. Re-runs the original crawl using stored config, applying conditional GET (Item 8) for known URLs and discovering new URLs normally.

**Implementation:**

- `cli.py`: `--refresh PATH` reads `run_config` from the vault's state DB to recover seed URL and original settings.
- Allow flag overrides for `--max-pages`, `--depth`, `--rate` to widen or narrow the refresh.
- All `done` URLs in the frontier are re-queued as `pending` with conditional GET enabled.
- Newly discovered URLs (not in `url_notes`) processed as full fetches.
- Manifest fully rebuilt at the end (notes that no longer exist on the site are flagged: add `removed_at` timestamp, do not delete the file by default).
- New flag: `--prune` to actually delete notes whose URLs returned 404 or 410 on refresh.

**Tests:**

- Refresh of an unchanged site emits all `fetch_unchanged` events.
- Refresh after a page removal: note flagged in manifest with `removed_at`.
- `--prune` deletes 404/410 notes.
- Refresh discovers and adds new pages.

## Item 10: Vault Namespacing for Multi-Site Vaults

**Goal:** Resolve ambiguity when a single vault accumulates mirrors of multiple sites (likely with the Obsidian plugin in use).

**Implementation:**

- New `RunConfig.namespace` field. CLI flag `--namespace NAME` and `--no-namespace`.
- Default behavior: if `--out` points at a directory containing an existing `.site2vault/manifest.json` for a **different** seed URL, refuse to run unless `--namespace` is provided or `--merge` is explicit.
- When namespacing is active, all notes go under `<vault>/<namespace>/...` and the namespace gets its own `.site2vault/<namespace>/manifest.json`.
- Default namespace value when auto-applied: hostname slug of the seed URL (e.g. `docs-example-com`).
- Top-level `.site2vault/index.json` lists all namespaces in the vault:

```json
{
  "schema_version": 1,
  "namespaces": [
    { "name": "docs-example-com", "seed_url": "...", "manifest": ".site2vault/docs-example-com/manifest.json" },
    { "name": "api-other-com", "seed_url": "...", "manifest": ".site2vault/api-other-com/manifest.json" }
  ]
}
```

**Tests:**

- Fresh vault with `--namespace foo` creates `vault/foo/` tree.
- Adding a second namespace to existing vault creates parallel tree without disturbing the first.
- Refusal when seed URL conflicts with existing namespace and no override given.
- Top-level index updated correctly.

## Deliverables Summary

For each item, deliver:

1. Implementation matching this spec.
2. New tests added to the suite.
3. Existing tests still passing.
4. Updated `site2vault-architecture.md` with new sections describing the changes (each item gets its own subsection under an appropriate top-level section, or a new section if no fit exists).
5. Updated `--help` output via Typer docstrings.
6. Atomic commit per item.

## Out of Scope

Do not address in this assignment:

- The Obsidian plugin itself (separate project, separate repo).
- OpenAPI/Swagger spec detection (deferred to a later assignment).
- Full-text search index sidecar (deferred).
- Content-hash deduplication of legitimate duplicates (deferred).
- PyInstaller bundling improvements.
- Any UI work.

If a question arises about behavior not covered here, default to the principle: **what produces the smallest, cleanest, most agent-friendly Markdown corpus?** That is the north star.
