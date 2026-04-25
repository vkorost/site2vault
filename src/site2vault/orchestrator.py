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

    db = StateDB(config.out)
    db.initialize()

    if not config.force and db.has_existing_run():
        if not db.config_matches(config):
            log.error("Existing run config mismatch. Use --force to override.")
            emit("run_end", exit_code=exit_codes.RESUME_CONFLICT, stats={})
            db.close()
            return exit_codes.RESUME_CONFLICT

    db.save_config(config)

    robots = RobotsChecker(config)
    await robots.load_seed()

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
        # Phase 2: Rewrite
        emit("phase_start", phase="rewrite")
        rewrite_all(config, db)
        emit("phase_end", phase="rewrite")

        # Phase 3: Index
        emit("phase_start", phase="index")
        generate_index(config, db)
        emit("phase_end", phase="index")

        # Phase 4: Manifest
        if config.emit_manifest:
            emit("phase_start", phase="manifest")
            from site2vault.manifest import build_manifest, write_manifest
            manifest = build_manifest(config, db)
            write_manifest(config, manifest)
            emit("phase_end", phase="manifest")

    # Determine exit code
    code = exit_codes.SUCCESS
    if crawler.has_stopped_hosts():
        code = exit_codes.PARTIAL

    db.close()
    emit("run_end", exit_code=code, stats=crawl_stats)
    return code
