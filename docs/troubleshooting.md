# Troubleshooting

## "Crawled 1 page but the site has hundreds"

Likely cause: the seed page uses `<meta http-equiv="refresh">` for redirects, or the navigation is rendered by JavaScript.

Fix:
1. Check the verbose log for "meta refresh" detections
2. If the site is JS-heavy, retry with `--render-js` (requires `pip install 'site2vault[js]'` and `playwright install chromium`)
3. Check `--depth`; the default is 3

## HTTP 403 / Cloudflare blocks

Site2Vault detects anti-bot challenges and stops crawling that host after 3 consecutive hits. The verbose log will name the signal (Cloudflare, CAPTCHA, etc.).

Options:
1. Try `--render-js` — Playwright sometimes solves the JS challenge
2. Slow down: `--rate 0.5 --concurrency 1 --jitter 0.5`
3. Some sites simply do not permit mirroring; respect that

## Crawl hangs or times out

- Set an overall budget: `--timeout 30` (minutes)
- Reduce concurrency: `--concurrency 1`
- Check network: `httpx` errors will appear in verbose mode

## Resume says "config mismatch"

The state DB was created with different settings (different seed URL, different scope flags). Either:
- Use `--force` to override and re-crawl
- Use a different `--name` for the new run
- Use `--namespace` if you want both sites in one vault

## Notes are empty or near-empty

- The page may be a redirect stub; check the verbose log for meta refresh detection
- The page may be behind a consent wall (cookie banner with no content visible)
- The page may be a login wall
- Trafilatura may have under-extracted; the BS4 fallback is automatic but conservative

## Wikilinks point to wrong files

- Verify the URL canonicalization is matching: two URLs that should be the same may differ in trailing slash, www prefix, or tracking params (these should be normalized; if not, file an issue)
- If the target URL was not crawled (failed, skipped, out of scope), the link will remain as a regular external markdown link

## "S2V_LINK_" appears in the final output

This means the rewrite phase did not complete or the link sidecar was missing. Check the log directory for errors. Re-running with `--resume` should retry the rewrite phase.

## Standalone exe is flagged by antivirus

PyInstaller-built exes are sometimes flagged as false positives by Windows Defender and others. Build from source or whitelist the binary.
