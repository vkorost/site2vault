"""Logging configuration with rich console and timestamped log file."""

import logging
from datetime import datetime, timezone
from logging.handlers import RotatingFileHandler
from pathlib import Path

from rich.logging import RichHandler


def setup_logging(config: "RunConfig") -> None:  # noqa: F821
    """Configure root logger with rich console + timestamped log file.

    When json_progress is enabled, the Rich console handler is suppressed
    and a JsonEmitter is installed for structured stdout output.
    """
    from site2vault.progress import JsonEmitter, RichEmitter, set_emitter

    level = logging.DEBUG if config.verbose else logging.INFO

    root = logging.getLogger("site2vault")
    root.setLevel(logging.DEBUG)
    root.handlers.clear()

    if config.json_progress:
        # JSON mode: no console handler, events go to stdout via JsonEmitter
        set_emitter(JsonEmitter())
    else:
        # Default: Rich console handler
        console_handler = RichHandler(
            level=level,
            show_time=True,
            show_path=False,
            markup=True,
        )
        console_handler.setFormatter(logging.Formatter("%(message)s"))
        root.addHandler(console_handler)
        set_emitter(RichEmitter())

    # Timestamped log file (always, regardless of mode)
    log_dir = Path(config.out) / "log"
    log_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H-%M-%S")
    log_path = log_dir / f"site2vault-{timestamp}.log"
    file_handler = RotatingFileHandler(
        log_path, maxBytes=10 * 1024 * 1024, backupCount=3, encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s %(levelname)-8s %(name)s %(message)s")
    )
    root.addHandler(file_handler)
