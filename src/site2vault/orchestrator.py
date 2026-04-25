"""Top-level orchestrator that wires crawler, extractor, converter, rewriter, and index."""

import logging

from site2vault.config import RunConfig

log = logging.getLogger("site2vault.orchestrator")


async def run(config: RunConfig) -> None:
    """Execute the full site2vault pipeline."""
    from site2vault.state import StateDB
    from site2vault.robots import RobotsChecker
    from site2vault.crawler import Crawler
    from site2vault.rewrite import rewrite_all
    from site2vault.index import generate_index

    log.info("site2vault starting: %s -> %s", config.seed_url, config.out)

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

    crawler = Crawler(config, db, robots)
    await crawler.crawl()

    if not config.dry_run:
        rewrite_all(config, db)
        generate_index(config, db)

        if config.emit_manifest:
            from site2vault.manifest import build_manifest, write_manifest
            manifest = build_manifest(config, db)
            write_manifest(config, manifest)

    db.close()
    log.info("site2vault finished.")
