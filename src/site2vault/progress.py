"""Structured progress event emitter.

Two implementations:
- RichEmitter: default, logs via Rich console handler (existing behavior).
- JsonEmitter: --json-progress mode, emits JSONL to stdout for plugin consumption.
"""

import json
import logging
import sys
from datetime import datetime, timezone
from typing import Protocol

log = logging.getLogger("site2vault.progress")


class ProgressEmitter(Protocol):
    """Protocol for progress event emission."""

    def emit(self, event: str, **fields) -> None: ...


class RichEmitter:
    """Default emitter — routes events to the standard logger."""

    def emit(self, event: str, **fields) -> None:
        phase = fields.get("phase", "")
        url = fields.get("url", "")
        status = fields.get("status", "")
        file = fields.get("file", "")
        reason = fields.get("reason", "")
        stats = fields.get("stats", {})

        if event == "run_start":
            log.info("site2vault starting: %s", fields.get("seed_url", ""))
        elif event == "phase_start":
            log.info("Phase: %s", phase)
        elif event == "phase_end":
            if stats:
                log.info("Phase %s complete: %s", phase, stats)
            else:
                log.info("Phase %s complete", phase)
        elif event == "fetch_start":
            log.info("Fetching: %s", url)
        elif event == "fetch_done":
            log.debug("Fetched: %s [%s] %d bytes in %dms",
                       url, status, fields.get("bytes", 0), fields.get("duration_ms", 0))
        elif event == "fetch_failed":
            log.warning("Failed: %s (%s) attempt %d", url, reason, fields.get("attempt", 0))
        elif event == "note_written":
            log.info("Written: %s <- %s", file, url)
        elif event == "run_end":
            exit_code = fields.get("exit_code", 0)
            if exit_code == 0:
                log.info("site2vault finished successfully.")
            else:
                log.info("site2vault finished with exit code %d.", exit_code)
        else:
            log.debug("Event: %s %s", event, fields)


class JsonEmitter:
    """JSONL emitter for --json-progress mode. Writes to stdout."""

    def emit(self, event: str, **fields) -> None:
        record = {
            "event": event,
            "ts": datetime.now(timezone.utc).isoformat(),
            **fields,
        }
        line = json.dumps(record, default=str, ensure_ascii=False)
        sys.stdout.write(line + "\n")
        sys.stdout.flush()


# Global emitter instance — set during logging setup
_emitter: ProgressEmitter = RichEmitter()


def set_emitter(emitter: ProgressEmitter) -> None:
    """Set the global progress emitter."""
    global _emitter
    _emitter = emitter


def get_emitter() -> ProgressEmitter:
    """Get the current global progress emitter."""
    return _emitter


def emit(event: str, **fields) -> None:
    """Emit a progress event through the global emitter."""
    _emitter.emit(event, **fields)
