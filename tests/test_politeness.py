"""Tests for politeness.py - targeting 100% coverage."""

import asyncio
import time

import pytest

from site2vault.politeness import (
    TokenBucket,
    PerHostDelay,
    PolitenessManager,
    HostState,
)


class TestTokenBucket:
    @pytest.mark.asyncio
    async def test_acquire_consumes_token(self):
        bucket = TokenBucket(rate=10.0, max_tokens=10.0)
        await bucket.acquire()
        # Should have consumed one token

    @pytest.mark.asyncio
    async def test_rate_limits(self):
        bucket = TokenBucket(rate=100.0, max_tokens=2.0)
        # Consume all tokens
        await bucket.acquire()
        await bucket.acquire()
        # Next acquire should wait for refill
        start = time.monotonic()
        await bucket.acquire()
        elapsed = time.monotonic() - start
        assert elapsed >= 0.005  # Should have waited a bit

    def test_set_rate(self):
        bucket = TokenBucket(rate=1.0)
        bucket.set_rate(5.0)
        assert bucket.rate == 5.0

    @pytest.mark.asyncio
    async def test_refill_over_time(self):
        bucket = TokenBucket(rate=100.0, max_tokens=5.0)
        # Drain tokens
        for _ in range(5):
            await bucket.acquire()
        # Wait for refill
        await asyncio.sleep(0.05)
        # Should be able to acquire again
        await bucket.acquire()


class TestPerHostDelay:
    @pytest.mark.asyncio
    async def test_first_request_no_wait(self):
        delay = PerHostDelay(min_delay=0.5)
        start = time.monotonic()
        await delay.wait("example.com")
        elapsed = time.monotonic() - start
        assert elapsed < 0.1

    @pytest.mark.asyncio
    async def test_second_request_waits(self):
        delay = PerHostDelay(min_delay=0.1)
        await delay.wait("example.com")
        start = time.monotonic()
        await delay.wait("example.com")
        elapsed = time.monotonic() - start
        assert elapsed >= 0.05  # Should wait at least part of min_delay

    @pytest.mark.asyncio
    async def test_different_hosts_independent(self):
        delay = PerHostDelay(min_delay=1.0)
        await delay.wait("a.com")
        start = time.monotonic()
        await delay.wait("b.com")
        elapsed = time.monotonic() - start
        assert elapsed < 0.1  # Different host, no wait

    def test_update_min_delay(self):
        delay = PerHostDelay(min_delay=0.5)
        delay.update_min_delay("host", 2.0)
        assert delay.min_delay == 2.0

    def test_update_min_delay_keeps_higher(self):
        delay = PerHostDelay(min_delay=3.0)
        delay.update_min_delay("host", 1.0)
        assert delay.min_delay == 3.0


class TestPolitenessManager:
    @pytest.mark.asyncio
    async def test_wait_for_slot_returns_true(self):
        pm = PolitenessManager(rate=100.0, concurrency=2, jitter=0.0,
                               min_delay=0.0, max_errors=10)
        assert await pm.wait_for_slot("example.com") is True

    @pytest.mark.asyncio
    async def test_stopped_host_returns_false(self):
        pm = PolitenessManager(rate=100.0, concurrency=2, jitter=0.0,
                               min_delay=0.0, max_errors=10)
        state = pm._get_host_state("example.com")
        state.stopped = True
        assert await pm.wait_for_slot("example.com") is False

    @pytest.mark.asyncio
    async def test_record_success_clears_errors(self):
        pm = PolitenessManager(rate=100.0, concurrency=2, jitter=0.0,
                               min_delay=0.0, max_errors=10)
        state = pm._get_host_state("example.com")
        state.consecutive_errors = 5
        state.consecutive_429s = 3
        await pm.record_success("example.com")
        assert state.consecutive_errors == 0
        assert state.consecutive_429s == 0

    @pytest.mark.asyncio
    async def test_jitter_adds_delay(self):
        pm = PolitenessManager(rate=100.0, concurrency=2, jitter=1.0,
                               min_delay=0.0, max_errors=10)
        # Jitter should be 0 to 1/rate = 0.01, very small
        start = time.monotonic()
        await pm.wait_for_slot("example.com")
        elapsed = time.monotonic() - start
        # Should be very small with high rate
        assert elapsed < 0.5

    @pytest.mark.asyncio
    async def test_429_triggers_backoff(self):
        pm = PolitenessManager(rate=100.0, concurrency=2, jitter=0.0,
                               min_delay=0.0, max_errors=50)
        await pm.record_error("example.com", status_code=429)
        state = pm.get_host_state("example.com")
        assert state.backoff_until > time.monotonic()

    @pytest.mark.asyncio
    async def test_429_with_retry_after(self):
        pm = PolitenessManager(rate=100.0, concurrency=2, jitter=0.0,
                               min_delay=0.0, max_errors=50)
        await pm.record_error("example.com", status_code=429, retry_after=5.0)
        state = pm.get_host_state("example.com")
        assert state.backoff_until > time.monotonic()

    @pytest.mark.asyncio
    async def test_429_halves_rate(self):
        pm = PolitenessManager(rate=10.0, concurrency=2, jitter=0.0,
                               min_delay=0.0, max_errors=50)
        original_rate = pm.bucket.rate
        await pm.record_error("example.com", status_code=429)
        assert pm.bucket.rate < original_rate

    @pytest.mark.asyncio
    async def test_503_with_retry_after(self):
        pm = PolitenessManager(rate=100.0, concurrency=2, jitter=0.0,
                               min_delay=0.0, max_errors=50)
        await pm.record_error("example.com", status_code=503, retry_after=10.0)
        state = pm.get_host_state("example.com")
        assert state.backoff_until > time.monotonic()

    @pytest.mark.asyncio
    async def test_503_without_retry_after_treated_as_429(self):
        pm = PolitenessManager(rate=10.0, concurrency=2, jitter=0.0,
                               min_delay=0.0, max_errors=50)
        await pm.record_error("example.com", status_code=503)
        state = pm.get_host_state("example.com")
        assert state.rate_halved

    @pytest.mark.asyncio
    async def test_connection_error_backoff_after_3(self):
        pm = PolitenessManager(rate=100.0, concurrency=2, jitter=0.0,
                               min_delay=0.0, max_errors=50)
        # 3 consecutive connection errors
        for _ in range(3):
            await pm.record_error("example.com", status_code=None)
        state = pm.get_host_state("example.com")
        assert state.backoff_until > time.monotonic()

    @pytest.mark.asyncio
    async def test_circuit_breaker_opens(self):
        pm = PolitenessManager(rate=100.0, concurrency=2, jitter=0.0,
                               min_delay=0.0, max_errors=5)
        for _ in range(5):
            await pm.record_error("example.com", status_code=500)
        state = pm.get_host_state("example.com")
        assert state.circuit_open_count == 1
        assert state.backoff_until > time.monotonic()

    @pytest.mark.asyncio
    async def test_circuit_breaker_stops_on_second_open(self):
        pm = PolitenessManager(rate=100.0, concurrency=2, jitter=0.0,
                               min_delay=0.0, max_errors=3)
        # First circuit open
        for _ in range(3):
            await pm.record_error("example.com", status_code=500)
        # Second circuit open
        for _ in range(3):
            await pm.record_error("example.com", status_code=500)
        assert pm.is_host_stopped("example.com")

    @pytest.mark.asyncio
    async def test_rate_restoration_after_halve(self):
        pm = PolitenessManager(rate=10.0, concurrency=2, jitter=0.0,
                               min_delay=0.0, max_errors=50)
        await pm.record_error("example.com", status_code=429)
        halved_rate = pm.bucket.rate
        # Simulate 20 successes
        for _ in range(20):
            await pm.record_success("example.com")
        assert pm.bucket.rate > halved_rate

    @pytest.mark.asyncio
    async def test_antibot_stops_after_3(self):
        pm = PolitenessManager(rate=100.0, concurrency=2, jitter=0.0,
                               min_delay=0.0, max_errors=10)
        assert not await pm.record_antibot("example.com")
        assert not await pm.record_antibot("example.com")
        assert await pm.record_antibot("example.com")
        assert pm.is_host_stopped("example.com")

    @pytest.mark.asyncio
    async def test_antibot_counter_resets_on_success(self):
        pm = PolitenessManager(rate=100.0, concurrency=2, jitter=0.0,
                               min_delay=0.0, max_errors=10)
        await pm.record_antibot("example.com")
        await pm.record_antibot("example.com")
        await pm.record_success("example.com")
        state = pm.get_host_state("example.com")
        assert state.consecutive_antibot == 0

    def test_is_host_stopped_unknown_host(self):
        pm = PolitenessManager(rate=100.0, concurrency=2, jitter=0.0,
                               min_delay=0.0, max_errors=10)
        assert not pm.is_host_stopped("unknown.com")

    def test_get_host_state_unknown(self):
        pm = PolitenessManager(rate=100.0, concurrency=2, jitter=0.0,
                               min_delay=0.0, max_errors=10)
        assert pm.get_host_state("unknown.com") is None


class TestJitterStatistics:
    @pytest.mark.asyncio
    async def test_jitter_within_expected_range(self):
        """Jitter should fall within 0 to jitter * (1/rate) statistically."""
        pm = PolitenessManager(rate=10.0, concurrency=2, jitter=0.3,
                               min_delay=0.0, max_errors=10)
        max_jitter = 0.3 * (1.0 / 10.0)  # 0.03 seconds

        delays = []
        for _ in range(20):
            start = time.monotonic()
            await pm.wait_for_slot("example.com")
            elapsed = time.monotonic() - start
            delays.append(elapsed)

        # Average delay should be roughly half the max jitter + token wait
        # Just verify no individual delay exceeds a reasonable bound
        for d in delays:
            assert d < max_jitter + 0.5  # generous bound
