# Site2Vault — Project CLAUDE.md

## Project Overview

Site2Vault is a cross-platform Python CLI that mirrors websites into linked Obsidian vaults. The downstream consumer is Claude Code (and similar agentic coding tools), not a human Obsidian user. The app exists to offload site-scraping so the agent reads local Markdown instead of burning tokens fetching web content.

- Entry point: `src/site2vault/cli.py` (Typer CLI)
- Config: `src/site2vault/config.py` (RunConfig dataclass)
- Pipeline: `src/site2vault/orchestrator.py` (multi-phase: crawl -> deboilerplate -> rewrite -> offsets -> index -> manifest)
- Architecture doc: `docs/architecture.md` (detailed technical reference)
- Improvements spec: `docs/improvements-assignment.md` (10-item assignment, all completed)

## Repo layout (for Claude Code sessions)

- Source: `src/site2vault/` (25 modules)
- Tests: `tests/` (339 tests, run with `python -m pytest`)
- Long-form docs: `docs/`

## CLI Signature

```
site2vault --url URL [--path PATH] [--name NAME] [OPTIONS]
```

All parameters are named (no positional args). Both `--url` and `-url` work (single-dash aliases for `--url`, `--path`, `--name`).

- `--url` (required): Seed URL to crawl. Auto-prepends `https://` if no scheme given.
- `--path` (optional): Base directory for output. Default: current directory.
- `--name` (optional): Output folder name. Default: derived from URL via `_domain_slug()`.
- Output resolves to: `path / name`

Short flags: `-d` (depth), `-m` (max-pages), `-s` (single), `-f` (flat), `-v` (verbose).

Additional options: `--tag` (repeatable, adds Obsidian tags to frontmatter), `--timeout` (crawl timeout in minutes), `--title-from` (auto|h1|url).

## Build & Package

### PyInstaller Standalone Exe

Spec file: `site2vault.spec`. Build with:

```
python -m PyInstaller site2vault.spec --noconfirm
```

Output: `dist/site2vault.exe`. Copy to `c:\user\` along with `site2vault.cmd`.

**Critical: `collect_all` packages in the spec file.** These packages ship data files that PyInstaller does not auto-detect:

- `trafilatura` — language models, settings, data files
- `justext` — stoplist data files (trafilatura dependency). Without this, trafilatura crashes with `[WinError 3] ... justext\stoplists` and falls back to lower-quality BS4 extraction.
- `certifi` — CA certificate bundle for HTTPS

If adding new dependencies that ship data files, always add `collect_all('package')` to the spec.

### CMD Wrapper

`site2vault.cmd` runs the CLI via Python directly (for dev use without PyInstaller):

```cmd
@echo off
C:\Python313\python.exe -c "from site2vault.cli import app; app()" %*
```

## Testing

- Framework: `pytest` with `pytest-asyncio` and `pytest-httpx`
- Run: `python -m pytest --tb=short`
- Current count: 339 tests
- All tests must pass before committing. Do not regress.

## Conventions

- Commits: `feat(scope): summary` or `fix(scope): summary`
- New modules get hidden imports added to `site2vault.spec`
- Config fields go in `RunConfig` dataclass, CLI flags in `cli.py`
- Async I/O in `crawler.py`, regex placeholder pattern in `convert.py`/`rewrite.py`, SQLite state in `state.py`
- Progress events go through `progress.py` emitter, not direct print/log

## Output Folder Naming (`_domain_slug`)

Hostname preserved with dots, path segments appended with dashes. Index files stripped.

```
https://docs.interop.io/index.html    -> docs.interop.io
https://code.claude.com/docs/en/      -> code.claude.com-docs-en
https://example.com/                  -> example.com
```

Do NOT reverse hostname segments. Do NOT strip subdomains. Preserve the hostname exactly as-is.

## Known Issues & Lessons Learned

1. **justext stoplists not bundled by PyInstaller**: `trafilatura` depends on `justext` which ships stoplist data files. Without `collect_all('justext')` in the spec, the exe crashes at runtime with a misleading `[WinError 3]` path error. Always verify new trafilatura-chain dependencies have their data files collected.

2. **Trafilatura strips navigation links**: Links are discovered from raw HTML (`_extract_raw_links()`), not trafilatura output. Trafilatura is for note content only.

3. **Meta refresh redirects**: `httpx` does not follow `<meta http-equiv="refresh">` redirects. `_parse_meta_refresh()` in `crawler.py` handles this.

4. **Link placeholder pattern**: `S2V_LINK_N` tokens in Phase 1, resolved in Phase 2 (rewrite). Never use this prefix in test HTML fixtures.

5. **Heading byte offsets must run after rewrite**: Link replacement changes byte positions, so `chunking.py` runs as Phase 2.5.

6. **Cross-page boilerplate auto-disables below 20 notes**: Small corpora trigger false positives.
