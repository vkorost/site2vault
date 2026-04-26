"""Structured exit codes for CLI and plugin consumption.

| Code | Meaning |
|------|---------|
| 0    | Success. All in-scope URLs processed or properly skipped. |
| 1    | Fatal error before crawl could meaningfully start. |
| 2    | Partial success. At least one host hit circuit breaker or anti-bot. |
| 3    | User abort (SIGINT/SIGTERM). |
| 4    | Resume conflict. Existing state DB has incompatible config. |
"""

SUCCESS = 0
FATAL = 1
PARTIAL = 2
USER_ABORT = 3
RESUME_CONFLICT = 4
