"""Top-level orchestrator that wires crawler, extractor, converter, rewriter, and index."""

import asyncio
import logging
import signal
import sys

from site2vault import exit_codes
from site2vault.config import RunConfig
from site2vault.progress import emit

log = logging.getLogger("site2vault.orchestrator")

# Sentinel for SIGINT/SIGTERM
_abort_requested = False


def _handle_signal(signum, frame):
    global _abort_requested
    _abort_requested = True
    log.warning("Received signal %d, initiating graceful shutdown...", signum)


async def run(config: RunConfig) -> int:
    """Execute the full site2vault pipeline.

    Returns:
        Exit code per exit_codes module.
    """
    from site2vault.state import StateDB
    from site2vault.robots import RobotsChecker
    from site2vault.crawler import Crawler
    from site2vault.rewrite import rewrite_all
    from site2vault.index import generate_index

    # Install signal handlers
    if sys.platform != "win32":
        loop = asyncio.get_running_loop()
        loop.add_signal_handler(signal.SIGINT, _handle_signal, signal.SIGINT, None)
        loop.add_signal_handler(signal.SIGTERM, _handle_signal, signal.SIGTERM, None)
    else:
        signal.signal(signal.SIGINT, _handle_signal)

    emit("run_start", seed_url=config.seed_url, config={
        "seed_url": config.seed_url,
        "out": str(config.out),
        "depth": config.depth,
        "max_pages": config.max_pages,
    })

    # Namespace handling: redirect output into subdirectory
    vault_root = config.out  # Preserve for index.json
    if config.namespace:
        from dataclasses import replace
        config = replace(config, out=config.out / config.namespace)
        config.out.mkdir(parents=True, exist_ok=True)

    db = StateDB(config.out)
    db.initialize()

    if not config.force and db.has_existing_run():
        if not db.config_matches(config):
            log.error("Existing run config mismatch. Use --force to override.")
            emit("run_end", exit_code=exit_codes.RESUME_CONFLICT, stats={})
            db.close()
            return exit_codes.RESUME_CONFLICT

    db.save_config(config)

    # Refresh mode: re-queue done URLs
    if config.refresh:
        requeued = db.requeue_done_for_refresh()
        log.info("Refresh mode: re-queued %d URLs for conditional GET", requeued)

    robots = RobotsChecker(config)
    await robots.load_seed()

    # Sitemap seeding
    if config.use_sitemap:
        await _seed_from_sitemap(config, db, robots)

    # Phase 1: Crawl
    emit("phase_start", phase="crawl")
    crawler = Crawler(config, db, robots)
    await crawler.crawl()
    crawl_stats = db.count_by_status()
    emit("phase_end", phase="crawl", stats=crawl_stats)

    if _abort_requested:
        emit("run_end", exit_code=exit_codes.USER_ABORT, stats=crawl_stats)
        db.close()
        return exit_codes.USER_ABORT

    if not config.dry_run:
        # Phase 1.5: Cross-page boilerplate detection
        if config.cross_page_boilerplate:
            from site2vault.boilerplate import (
                detect_cross_page_boilerplate,
                remove_cross_page_boilerplate,
            )
            notes_for_bp = db.get_all_notes()
            emit("phase_start", phase="deboilerplate")
            flagged = detect_cross_page_boilerplate(
                notes_for_bp, config.out, threshold=config.boilerplate_threshold,
            )
            if flagged:
                modified = remove_cross_page_boilerplate(notes_for_bp, config.out, flagged)
                emit("phase_end", phase="deboilerplate", stats={
                    "flagged_patterns": len(flagged),
                    "notes_modified": modified,
                })
            else:
                emit("phase_end", phase="deboilerplate", stats={"flagged_patterns": 0})

        # Phase 2: Rewrite
        emit("phase_start", phase="rewrite")
        rewrite_all(config, db)
        emit("phase_end", phase="rewrite")

        # Phase 2.5: Heading byte offsets (must be after rewrite)
        from site2vault.chunking import compute_heading_offsets
        notes_for_offsets = db.get_all_notes()
        compute_heading_offsets(notes_for_offsets, config.out, config.out / "log")

        # Phase 3: Index
        # In single-page mode, skip index if vault has only one note
        notes = db.get_all_notes()
        if not config.single or len(notes) > 1:
            emit("phase_start", phase="index")
            generate_index(config, db)
            emit("phase_end", phase="index")

        # Refresh pruning: handle 404/410 URLs
        if config.refresh:
            _handle_refresh_removals(config, db)

        # Phase 4: Manifest
        if config.emit_manifest:
            emit("phase_start", phase="manifest")
            from site2vault.manifest import build_manifest, write_manifest
            manifest = build_manifest(config, db)
            if config.namespace:
                # Namespaced: write to .site2vault/<namespace>/manifest.json
                _write_namespaced_manifest(vault_root, config.namespace, config, manifest)
                _update_namespace_index(vault_root, config.namespace, config.seed_url)
            elif config.single:
                _merge_manifest(config, manifest)
            else:
                write_manifest(config, manifest)
            emit("phase_end", phase="manifest")

    # Determine exit code
    code = exit_codes.SUCCESS
    if crawler.has_stopped_hosts():
        code = exit_codes.PARTIAL

    db.close()
    emit("run_end", exit_code=code, stats=crawl_stats)
    return code


async def _seed_from_sitemap(config: RunConfig, db, robots) -> None:
    """Discover and parse sitemaps, seeding the frontier with discovered URLs."""
    import httpx
    from site2vault.sitemap import discover_sitemaps, parse_sitemap
    from site2vault.canonical import canonicalize
    from urllib.parse import urlparse

    robots_urls = robots.get_sitemap_urls()

    try:
        async with httpx.AsyncClient(
            timeout=httpx.Timeout(15.0),
            follow_redirects=True,
        ) as client:
            sitemap_urls = await discover_sitemaps(
                config.seed_url, client, robots_urls
            )

            if not sitemap_urls:
                log.debug("No sitemaps found")
                return

            # Compute seed path prefix for scope filtering
            seed_parsed = urlparse(config.seed_url)
            seed_path = seed_parsed.path or "/"
            if seed_path.endswith("/"):
                seed_path_prefix = seed_path
            else:
                seed_path_prefix = seed_path.rsplit("/", 1)[0] + "/"

            seed_count = 0
            for sitemap_url in sitemap_urls:
                entries = await parse_sitemap(sitemap_url, client)

                for entry in entries:
                    canonical = canonicalize(entry.loc, config.seed_url)

                    # Scope check: same domain + path prefix
                    if config.same_domain:
                        seed_host = (seed_parsed.hostname or "").lower()
                        entry_parsed = urlparse(canonical)
                        entry_host = (entry_parsed.hostname or "").lower()
                        if config.subdomain_policy == "strict":
                            if entry_host != seed_host:
                                continue
                        elif config.subdomain_policy == "include":
                            if entry_host != seed_host and not entry_host.endswith(f".{seed_host}"):
                                continue

                        # Path prefix: reject URLs outside the seed's directory
                        entry_path = entry_parsed.path or "/"
                        if not entry_path.startswith(seed_path_prefix):
                            continue

                    if db.add_to_frontier(canonical, depth=0):
                        seed_count += 1

                emit("sitemap_discovered", url=sitemap_url, url_count=seed_count)

            if seed_count:
                log.info("Sitemap seeding: added %d URLs to frontier", seed_count)

    except Exception as e:
        log.warning("Sitemap discovery failed: %s (continuing with link discovery)", e)


def _merge_manifest(config: RunConfig, new_manifest: dict) -> None:
    """Merge new notes into an existing manifest (for --single mode)."""
    import json
    from site2vault.manifest import write_manifest

    manifest_path = config.out / ".site2vault" / "manifest.json"
    if manifest_path.exists():
        try:
            existing = json.loads(manifest_path.read_text(encoding="utf-8"))
            # Merge notes: replace existing entries by URL, add new ones
            existing_by_url = {n["url"]: n for n in existing.get("notes", [])}
            for note in new_manifest.get("notes", []):
                existing_by_url[note["url"]] = note
            existing["notes"] = list(existing_by_url.values())
            # Update stats
            existing["stats"]["note_count"] = len(existing["notes"])
            total_wc = sum(n.get("word_count", 0) for n in existing["notes"])
            existing["stats"]["total_word_count"] = total_wc
            existing["stats"]["estimated_total_tokens"] = round(total_wc * 1.33)
            existing["crawled_at"] = new_manifest["crawled_at"]
            write_manifest(config, existing)
            return
        except (json.JSONDecodeError, KeyError):
            pass

    write_manifest(config, new_manifest)


def _write_namespaced_manifest(
    vault_root: "Path", namespace: str, config: RunConfig, manifest: dict
) -> None:
    """Write manifest to .site2vault/<namespace>/manifest.json."""
    import json

    ns_dir = vault_root / ".site2vault" / namespace
    ns_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = ns_dir / "manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    log.info("Namespaced manifest written: %s (%d notes)", manifest_path, len(manifest["notes"]))


def _update_namespace_index(
    vault_root: "Path", namespace: str, seed_url: str
) -> None:
    """Write/update .site2vault/index.json with namespace registry."""
    import json
    from datetime import datetime, timezone

    index_path = vault_root / ".site2vault" / "index.json"
    if index_path.exists():
        try:
            index = json.loads(index_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, KeyError):
            index = {"namespaces": {}}
    else:
        (vault_root / ".site2vault").mkdir(parents=True, exist_ok=True)
        index = {"namespaces": {}}

    index["namespaces"][namespace] = {
        "seed_url": seed_url,
        "manifest": f"{namespace}/manifest.json",
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }

    index_path.write_text(
        json.dumps(index, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    log.info("Namespace index updated: %s", index_path)


def _handle_refresh_removals(config: RunConfig, db) -> None:
    """Handle URLs that returned 404/410 during refresh.

    With --prune: delete the note files.
    Without --prune: log warnings only.
    """
    from pathlib import Path

    failed_urls = db.get_failed_urls()
    removed_codes = {"http_404", "http_410"}
    removed_urls = [f for f in failed_urls if f.get("error") in removed_codes]

    if not removed_urls:
        return

    for entry in removed_urls:
        url = entry["url"]
        note = db.get_note_by_url(url)
        if not note:
            continue

        folder = note.get("folder_path") or ""
        fn = note["filename"]
        if folder:
            note_path = Path(config.out) / folder / f"{fn}.md"
        else:
            note_path = Path(config.out) / f"{fn}.md"

        if config.prune:
            if note_path.exists():
                note_path.unlink()
                log.info("Pruned: %s (URL returned %s)", note_path, entry["error"])
        else:
            log.warning("URL removed from site: %s (%s) — use --prune to delete", url, entry["error"])
