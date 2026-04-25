# site2vault

Mirror any website into a linked Obsidian vault. One command in, folder of connected markdown notes out. Text only -- no images, no binary assets.

## Install

```bash
pip install -e .
```

For JS-rendered sites (optional):

```bash
pip install -e ".[js]"
playwright install chromium
```

## Quick start

```bash
# Mirror a documentation site
site2vault https://docs.example.com

# Shallow crawl of a blog, skip tag pages
site2vault https://blog.example.com --depth 2 --exclude '/tag/'

# JS-rendered SPA, custom output directory
site2vault https://spa.example.com --render-js --out ./vault/spa
```

The output folder can be opened directly as an Obsidian vault or dropped into an existing vault.

## How it works

1. **Crawl** -- async HTTP client fetches pages breadth-first, respecting robots.txt, rate limits, and polite defaults.
2. **Extract** -- trafilatura isolates main content, strips images and boilerplate. BS4 fallback for sparse pages.
3. **Convert** -- markdownify turns clean HTML into markdown with placeholder link tokens.
4. **Rewrite** -- second pass replaces placeholders with Obsidian `[[wikilinks]]` for in-scope pages, standard `[markdown](links)` for everything else.
5. **Index** -- generates `Index.md` MOC at vault root with wikilinks to all notes.

## Output structure

```
<out>/
  Index.md                      # Map of Content
  _meta/
    site2vault.sqlite           # resumable state
    site2vault.log              # debug log
    link-index/                 # per-note link sidecars
    headings/                   # per-note heading sidecars
  docs/
    Installation Guide.md
    Configuration.md
  blog/
    First Post.md
```

Every note has YAML frontmatter with title, source URL, retrieval timestamp, and tags.

## CLI options

```
site2vault URL [OPTIONS]

Arguments:
  URL                          Seed URL. Required.

Options:
  --out PATH                   Output directory. Default: ./<domain-slug>/
  --depth INT                  Max crawl depth. Default: 3.
  --max-pages INT              Hard cap on pages. Default: 2000.
  --include PATTERN            Only crawl matching URLs (regex, repeatable).
  --exclude PATTERN            Skip matching URLs (regex, repeatable).
  --same-domain/--any-domain   Stay on seed domain. Default: same-domain.
  --subdomain-policy           strict|include|any. Default: include.
  --rate FLOAT                 Requests per second. Default: 1.0.
  --concurrency INT            Parallel workers. Default: 2.
  --jitter FLOAT               Random delay factor. Default: 0.3.
  --min-delay FLOAT            Min seconds between host requests. Default: 0.5.
  --max-errors INT             Circuit breaker threshold. Default: 10.
  --ignore-robots              Skip robots.txt.
  --render-js                  Use Playwright for JS rendering.
  --user-agent STRING          Override User-Agent.
  --resume/--no-resume         Continue previous run. Default: resume.
  --force                      Re-crawl even if state exists.
  --flat                       All notes at vault root.
  --link-style shortest|path   Wikilink style. Default: shortest.
  --verbose/-v                 Debug logging.
  --dry-run                    Discover URLs only, write no files.
```

## FAQ

**Q: A site blocks the crawler. What should I do?**
A: First, check if the site's `robots.txt` disallows crawling. If so, respect it. If you own the site, try `--rate 10 --concurrency 8`. For Cloudflare-protected sites, try `--render-js`. If blocks persist, the tool will log clear warnings and stop -- don't hammer harder.

**Q: How do I handle JS-rendered sites?**
A: Pass `--render-js`. This uses Playwright with headless Chromium. Install it first with `pip install 'site2vault[js]' && playwright install chromium`. It's much slower than the default httpx client.

**Q: Does it respect robots.txt?**
A: Yes, by default. It reads `robots.txt` per host, respects `Disallow` rules and `Crawl-delay` directives. Use `--ignore-robots` to skip (not recommended).

**Q: How do I open the output in Obsidian?**
A: Open Obsidian, click "Open folder as vault", and select the output directory. The graph view will show all the interconnected notes.

**Q: What about rate limiting?**
A: Default is 1 request/second with 0.3 jitter factor. The crawler adapts: on HTTP 429 it backs off exponentially, on repeated errors a circuit breaker pauses crawling. For your own sites, increase with `--rate` and `--concurrency`.

**Q: Can I resume a cancelled crawl?**
A: Yes. Just run the same command again. State is persisted in `_meta/site2vault.sqlite`. The crawler picks up where it left off. Use `--force` to start fresh.

## Development

```bash
pip install -e ".[dev]"
pytest
```

## License

MIT
