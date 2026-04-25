"""Top-level orchestrator that wires crawler, extractor, converter, rewriter, and index."""

import logging

from site2vault.config import RunConfig
from site2vault.progress import emit

log = logging.getLogger("site2vault.orchestrator")


async def run(config: RunConfig) -> int:
    """Execute the full site2vault pipeline.

    Returns:
        Exit code (0 = success).
    """
    from site2vault.state import StateDB
    from site2vault.robots import RobotsChecker
    from site2vault.crawler import Crawler
    from site2vault.rewrite import rewrite_all
    from site2vault.index import generate_index

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
            if not config.force:
                log.error(
                    "Existing run config mismatch. Use --force to override."
                )
                raise SystemExit(1)

    db.save_config(config)

    robots = RobotsChecker(config)
    await robots.load_seed()

    # Phase 1: Crawl
    emit("phase_start", phase="crawl")
    crawler = Crawler(config, db, robots)
    await crawler.crawl()
    crawl_stats = db.count_by_status()
    emit("phase_end", phase="crawl", stats=crawl_stats)

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

    db.close()

    final_stats = crawl_stats
    emit("run_end", exit_code=0, stats=final_stats)
    return 0
