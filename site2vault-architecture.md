# Site2Vault — Technical Architecture

## 1. What It Does

Site2Vault is a cross-platform Python CLI that mirrors websites into fully linked [Obsidian](https://obsidian.md/) vaults. Given a seed URL, it crawls every reachable page under the same domain, converts each page to clean Markdown, and wires all internal links as Obsidian `[[wikilinks]]`. The result is a self-contained vault you can open in Obsidian and navigate exactly like the original site — except offline, in Markdown, and with bi-directional link graph support.

```
site2vault --url docs.example.com --path ./vaults --name my-vault --depth 5
```

Produces:

```
vaults/my-vault/
├── Index.md                  # Root MOC (Map of Content)
├── getting-started/
│   ├── Index.md              # Folder MOC
│   ├── Installation.md
│   └── Quick Start.md
├── api/
│   ├── Index.md
│   └── REST Reference.md
└── log/
    ├── site2vault.sqlite     # Resumable state DB
    ├── site2vault-2026-04-24-*.log
    ├── link-index/           # Per-note link sidecar JSONs
    └── headings/             # Per-note heading sidecar JSONs
```

---

## 2. High-Level Pipeline

The app executes a **multi-phase pipeline**, orchestrated by `orchestrator.py`:

```
Phase 1: CRAWL          Phase 1.5: DEBOILERPLATE   Phase 2: REWRITE
─────────────────       ────────────────────────   ──────────────────
Seed URL + Sitemap      Cross-page paragraph       Replace S2V_LINK_N
    │                   hash frequency analysis    placeholders with
    ▼                   → remove repeated cruft    [[wikilinks]] or
Frontier loop                                      [markdown](links)
(fetch → extract →
 convert → write .md)       Phase 2.5: OFFSETS     Phase 3: INDEX
    │                       ──────────────────     ──────────────
    ▼                       Compute heading        Generate Index.md
Discover links              byte offsets in        (root + per-folder
(enqueue to frontier)       final Markdown         MOCs)

                            Phase 4: MANIFEST
                            ─────────────────
                            Build .site2vault/manifest.json
                            with per-note metadata
```

### Why multiple phases?

Links can only be resolved after the **full URL → filename map** exists. During crawl, we don't yet know which URLs will succeed, fail, or redirect. So Phase 1 writes placeholder tokens (`S2V_LINK_0`, `S2V_LINK_1`, ...) wherever a link appears, and Phase 2 resolves them once every page has been processed.

Cross-page boilerplate detection (Phase 1.5) must run after all notes are written but before rewrite, so repeated cruft doesn't get linked. Heading byte offsets (Phase 2.5) must run after rewrite because link replacement changes byte positions. The manifest (Phase 4) runs last because it reads the final state of all files.

---

## 3. Module Map

| Module | Responsibility |
|---|---|
| `cli.py` | Typer CLI entry point. Named parameters (`--url`, `--path`, `--name`), parses into `RunConfig`. |
| `config.py` | `RunConfig` dataclass — single source of truth for all settings. |
| `orchestrator.py` | Wires the three phases: crawl → rewrite → index. |
| `crawler.py` | Async crawl loop: frontier management, HTTP fetching, link discovery. |
| `extract.py` | HTML → cleaned HTML. Trafilatura main-content extraction with BS4 fallback. Strips media. |
| `convert.py` | Cleaned HTML → Markdown with `S2V_LINK_N` placeholder tokens. Uses `markdownify`. |
| `rewrite.py` | Phase 2: replaces placeholder tokens with `[[wikilinks]]` or `[external](links)`. |
| `frontmatter.py` | Builds YAML frontmatter (`source_url`, `author`, `published`, `description`, `tags`). |
| `index.py` | Generates root `Index.md` and per-folder MOC indexes. |
| `canonical.py` | URL canonicalization: normalize scheme, host, path, query; strip tracking params. |
| `slug.py` | URL/title → filename mapping with collision handling. |
| `state.py` | SQLite state database for resumable crawls. |
| `robots.py` | `robots.txt` fetching, parsing, caching, and `Crawl-delay` extraction. |
| `politeness.py` | Token-bucket rate limiter, per-host delay, adaptive backoff, circuit breaker. |
| `antibot.py` | Detects Cloudflare challenges, CAPTCHAs, login walls, consent walls, bot traps. |
| `render_js.py` | Optional Playwright-based JS rendering (lazy import, `pip install 'site2vault[js]'`). |
| `manifest.py` | Builds `.site2vault/manifest.json` listing every note with metadata. |
| `progress.py` | Structured progress event system with `RichEmitter` and `JsonEmitter`. |
| `exit_codes.py` | Named exit code constants (0-4). |
| `sitemap.py` | Sitemap discovery and XML parsing with index recursion and gzip support. |
| `boilerplate.py` | Two-stage boilerplate stripping (static rules + cross-page frequency). |
| `boilerplate_patterns.py` | CSS selectors and regex for known boilerplate elements. |
| `chunking.py` | Heading-level byte offset computation for section-level file reading. |
| `logging_setup.py` | Rich console handler + timestamped rotating log file. Selects emitter. |

---

## 4. Phase 1: Crawl (crawler.py)

### 4.1 Frontier Loop

The crawler uses a **breadth-first frontier** backed by SQLite:

```python
while True:
    if done_count >= max_pages:
        break
    pending = db.get_pending_urls(concurrency)
    if not pending:
        break
    await asyncio.gather(*[process_url(url, depth) for url in pending])
```

URLs are fetched from the `frontier` table ordered by `depth ASC, rowid ASC` (breadth-first). Each URL passes through:

1. **Politeness gate** — token bucket + per-host delay + jitter
2. **HTTP fetch with retry** — up to 3 retries on transient errors (500/502/503/504/429)
3. **Content-type check** — only `text/html`, `application/xhtml+xml`, `text/plain`
4. **Meta refresh detection** — follows `<meta http-equiv="refresh">` redirects (see §7.3)
5. **HTTP redirect tracking** — records `from_url → to_url` for wikilink resolution
6. **Anti-bot check** — Cloudflare, CAPTCHA, login wall, consent wall detection
7. **Content extraction** — trafilatura + BS4 fallback (see §5)
8. **Bot trap check** — duplicate content hash, query explosion, calendar explosion
9. **Markdown conversion** — placeholder link tokens (see §6)
10. **File write** — YAML frontmatter + markdown body
11. **Link discovery** — extract all `<a href>` from **raw HTML** and enqueue

### 4.2 HTTP Client

```python
httpx.AsyncClient(
    http2=True,               # HTTP/2 for multiplexing
    follow_redirects=True,    # Up to 5 hops
    max_redirects=5,
    limits=Limits(max_connections=concurrency*2, max_keepalive=concurrency),
    timeout=Timeout(connect=10, read=30, write=10, pool=60),
)
```

Headers include a descriptive `User-Agent` with contact URL, plus `Accept: text/html`, `Accept-Language`, `Accept-Encoding`, and a `Referer` header set to the discovering page's URL.

### 4.3 Retry Logic

| Status Code | Behavior |
|---|---|
| 429 | Parse `Retry-After`, exponential backoff (2→4→8→16→30s), halve global rate |
| 503 | Same as 429 (often means "overloaded, come back later") |
| 500, 502, 504 | Retry up to 3 times |
| 400, 401, 404, 405, 406, 410, 451 | Permanent failure, no retry |
| Connection errors | Retry with `2^attempt` second backoff |

### 4.4 Scope Enforcement

URLs are filtered through:

1. **Scheme filter** — skip `mailto:`, `tel:`, `javascript:`, `data:`, `ftp:`, `file:`
2. **Domain scope** — configurable via `--same-domain` / `--any-domain` and `--subdomain-policy`:
   - `strict`: exact hostname match only
   - `include` (default): seed host + subdomains (e.g., `docs.example.com` matches `example.com`)
   - `any`: same base domain (last two segments)
3. **Include/exclude regex filters** — `--include` and `--exclude` patterns applied to canonical URLs
4. **Session parameter filter** — URLs with `sid`, `phpsessid`, `jsessionid`, etc. are skipped
5. **Max depth** — `--depth N` limits how many hops from the seed URL

### 4.5 Link Discovery: Raw HTML vs. Trafilatura

**Design decision**: Links are discovered from the **raw HTML** (via `_extract_raw_links()`), not from trafilatura's extracted content.

Trafilatura is designed for main-content extraction — it intentionally strips navigation, sidebars, footers, and menus. If we only discovered links from trafilatura's output, we'd miss most of the site's page tree. The raw-HTML extraction ensures navigation links, breadcrumbs, sidebar menus, and footer links all get discovered for crawling.

The trafilatura-extracted content is still used for the **note body** — we just don't rely on it for link discovery.

---

## 5. Content Extraction (extract.py)

### 5.1 Pipeline

```
Raw HTML
    │
    ├─ _expand_tabs()           # Expand tabbed UI into labeled sections
    ├─ _preprocess_figcaptions() # Convert <figcaption> to <p> before trafilatura strips them
    │
    ▼
trafilatura.extract(output_format="html", include_links=True, include_tables=True)
    │
    ├─ If result < 50 chars → BS4 fallback (<article> → <main> → largest <div>)
    │
    ▼
_strip_media()              # Remove img, picture, svg, video, audio, canvas, iframe, etc.
_preserve_figcaptions()     # Unwrap remaining figcaptions as <p>
_extract_headings()         # Collect h1-h6 with text, level, id
_extract_links()            # Collect <a href> with text and fragment
```

### 5.2 Tab Expansion

Many documentation sites use tabbed UI components (`role="tablist"` + `role="tabpanel"`) to show platform-specific content (e.g., "Windows / macOS / Linux" tabs). Only the active tab is visible in the DOM; the others are hidden via CSS/JS.

**Problem**: Trafilatura only sees the active tab's content. Hidden tab panels are lost.

**Solution**: `_expand_tabs()` runs **before** trafilatura. It finds all `role="tablist"` elements, matches each `role="tab"` to its `role="tabpanel"` via `aria-controls` → `id`, then replaces the entire tab group with a sequence of `<h4>Tab Label</h4><div>Panel Content</div>` blocks. This ensures ALL tab content appears in the final note.

The implementation handles:
- Nested tab groups (processes innermost first via iterative loop)
- Missing panels (skipped gracefully)
- `aria-controls` → `id` matching with fallback to `aria-labelledby`

### 5.3 Metadata Extraction

Metadata is extracted from multiple sources in priority order:
- `<html lang="...">` → language
- `<meta property="og:author">`, `<meta name="author">`, `<meta name="dc.creator">` → author
- `<meta property="article:published_time">`, `<meta name="dc.date">` → published date
- `<meta property="og:description">`, `<meta name="description">` → description (truncated to 160 chars)
- `<script type="application/ld+json">` → JSON-LD `author.name`, `datePublished`

---

## 6. Markdown Conversion (convert.py)

### 6.1 Placeholder-Then-Rewrite Strategy

This is the core design pattern of the entire app.

**Problem**: When converting page A's HTML to Markdown, we need to know the Obsidian filename of page B to create `[[Page B]]`. But page B might not have been crawled yet. It might redirect. It might fail. We can't know until Phase 1 is complete.

**Solution**: Two-pass conversion.

**Pass 1 (during crawl)**: Replace every `<a href="...">` with a numbered placeholder token before running markdownify:

```python
# Before markdownify:
<a href="https://example.com/page-b">see this</a>

# After token replacement:
<a href="S2V_LINK_0">see this</a>

# After markdownify:
[see this](S2V_LINK_0)

# Sidecar JSON (link-index/Page-A.json):
{"S2V_LINK_0": {"url": "https://example.com/page-b", "text": "see this"}}
```

**Pass 2 (rewrite.py)**: After all pages are crawled, read every note, look up each `S2V_LINK_N` in the sidecar JSON, resolve the URL to a note filename, and replace:

```markdown
# Internal link (URL maps to a crawled note):
[see this](S2V_LINK_0)  →  [[Page B|see this]]

# External link (URL not in vault):
[see this](S2V_LINK_0)  →  [see this](https://external.com/page)
```

### 6.2 Safety Guard

The converter raises `ValueError` if the source HTML already contains the string `S2V_LINK_` — this would cause silent corruption during the rewrite pass. This has never triggered in practice but prevents a catastrophic class of bugs.

### 6.3 Link Text Handling

Long link text (e.g., `<a>` tags wrapping entire paragraphs) is capped at 100 characters to prevent absurdly long wikilinks like `[[Page|This is a very long paragraph that was accidentally wrapped in an anchor tag and would create an unreadable link...]]`.

### 6.4 Markdownify Configuration

```python
markdownify(html, heading_style="ATX", bullets="-", strip=STRIP_TAGS)
```

`ATX` headings (`# H1`, `## H2`), dash bullets, and media/script tags stripped.

---

## 7. Link Rewriting (rewrite.py)

### 7.1 Resolution Logic

For each `[display text](S2V_LINK_N)` pattern:

1. Look up `S2V_LINK_N` in the note's sidecar JSON → get original URL and text
2. Resolve relative URL against the note's source URL
3. Separate fragment (`#section`) from base URL
4. Canonicalize the base URL
5. Look up canonical URL in the `url_to_note` map (includes redirect mappings)
6. If found → format as `[[wikilink]]`
7. If not found → keep as `[text](https://...)`

### 7.2 Wikilink Formatting

```python
# Shortest style (default): just filename if unique
[[Page B]]

# With alias if display text differs from filename
[[Page B|see this]]

# With anchor (heading resolved to Obsidian heading text)
[[Page B#Installation|install guide]]

# Path style (if filename collides across folders, or --link-style=path)
[[docs/api/Page B|see this]]
```

Anchor fragments are resolved by matching the web anchor slug against the target note's heading slugs (stored in `headings/*.json` sidecars).

### 7.3 Space Insertion

After all placeholder replacements, regex passes ensure proper spacing around links:

```python
# "word[[Page]]" → "word [[Page]]"
re.sub(r'(\w)\[\[', r'\1 [[', content)

# "]]word" → "]] word"
re.sub(r'\]\](\w)', r']] \1', content)

# "word[text](url)" → "word [text](url)"
re.sub(r'(\w)\[([^\]]+)\]\(http', r'\1 [\2](http', content)

# "](url)word" → "](url) word"
re.sub(r'\]\(([^)]+)\)(\w)', r'](\1) \2', content)
```

Any remaining bare `S2V_LINK_N` tokens (not inside markdown links) are cleaned up.

---

## 8. URL Canonicalization (canonical.py)

Every URL passes through `canonicalize()` before entering the frontier or being compared. Rules applied in order:

1. **Lowercase** scheme and hostname
2. **Strip default ports** (`:80` for HTTP, `:443` for HTTPS)
3. **Force HTTPS** when seed uses HTTPS (upgrade `http://` → `https://`)
4. **Drop fragment** (`#section` removed — stored separately for anchor resolution)
5. **Normalize www** — strip `www.` prefix unless the seed URL uses `www.`
6. **Strip trailing slash** (except bare `/`)
7. **Strip tracking params** — removes 20+ known tracking/session parameters: `utm_*`, `fbclid`, `gclid`, `_ga`, `phpsessid`, `jsessionid`, etc.
8. **Sort query params** alphabetically
9. **Percent-encode** path segments per RFC 3986

This ensures that `https://Example.COM:443/page/?utm_source=twitter&b=2&a=1#top` and `https://example.com/page?a=1&b=2` map to the same canonical URL.

---

## 9. Filename Assignment (slug.py)

### 9.1 Rules

1. Use page `<title>` if available → `sanitize()` (NFKC normalize, strip forbidden chars, cap at 120 chars)
2. Else use last URL path segment → `slugify()` (ASCII-fold, lowercase, hyphen-delimited)
3. Else use first 8 chars of URL's SHA-1 hash
4. If collision with existing filename → append `-` + first 6 chars of URL's SHA-1

### 9.2 Folder Structure

`url_to_folder_path()` derives folder nesting from the URL path relative to the seed. The last path segment (the page itself) is removed, and remaining segments are slugified:

```
https://docs.example.com/api/rest/endpoints.html
→ folder_path: "api/rest"
→ filename:    "Endpoints"
→ note:        my-vault/api/rest/Endpoints.md
```

The `--flat` flag disables folder structure, prefixing folder segments to the filename with `--` separators instead.

---

## 10. State Database (state.py)

SQLite with WAL mode for concurrent reads. Five tables:

| Table | Purpose |
|---|---|
| `run_config` | Key-value store of config params for resume validation |
| `frontier` | URL queue with `status` (pending/in_progress/done/failed/skipped) and `depth` |
| `url_notes` | Maps URLs to filenames, folder paths, titles, content hashes |
| `redirects` | `from_url → to_url` for redirect chain resolution |
| `host_stats` | Per-host request/error counts, backoff state, current rate |

### 10.1 Resumability

On crash, `reset_in_progress()` moves all `in_progress` URLs back to `pending`. The crawler picks up where it left off — only re-fetching the batch that was in-flight at crash time.

Config mismatch detection prevents accidentally resuming with different settings (e.g., different seed URL). Use `--force` to override.

---

## 11. Politeness System (politeness.py)

### 11.1 Components

**Token Bucket** — Global rate limiter. Tokens refill at `--rate` per second (default: 1.0 req/s). Each fetch consumes one token.

**Per-Host Delay** — Minimum `--min-delay` seconds (default: 0.5s) between requests to the same host. Honors `Crawl-delay` from `robots.txt`.

**Jitter** — Random delay factor (default: 0.3) applied per request to avoid thundering herd.

### 11.2 Adaptive Backoff

On HTTP 429 or 503:
- Parse `Retry-After` header if present
- Else exponential backoff: 2→4→8→16→30 seconds
- Halve global rate (restored gradually after 20 consecutive successes at +10% per 10 successes)

On 3 consecutive connection errors: 60-second backoff + rate halving.

### 11.3 Circuit Breaker

Sliding window of last 50 results per host. If `--max-errors` (default: 10) errors in the window:
- **First trip**: 60-second pause, clear window
- **Second trip**: Permanently stop crawling that host

### 11.4 Anti-Bot Kill Switch

3 consecutive anti-bot detections (Cloudflare challenge, CAPTCHA, etc.) → permanently stop the host with a suggestion to try `--render-js`.

---

## 12. Anti-Bot Detection (antibot.py)

### 12.1 Response-Level Checks

| Signal | Detection Method |
|---|---|
| Cloudflare | 403 + `cf-ray` header, or body contains `cf-browser-verification`, `cf-challenge`, `Just a moment...` |
| CAPTCHA | Body contains `g-recaptcha`, `h-captcha`, `turnstile`, `/recaptcha/api.js` |
| Login wall | Final URL redirected to `/login`, `/signin`, `/auth`, etc., or has `returnto`/`redirect` query params |
| Consent wall | Body contains `onetrust`/`cookielaw`/`quantcast` AND stripped text < 200 chars |
| Generic block | 403 with body < 2KB, or 200 with "access denied"/"forbidden" in `<title>`/`<h1>` |

### 12.2 Bot Trap Checks

| Trap | Detection |
|---|---|
| Query explosion | Same URL path seen with 100+ different query strings |
| Calendar explosion | Same URL prefix with 10+ different `/YYYY/MM/DD/` patterns |
| Duplicate content | SHA-256 content hash matches a previously seen page |
| Session URL | URL contains `sid`, `phpsessid`, `jsessionid`, etc. query params |

---

## 13. Meta Refresh Redirects (crawler.py)

### 13.1 The Problem

Many documentation sites (e.g., docs.interop.io) use `<meta http-equiv="refresh" content="0; url=...">` for redirects. These are **not HTTP redirects** — they're HTML-level instructions. `httpx` (and most HTTP clients) does not follow them. The response is a 200 OK with a tiny HTML body, and the crawler would process it as a normal page — resulting in an empty or near-empty note, with the actual documentation tree unreachable.

### 13.2 The Solution

`_parse_meta_refresh()` scans the response body for `<meta http-equiv="refresh">` tags using regex:

```python
match = re.search(
    r'<meta\s[^>]*http-equiv\s*=\s*["\']?refresh["\']?[^>]*'
    r'content\s*=\s*["\']?\s*\d+\s*;\s*url\s*=\s*([^"\'\s>]+)',
    body, re.IGNORECASE,
)
```

When detected:
1. The target URL is resolved against the current page's URL
2. A redirect record is saved in the DB (for wikilink resolution)
3. The target is enqueued to the frontier at the **same depth** (not depth+1)
4. The current URL is marked `done` (it's a redirect page, not content)

---

## 14. YAML Frontmatter (frontmatter.py)

Each note gets YAML frontmatter with:

```yaml
---
source_url: https://example.com/page
author: John Doe           # if detected
published: 2024-01-15      # if detected
description: A short...    # if detected, truncated to 160 chars
tags:                       # if --tag used (repeatable)
  - source/web
  - reference
---
```

**Design decision**: `title` is intentionally omitted from frontmatter. The note's filename IS the title in Obsidian — repeating it in frontmatter is redundant and creates a maintenance burden if the file is renamed.

Tags are added when `--tag` is passed on the CLI (repeatable: `--tag source/web --tag reference`). They appear as standard Obsidian tags in frontmatter.

---

## 15. Index Generation (index.py)

After rewriting, the app generates:

1. **Root `Index.md`** — frontmatter with source URL, heading with site hostname, mirror date and note count, list of top-level folder sections, then all notes grouped by folder with `[[wikilinks]]`.

2. **Per-folder `Index.md`** — one per subfolder, listing all notes in that folder.

These serve as Obsidian Maps of Content (MOCs), providing navigable entry points into the vault.

---

## 16. Packaging & Distribution

### 16.1 Python Package

Standard `pyproject.toml` with `setuptools` backend. Entry point: `site2vault = "site2vault.cli:app"`.

Installable via:
```
pip install -e .          # Development
pipx install site2vault   # End-user (isolated venv, adds to PATH)
```

### 16.2 Standalone Executable

Built with PyInstaller (`--onefile`). Bundles the entire Python runtime, all dependencies (trafilatura, lxml, httpx with HTTP/2, beautifulsoup4, markdownify, etc.), and certifi CA certificates into a single `.exe`.

```
python -m PyInstaller --onefile --name site2vault --console \
    --collect-all trafilatura --collect-all certifi \
    --hidden-import=h2 --hidden-import=hpack --hidden-import=hyperframe \
    --hidden-import=lxml.html --hidden-import=lxml.etree \
    ... (all site2vault submodules) \
    --paths src src/site2vault/cli.py
```

Key PyInstaller considerations:
- `trafilatura` requires `--collect-all` because it loads data files (language models, settings) at runtime
- `justext` requires `--collect-all` for stoplist data files (trafilatura dependency; without it, extraction crashes at runtime)
- `certifi` must be collected for HTTPS certificate verification
- `h2`, `hpack`, `hyperframe` are httpx's HTTP/2 dependencies — not auto-detected
- `lxml` C extensions require explicit hidden imports
- All `site2vault.*` submodules need hidden imports since they're lazily imported

---

## 17. Issues Found and Solved

### 17.1 Trafilatura Strips Navigation Links

**Problem**: Trafilatura is a main-content extractor — it intentionally removes navigation bars, sidebars, footers, and menus. When the crawler only discovered links from trafilatura's output, it missed most of the site's page tree. For sites like docs.interop.io, this meant crawling only 1 page instead of hundreds.

**Solution**: Added `_extract_raw_links()` which uses BeautifulSoup to extract ALL `<a href>` links from the full raw HTML, not trafilatura's cleaned output. Raw links are used for **crawl discovery** (frontier), while trafilatura's output is used for **note content**. This separation ensures comprehensive crawling without polluting note content with navigation boilerplate.

### 17.2 Meta Refresh Redirects Not Followed

**Problem**: `httpx` doesn't follow `<meta http-equiv="refresh">` redirects. Pages like `docs.interop.io/desktop/index.html` return HTTP 200 with a tiny body containing only a meta refresh tag. The crawler treated this as a normal (empty) page and never reached the actual documentation.

**Solution**: Added `_parse_meta_refresh()` to detect meta refresh tags in response bodies. When found, the target URL is enqueued at the same depth and a redirect record is saved for wikilink resolution.

### 17.3 Tabbed Content Lost

**Problem**: Documentation sites use tabbed UI components (Windows/macOS/Linux, npm/yarn/pnpm) where only the active tab is visible. Trafilatura only captured the active tab's content; hidden tabs were lost.

**Solution**: `_expand_tabs()` pre-processes HTML before trafilatura, converting `role="tablist"` + `role="tabpanel"` structures into flat `<h4>Label</h4><div>Content</div>` sequences. All tab content is preserved regardless of active state.

**Complication**: Nested tab groups (tabs within tabs). The initial implementation consumed inner tabpanels when processing outer tab groups. Fixed by switching to `aria-controls` → `id` matching (instead of parent-relative queries) and processing iteratively with DOM restart after each group.

### 17.4 Links Jammed Against Text

**Problem**: After wikilink replacement, links appeared without spaces: `See[[Page]]for details` instead of `See [[Page]] for details`. This happened because markdownify doesn't guarantee whitespace around the placeholder tokens.

**Solution**: Post-replacement regex passes in `rewrite.py` insert spaces between `\w` characters and `[[`/`]]`/`[text](url)` boundaries.

### 17.5 Excessively Long Wikilinks

**Problem**: Some pages had `<a>` tags wrapping entire paragraphs. After conversion, this produced absurdly long wikilinks: `[[Page|This is a very long paragraph that was accidentally wrapped in an anchor tag and would create...]]`.

**Solution**: Link text is capped at 100 characters (with `...` suffix) in both `convert.py` (during HTML→Markdown) and `rewrite.py` (during placeholder replacement).

### 17.6 Figcaptions Lost by Trafilatura

**Problem**: Trafilatura strips `<figure>` elements (they typically contain images). But `<figcaption>` text inside figures contains meaningful content (image descriptions, code snippet labels) that should be preserved.

**Solution**: Two-stage handling:
1. `_preprocess_figcaptions()` converts `<figcaption>` text to `<p>` tags before trafilatura runs
2. `_preserve_figcaptions()` catches any remaining figcaptions post-extraction

### 17.7 Title Derivation (--title-from)

Note titles (used as filenames and in the manifest) can be derived from three sources via `--title-from`:

- **`auto`** (default): Uses the page's `<title>` tag. Falls back to URL slug if no title found.
- **`h1`**: Uses the first `<h1>` heading from the extracted content. Falls back to `<title>` if no h1 exists.
- **`url`**: Derives from the last URL path segment, stripping extensions and converting hyphens/underscores to spaces with title case (e.g., `/api/getting-started.html` → `Getting Started`).

### 17.8 Crawl Timeout (--timeout)

`--timeout N` sets an overall crawl time limit in minutes. The crawler checks elapsed time before each batch and stops gracefully when the deadline is reached. Remaining pending URLs stay in the frontier for a future resume run.

### 17.9 Redundant Title in Frontmatter

**Problem**: The YAML frontmatter included a `title:` property, but in Obsidian the note's filename IS the title. The frontmatter title was redundant and would diverge if the file was renamed.

**Solution**: Removed `title` from frontmatter. Only `source_url` and detected metadata (author, published, description) are included.

---

## 18. Vault Manifest (manifest.py)

A machine-readable JSON manifest is written to `.site2vault/manifest.json` after every run (unless `--no-manifest`). It lists every note with metadata for consumption by Claude Code and similar agentic tools.

### 18.1 Schema

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
      "headings": [...],
      "outbound_internal_links": ["api/rest/Auth.md"],
      "outbound_external_links": ["https://oauth.net/2/"],
      "word_count": 1840,
      "estimated_tokens": 2447,
      "content_hash": "sha256:..."
    }
  ]
}
```

### 18.2 Token Estimation

Token count is estimated as `round(word_count * 1.33)`. This approximates typical BPE tokenization ratio for English prose. It is intentionally simple — actual counts vary by model and content type — but close enough for budget estimation.

### 18.3 Outbound Links

Each note entry includes resolved `outbound_internal_links` (file paths within the vault) and `outbound_external_links` (absolute URLs). These are derived from the link-index sidecar JSONs written during Phase 1, resolved through the URL→file map including redirect targets.

### 18.4 Single-Page Merge

In `--single` mode against an existing vault, the manifest is merged rather than overwritten: existing notes are preserved, the new note is added or updated by URL, and stats are recomputed.

---

## 19. JSON Progress Output (progress.py)

### 19.1 Architecture

The progress system uses a `ProgressEmitter` protocol with two implementations:

- **`RichEmitter`** (default): Routes events through Python's logging module with Rich console formatting.
- **`JsonEmitter`** (`--json-progress`): Writes one JSON object per line to stdout, with timestamps.

A global emitter is set during `logging_setup.py` based on `config.json_progress`.

### 19.2 Event Schema

Events follow the pattern `{"event": "<name>", "ts": "<ISO8601>", ...fields}`:

| Event | When | Key Fields |
|---|---|---|
| `run_start` | Pipeline begins | `config` |
| `phase_start` | Phase begins | `phase` |
| `fetch_start` | URL fetch begins | `url`, `depth` |
| `fetch_done` | URL fetch succeeds | `url`, `status`, `bytes`, `duration_ms` |
| `fetch_failed` | URL fetch fails | `url`, `reason`, `attempt` |
| `fetch_unchanged` | 304 Not Modified | `url`, `via` |
| `note_written` | Note file written | `url`, `file` |
| `sitemap_discovered` | Sitemap parsed | `url`, `url_count` |
| `phase_end` | Phase completes | `phase`, `stats` |
| `run_end` | Pipeline completes | `exit_code`, `stats` |

---

## 20. Structured Exit Codes (exit_codes.py)

| Code | Constant | Meaning |
|---|---|---|
| 0 | `SUCCESS` | All in-scope URLs processed or properly skipped. |
| 1 | `FATAL` | Fatal error before crawl could meaningfully start. |
| 2 | `PARTIAL` | Crawl completed but at least one host hit circuit breaker or anti-bot kill switch. |
| 3 | `USER_ABORT` | User abort (SIGINT/SIGTERM). Clean shutdown, not 130. |
| 4 | `RESUME_CONFLICT` | Existing state DB has incompatible config and `--force` not set. |

The `cli.py` top-level handler maps exceptions to exit codes. `orchestrator.py` installs SIGINT/SIGTERM handlers and promotes partial-success detection from the crawler.

---

## 21. Sitemap Frontier Seeding (sitemap.py)

### 21.1 Discovery

Sitemaps are discovered in priority order:

1. `Sitemap:` directives from `robots.txt` (parsed during robots checking)
2. `<seed_origin>/sitemap.xml`
3. `<seed_origin>/sitemap_index.xml`

### 21.2 Parsing

- **Sitemap index files** are recursed up to depth 2.
- **Gzipped sitemaps** (`.xml.gz`) are detected by URL and decompressed.
- **HTML responses** (404 pages served as 200) are detected by content sniffing and treated as missing.
- All discovered URLs pass through `canonicalize()` and scope filters before frontier insertion at `depth=0`.

### 21.3 Integration

Sitemap seeding runs before the crawl loop in the orchestrator. Existing dedup logic prevents double-fetching when link discovery later finds the same URLs. Disabled with `--no-sitemap` or in `--single` mode.

---

## 22. Single-Page Mode

`--single` forces `--depth 0` and `--max-pages 1`, processing only the seed URL. Sitemap discovery is disabled. Designed for ad-hoc usage when a user wants exactly one page added to a vault mid-task.

**Index behavior**: If the vault has only one note, index generation is skipped. If appending to an existing vault, indexes are regenerated to incorporate the new note.

**Manifest behavior**: In single-page mode against an existing vault, the manifest is merged (see §18.4) rather than overwritten.

---

## 23. Boilerplate Stripping (boilerplate.py)

### 23.1 Stage 1: Static Rules

`strip_static_boilerplate(html)` runs after trafilatura extraction (gated by `--no-static-boilerplate`). It removes known boilerplate patterns by CSS selector and regex:

- Elements with class/id matching `edit-this-page`, `edit-on-github`, `feedback`, `was-this-helpful`, `last-updated`, `version-selector`, `breadcrumb`, `cookie-banner`, `consent`
- Trailing paragraphs matching `^(Last updated|Last modified|Edit this page|Was this helpful)`
- "On this page" / "Table of contents" sidebars

Patterns are defined in `boilerplate_patterns.py` as lists of CSS selectors and compiled regex patterns, designed for easy extension.

### 23.2 Stage 2: Cross-Page Detection

Phase 1.5 in the pipeline (between Crawl and Rewrite). Algorithm:

1. Hash each paragraph (normalized whitespace, text only) across all notes
2. Build frequency map: how many notes contain each paragraph hash
3. Flag paragraphs appearing in more than `--boilerplate-threshold` (default 0.5 = 50%) of notes
4. Remove flagged paragraphs from each note's Markdown file

**Safeguards**:
- Auto-disables below 20 notes (small corpora trigger false positives)
- Never removes paragraphs inside fenced code blocks
- Emits progress events with flagged pattern count and notes modified

---

## 24. Heading-Level Chunking Metadata (chunking.py)

Enables section-level file reading by recording byte offsets for each heading in the final Markdown files.

### 24.1 Timing

Runs as Phase 2.5, after rewrite (because link replacement changes byte positions). Reads the final `.md` files and computes offsets on the UTF-8 encoded bytes.

### 24.2 Sidecar Schema

Written to `log/headings/<filename>.json`:

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

**Section boundaries**: A section starts at the heading line's byte offset and ends at the next heading of equal or lesser level, or EOF. The manifest (§18) references these offsets so Claude Code can read `file[start_byte:end_byte]` to get exactly one section.

---

## 25. Conditional GET (crawler.py, state.py)

### 25.1 Storage

The `url_notes` table stores `etag` and `last_modified` columns (added via schema migration). When a page is fetched, the crawler stores the response's `ETag` and `Last-Modified` headers.

### 25.2 Behavior

On resume or refresh runs, the crawler sends `If-None-Match` and `If-Modified-Since` headers using stored values:

- **304 Not Modified**: URL marked `done`, note not rewritten, `fetch_unchanged` event emitted
- **200 OK**: Note processed normally, headers updated
- **No stored headers**: Full fetch (no conditional headers sent)

---

## 26. Refresh Mode

`--refresh` re-crawls an existing vault using conditional GET for known URLs. All `done` URLs in the frontier are re-queued as `pending`.

### 26.1 Pruning

`--prune` deletes note files whose URLs returned 404 or 410 on refresh. Without `--prune`, removals are logged as warnings only. Non-404/410 failures (500, timeout, etc.) are never pruned.

### 26.2 Flow

1. Re-queue all `done` frontier entries as `pending`
2. Crawl with conditional GET headers
3. Unchanged pages (304) skip processing
4. Changed pages overwrite notes normally
5. New URLs discovered during crawl are processed as full fetches
6. After crawl, handle removals (prune or warn)
7. Rebuild manifest and indexes

---

## 27. Vault Namespacing

`--namespace NAME` isolates multiple sites within a single vault. Each namespace gets its own subdirectory, state database, and manifest.

### 27.1 Directory Structure

```
vault/
├── docs/                    # --namespace docs
│   ├── Index.md
│   ├── api/
│   └── log/site2vault.sqlite
├── blog/                    # --namespace blog
│   ├── Index.md
│   └── log/site2vault.sqlite
└── .site2vault/
    ├── index.json           # Namespace registry
    ├── docs/manifest.json   # Per-namespace manifest
    └── blog/manifest.json
```

### 27.2 Namespace Index

Top-level `.site2vault/index.json` tracks all registered namespaces:

```json
{
  "namespaces": {
    "docs": {
      "seed_url": "https://docs.example.com",
      "manifest": "docs/manifest.json",
      "updated_at": "2026-04-24T18:32:11Z"
    }
  }
}
```

Each `--namespace` run updates the index with its namespace entry. Multiple namespaces coexist independently — each has its own state DB, crawl frontier, and note tree.

---

## 28. Configuration Reference

### 28.1 Core Parameters

| Flag | Short | Default | Description |
|---|---|---|---|
| `--url` | `-url` | required | Seed URL to crawl (auto-prepends `https://` if no scheme) |
| `--path` | `-path` | `.` | Base directory for output |
| `--name` | `-name` | derived | Output folder name (default: derived from URL hostname + path) |

Output resolves to: `path / name`. Example: `--path C:\Obsidian\Vault --name "My Docs"` → `C:\Obsidian\Vault\My Docs\`.

### 28.2 Crawl Control

| Flag | Short | Default | Description |
|---|---|---|---|
| `--depth` | `-d` | 3 | Max crawl depth from seed |
| `--max-pages` | `-m` | 2000 | Hard cap on total pages |
| `--single` | `-s` | false | Fetch only the seed URL (no crawl) |
| `--timeout` | | none | Overall crawl timeout in minutes |
| `--include` | | none | Regex whitelist for URLs (repeatable) |
| `--exclude` | | none | Regex blacklist for URLs (repeatable) |
| `--same-domain/--any-domain` | | same-domain | Stay on seed domain |
| `--subdomain-policy` | | `include` | `strict` / `include` / `any` |

### 28.3 Politeness

| Flag | Default | Description |
|---|---|---|
| `--rate` | 1.0 | Target requests per second |
| `--concurrency` | 2 | Parallel fetch workers |
| `--jitter` | 0.3 | Random delay factor (0.0–1.0) |
| `--min-delay` | 0.5 | Min seconds between requests to same host |
| `--max-errors` | 10 | Circuit breaker threshold per 50-request window |
| `--ignore-robots` | false | Skip robots.txt checking |
| `--render-js` | false | Use Playwright for JS rendering |
| `--user-agent` | site2vault/0.1.0 | Override User-Agent string |

### 28.4 Output Control

| Flag | Short | Default | Description |
|---|---|---|---|
| `--flat` | `-f` | false | All notes at vault root (no subfolders) |
| `--link-style` | | `shortest` | Wikilink style: `shortest` / `path` |
| `--tag` | | none | Obsidian tag for frontmatter (repeatable) |
| `--title-from` | | `auto` | Title source: `auto` (page title), `h1` (first H1), `url` (from path) |
| `--no-manifest` | | false | Skip manifest generation |
| `--no-sitemap` | | false | Skip sitemap.xml discovery |
| `--no-static-boilerplate` | | false | Skip static boilerplate stripping |
| `--no-cross-page-boilerplate` | | false | Skip cross-page boilerplate detection |
| `--boilerplate-threshold` | | 0.5 | Cross-page boilerplate threshold (0.0–1.0) |

### 28.5 Resume & Refresh

| Flag | Default | Description |
|---|---|---|
| `--resume/--no-resume` | resume | Continue previous run |
| `--force` | false | Re-crawl even if state exists |
| `--refresh` | false | Re-crawl existing vault using conditional GET |
| `--prune` | false | Delete notes whose URLs return 404/410 on refresh |
| `--namespace` | none | Namespace for multi-site vaults |

### 28.6 Debug & Integration

| Flag | Short | Default | Description |
|---|---|---|---|
| `--verbose` | `-v` | false | Debug logging |
| `--dry-run` | | false | Discover URLs only, write no files |
| `--json-progress` | | false | Emit JSONL progress to stdout for plugin consumption |

---

## 29. Dependencies

| Package | Purpose |
|---|---|
| `typer` | CLI framework (argument parsing, help generation) |
| `httpx[http2]` | Async HTTP client with HTTP/2, connection pooling, redirect following |
| `beautifulsoup4` + `lxml` | HTML parsing (tab expansion, raw link extraction, BS4 fallback) |
| `trafilatura` | Main-content extraction from HTML (strips boilerplate, nav, ads) |
| `markdownify` | HTML → Markdown conversion |
| `pyyaml` | YAML frontmatter generation |
| `rich` | Console logging with colors and formatting |
| `playwright` (optional) | Headless browser for JS-rendered pages |

---

## 30. Test Suite

339 tests covering:
- URL canonicalization (scheme, host, port, path, query, fragment, tracking params, www normalization)
- Filename assignment (sanitization, slugification, collision handling, folder path derivation)
- Content extraction (trafilatura, BS4 fallback, media stripping, heading/link extraction, tab expansion, figcaption preservation)
- HTML→Markdown conversion (placeholder tokens, link index generation, heading slugs, safety guard, long text truncation)
- Link rewriting (wikilink formatting, external links, anchor resolution, redirect resolution, space insertion, display text aliasing)
- State database (CRUD operations, frontier management, resume logic, redirect chains, conditional GET headers)
- Index generation (root MOC, folder MOCs)
- Integration tests (end-to-end crawl with mock HTTP server)
- Vault manifest (schema, note counts, outbound links, word/token counts, no-manifest flag)
- JSON progress output (JSONL validation, event fields, emitter selection)
- Structured exit codes (all codes reachable, force override, partial success)
- Sitemap seeding (sitemap.xml, sitemap index, gzip, scope filtering, no-sitemap flag)
- Single-page mode (fresh vault, existing vault, manifest merge, index behavior)
- Boilerplate stripping (static rules, cross-page detection, code block exclusion, threshold, auto-disable)
- Heading byte offsets (section boundaries, UTF-8 correctness, EOF handling)
- Conditional GET (304 path, 200 overwrite, missing headers)
- Refresh mode (requeue, conditional GET, pruning, non-404 preservation)
- Vault namespacing (namespace dirs, index.json, manifest isolation, multi-namespace coexistence)

All tests use `pytest` with `pytest-asyncio` for async test support and `pytest-httpx` for HTTP mocking.
