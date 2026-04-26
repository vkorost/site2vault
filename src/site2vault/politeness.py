"""Rate limiting, jitter, adaptive backoff, and circuit breaker.

Global token-bucket limiter shared across all workers, with per-host
minimum delay and adaptive backoff on error signals.
"""

import asyncio
import logging
import random
import time
from collections import deque
from dataclasses import dataclass, field

log = logging.getLogger("site2vault.politeness")


class TokenBucket:
    """Global token-bucket rate limiter.

    Tokens refill at `rate` per second. Each fetch consumes one token.
    """

    def __init__(self, rate: float, max_tokens: float | None = None):
        self.rate = rate
        self.max_tokens = max_tokens or max(rate * 2, 1.0)
        self._tokens = self.max_tokens
        self._last_refill = time.monotonic()
        self._lock = asyncio.Lock()

    async def acquire(self) -> None:
        """Wait until a token is available, then consume it."""
        while True:
            async with self._lock:
                self._refill()
                if self._tokens >= 1.0:
                    self._tokens -= 1.0
                    return
            # Wait a short interval before retrying
            wait = 1.0 / self.rate if self.rate > 0 else 1.0
            await asyncio.sleep(min(wait, 0.1))

    def _refill(self) -> None:
        now = time.monotonic()
        elapsed = now - self._last_refill
        self._tokens = min(self.max_tokens, self._tokens + elapsed * self.rate)
        self._last_refill = now

    def set_rate(self, new_rate: float) -> None:
        """Update the refill rate."""
        self._refill()
        self.rate = new_rate


class PerHostDelay:
    """Enforces minimum delay between requests to the same host."""

    def __init__(self, min_delay: float):
        self.min_delay = min_delay
        self._last_request: dict[str, float] = {}
        self._lock = asyncio.Lock()

    async def wait(self, host: str) -> None:
        """Wait until min_delay has passed since last request to this host."""
        async with self._lock:
            now = time.monotonic()
            last = self._last_request.get(host, 0.0)
            wait_time = self.min_delay - (now - last)
            if wait_time > 0:
                await asyncio.sleep(wait_time)
            self._last_request[host] = time.monotonic()

    def update_min_delay(self, host: str, new_delay: float) -> None:
        """Update min delay for a specific host (e.g. from Crawl-delay)."""
        self.min_delay = max(self.min_delay, new_delay)


@dataclass
class HostState:
    """Tracks error signals and backoff state for a single host."""
    recent_results: deque = field(default_factory=lambda: deque(maxlen=50))
    consecutive_errors: int = 0
    consecutive_429s: int = 0
    circuit_open_count: int = 0
    rate_halved: bool = False
    rate_halved_at: float = 0.0
    successes_since_halve: int = 0
    original_rate: float = 1.0
    backoff_until: float = 0.0
    stopped: bool = False
    consecutive_antibot: int = 0


class PolitenessManager:
    """Coordinates all politeness mechanisms."""

    def __init__(self, rate: float, concurrency: int, jitter: float,
                 min_delay: float, max_errors: int):
        self.rate = rate
        self.jitter = jitter
        self.max_errors = max_errors
        self.bucket = TokenBucket(rate)
        self.per_host = PerHostDelay(min_delay)
        self._host_states: dict[str, HostState] = {}
        self._lock = asyncio.Lock()

    def _get_host_state(self, host: str) -> HostState:
        if host not in self._host_states:
            self._host_states[host] = HostState(original_rate=self.rate)
        return self._host_states[host]

    async def wait_for_slot(self, host: str) -> bool:
        """Wait for permission to make a request to the given host.

        Returns False if the host is stopped (circuit permanently open).
        """
        state = self._get_host_state(host)

        if state.stopped:
            return False

        # Check backoff
        now = time.monotonic()
        if state.backoff_until > now:
            wait = state.backoff_until - now
            log.debug("Host %s in backoff, waiting %.1fs", host, wait)
            await asyncio.sleep(wait)

        # Global token bucket
        await self.bucket.acquire()

        # Per-host delay
        await self.per_host.wait(host)

        # Jitter
        if self.jitter > 0 and self.rate > 0:
            jitter_delay = self.jitter * (1.0 / self.rate) * random.random()
            await asyncio.sleep(jitter_delay)

        return True

    async def record_success(self, host: str) -> None:
        """Record a successful request."""
        async with self._lock:
            state = self._get_host_state(host)
            state.recent_results.append("ok")
            state.consecutive_errors = 0
            state.consecutive_429s = 0
            state.consecutive_antibot = 0

            # Gradual rate restoration after halving
            if state.rate_halved:
                state.successes_since_halve += 1
                if state.successes_since_halve >= 20:
                    # Restore full rate gradually (10% per 10 successes)
                    restored = min(
                        state.original_rate,
                        self.bucket.rate + state.original_rate * 0.1
                    )
                    self.bucket.set_rate(restored)
                    if restored >= state.original_rate:
                        state.rate_halved = False
                        log.info("Host %s: rate restored to %.1f", host, restored)

    async def record_error(self, host: str, status_code: int | None = None,
                           retry_after: float | None = None) -> None:
        """Record an error and apply backoff/circuit-breaking logic."""
        async with self._lock:
            state = self._get_host_state(host)
            state.recent_results.append("error")
            state.consecutive_errors += 1

            if status_code == 429:
                await self._handle_429(host, state, retry_after)
            elif status_code == 503:
                await self._handle_503(host, state, retry_after)
            elif status_code is None:  # Connection error / timeout
                await self._handle_connection_error(host, state)

            # Circuit breaker check
            self._check_circuit(host, state)

    async def record_antibot(self, host: str) -> bool:
        """Record an anti-bot detection. Returns True if host should be stopped."""
        async with self._lock:
            state = self._get_host_state(host)
            state.consecutive_antibot += 1
            if state.consecutive_antibot >= 3:
                state.stopped = True
                log.warning(
                    "Host %s: 3 consecutive anti-bot hits, stopping crawl. "
                    "Try --render-js or inspect the site's terms.", host
                )
                return True
            return False

    async def _handle_429(self, host: str, state: HostState,
                          retry_after: float | None) -> None:
        """Handle HTTP 429 Too Many Requests."""
        state.consecutive_429s += 1

        if retry_after is not None:
            delay = retry_after
        else:
            # Exponential backoff: 2, 4, 8, 16, 30
            delay = min(2 ** state.consecutive_429s, 30)

        state.backoff_until = time.monotonic() + delay
        log.warning("Host %s: 429, backing off %.1fs", host, delay)

        # Halve rate for 5 minutes
        if not state.rate_halved:
            state.rate_halved = True
            state.rate_halved_at = time.monotonic()
            state.successes_since_halve = 0
            new_rate = self.bucket.rate / 2
            self.bucket.set_rate(max(new_rate, 0.1))
            log.warning("Host %s: halving rate to %.2f", host, new_rate)

    async def _handle_503(self, host: str, state: HostState,
                          retry_after: float | None) -> None:
        """Handle HTTP 503 Service Unavailable."""
        if retry_after is not None:
            state.backoff_until = time.monotonic() + retry_after
        else:
            # Treat like 429
            await self._handle_429(host, state, None)

    async def _handle_connection_error(self, host: str, state: HostState) -> None:
        """Handle connection reset / timeout."""
        if state.consecutive_errors >= 3:
            state.backoff_until = time.monotonic() + 60
            log.warning("Host %s: 3 consecutive connection errors, backing off 60s", host)
            if not state.rate_halved:
                state.rate_halved = True
                state.rate_halved_at = time.monotonic()
                state.successes_since_halve = 0
                new_rate = self.bucket.rate / 2
                self.bucket.set_rate(max(new_rate, 0.1))

    def _check_circuit(self, host: str, state: HostState) -> None:
        """Check if circuit breaker should trip."""
        error_count = sum(1 for r in state.recent_results if r == "error")
        if error_count >= self.max_errors:
            state.circuit_open_count += 1
            if state.circuit_open_count >= 2:
                state.stopped = True
                log.error(
                    "Host %s: circuit opened twice, permanently stopping", host
                )
            else:
                state.backoff_until = time.monotonic() + 60
                log.warning(
                    "Host %s: circuit open (%d errors in last %d), "
                    "pausing 60s",
                    host, error_count, len(state.recent_results),
                )
            # Clear the window
            state.recent_results.clear()

    def is_host_stopped(self, host: str) -> bool:
        """Check if a host is permanently stopped."""
        state = self._host_states.get(host)
        return state.stopped if state else False

    def get_host_state(self, host: str) -> HostState | None:
        return self._host_states.get(host)
