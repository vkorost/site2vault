"""SQLite state database for resumable crawls."""

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from site2vault.config import RunConfig

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS run_config (
    key TEXT PRIMARY KEY,
    value TEXT
);
CREATE TABLE IF NOT EXISTS frontier (
    url TEXT PRIMARY KEY,
    depth INTEGER,
    discovered_from TEXT,
    status TEXT CHECK(status IN ('pending','in_progress','done','failed','skipped')),
    error TEXT,
    updated_at TEXT
);
CREATE TABLE IF NOT EXISTS url_notes (
    url TEXT PRIMARY KEY,
    filename TEXT NOT NULL,
    folder_path TEXT,
    title TEXT,
    content_hash TEXT,
    fetched_at TEXT,
    status TEXT
);
CREATE TABLE IF NOT EXISTS redirects (
    from_url TEXT PRIMARY KEY,
    to_url TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS host_stats (
    host TEXT PRIMARY KEY,
    requests INTEGER DEFAULT 0,
    errors INTEGER DEFAULT 0,
    last_429_at TEXT,
    current_rate REAL,
    backoff_until TEXT
);
CREATE INDEX IF NOT EXISTS idx_frontier_status ON frontier(status);
CREATE INDEX IF NOT EXISTS idx_url_notes_filename ON url_notes(filename);
"""

MIGRATION_SQL = """
-- Add etag and last_modified columns if they don't exist
ALTER TABLE url_notes ADD COLUMN etag TEXT;
ALTER TABLE url_notes ADD COLUMN last_modified TEXT;
"""


class StateDB:
    """SQLite-backed state for site2vault crawl runs."""

    def __init__(self, out_dir: Path | str):
        self.out_dir = Path(out_dir)
        self.meta_dir = self.out_dir / "log"
        self.db_path = self.meta_dir / "site2vault.sqlite"
        self._conn: sqlite3.Connection | None = None

    @property
    def conn(self) -> sqlite3.Connection:
        if self._conn is None:
            self.meta_dir.mkdir(parents=True, exist_ok=True)
            self._conn = sqlite3.connect(str(self.db_path))
            self._conn.row_factory = sqlite3.Row
            self._conn.execute("PRAGMA journal_mode=WAL")
            self._conn.execute("PRAGMA foreign_keys=ON")
        return self._conn

    def initialize(self) -> None:
        """Create tables if they don't exist."""
        self.conn.executescript(SCHEMA_SQL)
        self._migrate()

    def _migrate(self) -> None:
        """Apply schema migrations."""
        # Check if etag column exists
        cursor = self.conn.execute("PRAGMA table_info(url_notes)")
        columns = {row[1] for row in cursor.fetchall()}
        if "etag" not in columns:
            self.conn.execute("ALTER TABLE url_notes ADD COLUMN etag TEXT")
            self.conn.execute("ALTER TABLE url_notes ADD COLUMN last_modified TEXT")
            self.conn.commit()

    def close(self) -> None:
        if self._conn:
            self._conn.close()
            self._conn = None

    # --- Run config ---

    def save_config(self, config: RunConfig) -> None:
        """Persist run config as key-value pairs."""
        config_dict = {
            "seed_url": config.seed_url,
            "depth": str(config.depth),
            "max_pages": str(config.max_pages),
            "same_domain": str(config.same_domain),
            "subdomain_policy": config.subdomain_policy,
            "include": json.dumps(config.include),
            "exclude": json.dumps(config.exclude),
            "flat": str(config.flat),
            "link_style": config.link_style,
        }
        for key, value in config_dict.items():
            self.conn.execute(
                "INSERT OR REPLACE INTO run_config (key, value) VALUES (?, ?)",
                (key, value),
            )
        self.conn.commit()

    def has_existing_run(self) -> bool:
        """Check if there's an existing crawl state."""
        row = self.conn.execute("SELECT COUNT(*) FROM run_config").fetchone()
        return row[0] > 0

    def config_matches(self, config: RunConfig) -> bool:
        """Check if existing config matches the new one."""
        row = self.conn.execute(
            "SELECT value FROM run_config WHERE key = 'seed_url'"
        ).fetchone()
        if row is None:
            return True
        return row[0] == config.seed_url

    # --- Frontier ---

    def add_to_frontier(
        self, url: str, depth: int, discovered_from: str | None = None
    ) -> bool:
        """Add a URL to the frontier. Returns True if newly added."""
        try:
            self.conn.execute(
                """INSERT INTO frontier (url, depth, discovered_from, status, updated_at)
                   VALUES (?, ?, ?, 'pending', ?)""",
                (url, depth, discovered_from, _now()),
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def get_pending_urls(self, limit: int) -> list[dict]:
        """Get up to `limit` pending URLs ordered by depth then discovery order."""
        rows = self.conn.execute(
            """SELECT url, depth, discovered_from FROM frontier
               WHERE status = 'pending'
               ORDER BY depth ASC, rowid ASC
               LIMIT ?""",
            (limit,),
        ).fetchall()
        return [dict(r) for r in rows]

    def mark_in_progress(self, url: str) -> None:
        self.conn.execute(
            "UPDATE frontier SET status = 'in_progress', updated_at = ? WHERE url = ?",
            (_now(), url),
        )
        self.conn.commit()

    def mark_done(self, url: str) -> None:
        self.conn.execute(
            "UPDATE frontier SET status = 'done', updated_at = ? WHERE url = ?",
            (_now(), url),
        )
        self.conn.commit()

    def mark_failed(self, url: str, error: str) -> None:
        self.conn.execute(
            "UPDATE frontier SET status = 'failed', error = ?, updated_at = ? WHERE url = ?",
            (error, _now(), url),
        )
        self.conn.commit()

    def mark_skipped(self, url: str, reason: str) -> None:
        self.conn.execute(
            "UPDATE frontier SET status = 'skipped', error = ?, updated_at = ? WHERE url = ?",
            (reason, _now(), url),
        )
        self.conn.commit()

    def reset_in_progress(self) -> int:
        """Reset any in_progress URLs back to pending (for resume after crash)."""
        cur = self.conn.execute(
            "UPDATE frontier SET status = 'pending', updated_at = ? WHERE status = 'in_progress'",
            (_now(),),
        )
        self.conn.commit()
        return cur.rowcount

    def requeue_done_for_refresh(self) -> int:
        """Re-queue all done URLs as pending for refresh crawl."""
        cur = self.conn.execute(
            "UPDATE frontier SET status = 'pending', updated_at = ? WHERE status = 'done'",
            (_now(),),
        )
        self.conn.commit()
        return cur.rowcount

    def get_failed_urls(self) -> list[dict]:
        """Get all failed URLs with their error reasons."""
        rows = self.conn.execute(
            "SELECT url, error FROM frontier WHERE status = 'failed'"
        ).fetchall()
        return [dict(r) for r in rows]

    def count_done(self) -> int:
        row = self.conn.execute(
            "SELECT COUNT(*) FROM frontier WHERE status = 'done'"
        ).fetchone()
        return row[0]

    def count_by_status(self) -> dict[str, int]:
        rows = self.conn.execute(
            "SELECT status, COUNT(*) FROM frontier GROUP BY status"
        ).fetchall()
        return {r[0]: r[1] for r in rows}

    def url_in_frontier(self, url: str) -> bool:
        row = self.conn.execute(
            "SELECT 1 FROM frontier WHERE url = ?", (url,)
        ).fetchone()
        return row is not None

    # --- URL Notes ---

    def save_note(
        self,
        url: str,
        filename: str,
        folder_path: str,
        title: str | None,
        content_hash: str,
        status: str = "done",
        etag: str | None = None,
        last_modified: str | None = None,
    ) -> None:
        self.conn.execute(
            """INSERT OR REPLACE INTO url_notes
               (url, filename, folder_path, title, content_hash, fetched_at, status, etag, last_modified)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (url, filename, folder_path, title, content_hash, _now(), status, etag, last_modified),
        )
        self.conn.commit()

    def get_note_by_url(self, url: str) -> dict | None:
        row = self.conn.execute(
            "SELECT * FROM url_notes WHERE url = ?", (url,)
        ).fetchone()
        return dict(row) if row else None

    def get_all_notes(self) -> list[dict]:
        rows = self.conn.execute("SELECT * FROM url_notes").fetchall()
        return [dict(r) for r in rows]

    def get_all_filenames(self) -> set[str]:
        rows = self.conn.execute("SELECT filename FROM url_notes").fetchall()
        return {r[0] for r in rows}

    def get_conditional_headers(self, url: str) -> dict[str, str]:
        """Get If-None-Match / If-Modified-Since headers for a URL."""
        row = self.conn.execute(
            "SELECT etag, last_modified FROM url_notes WHERE url = ?", (url,)
        ).fetchone()
        headers = {}
        if row:
            if row["etag"]:
                headers["If-None-Match"] = row["etag"]
            if row["last_modified"]:
                headers["If-Modified-Since"] = row["last_modified"]
        return headers

    def get_content_hashes(self) -> set[str]:
        rows = self.conn.execute(
            "SELECT content_hash FROM url_notes WHERE content_hash IS NOT NULL"
        ).fetchall()
        return {r[0] for r in rows}

    # --- Redirects ---

    def save_redirect(self, from_url: str, to_url: str) -> None:
        self.conn.execute(
            "INSERT OR REPLACE INTO redirects (from_url, to_url) VALUES (?, ?)",
            (from_url, to_url),
        )
        self.conn.commit()

    def resolve_redirect(self, url: str) -> str:
        """Follow redirect chain to final URL."""
        visited = set()
        current = url
        while True:
            if current in visited:
                break
            visited.add(current)
            row = self.conn.execute(
                "SELECT to_url FROM redirects WHERE from_url = ?", (current,)
            ).fetchone()
            if row is None:
                break
            current = row[0]
        return current

    # --- Host Stats ---

    def update_host_stats(
        self, host: str, requests_delta: int = 0, errors_delta: int = 0
    ) -> None:
        self.conn.execute(
            """INSERT INTO host_stats (host, requests, errors)
               VALUES (?, ?, ?)
               ON CONFLICT(host) DO UPDATE SET
                   requests = requests + excluded.requests,
                   errors = errors + excluded.errors""",
            (host, requests_delta, errors_delta),
        )
        self.conn.commit()

    def get_host_stats(self, host: str) -> dict | None:
        row = self.conn.execute(
            "SELECT * FROM host_stats WHERE host = ?", (host,)
        ).fetchone()
        return dict(row) if row else None

    def set_host_backoff(self, host: str, until: str) -> None:
        self.conn.execute(
            """UPDATE host_stats SET backoff_until = ? WHERE host = ?""",
            (until, host),
        )
        self.conn.commit()

    def set_host_rate(self, host: str, rate: float) -> None:
        self.conn.execute(
            """UPDATE host_stats SET current_rate = ? WHERE host = ?""",
            (rate, host),
        )
        self.conn.commit()

    def get_all_host_stats(self) -> list[dict]:
        rows = self.conn.execute("SELECT * FROM host_stats").fetchall()
        return [dict(r) for r in rows]


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()
