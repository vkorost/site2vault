# CLI Reference

Run `site2vault --help` for the live help text.

## Synopsis

```
site2vault --url URL [--path PATH] [--name NAME] [OPTIONS]
```

## Output location

Output resolves to `<path>/<name>`. If `--name` is omitted, it is derived from the URL hostname.

Examples:
- `--url docs.example.com` -> `./docs.example.com/`
- `--path C:\Vault --url docs.example.com` -> `C:\Vault\docs.example.com\`
- `--path C:\Vault --name "My Docs" --url docs.example.com` -> `C:\Vault\My Docs\`

## Core parameters

| Flag | Short | Default | Description |
|---|---|---|---|
| `--url` | `-url` | required | Seed URL to crawl (auto-prepends `https://` if no scheme) |
| `--path` | `-path` | `.` | Base directory for output |
| `--name` | `-name` | derived | Output folder name (default: derived from URL hostname + path) |

## Crawl control

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

## Politeness

| Flag | Default | Description |
|---|---|---|
| `--rate` | 1.0 | Target requests per second |
| `--concurrency` | 2 | Parallel fetch workers |
| `--jitter` | 0.3 | Random delay factor (0.0-1.0) |
| `--min-delay` | 0.5 | Min seconds between requests to same host |
| `--max-errors` | 10 | Circuit breaker threshold per 50-request window |
| `--ignore-robots` | false | Skip robots.txt checking |
| `--render-js` | false | Use Playwright for JS rendering |
| `--user-agent` | site2vault/0.1.0 | Override User-Agent string |

## Output control

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
| `--boilerplate-threshold` | | 0.5 | Cross-page boilerplate threshold (0.0-1.0) |

## Resume and refresh

| Flag | Default | Description |
|---|---|---|
| `--resume/--no-resume` | resume | Continue previous run |
| `--force` | false | Re-crawl even if state exists |
| `--refresh` | false | Re-crawl existing vault using conditional GET |
| `--prune` | false | Delete notes whose URLs return 404/410 on refresh |
| `--namespace` | none | Namespace for multi-site vaults |

## Debug and integration

| Flag | Short | Default | Description |
|---|---|---|---|
| `--verbose` | `-v` | false | Debug logging |
| `--dry-run` | | false | Discover URLs only, write no files |
| `--json-progress` | | false | Emit JSONL progress to stdout for plugin consumption |

## Exit codes

| Code | Meaning |
|---|---|
| 0 | Success — all in-scope URLs processed or properly skipped |
| 1 | Fatal error before crawl could meaningfully start |
| 2 | Partial — at least one host hit circuit breaker or anti-bot kill |
| 3 | User abort (SIGINT/SIGTERM) |
| 4 | Resume conflict — existing state has incompatible config and `--force` not set |
