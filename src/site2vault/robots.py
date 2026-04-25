"""robots.txt parsing and caching with Crawl-delay support."""

import logging
import re
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

log = logging.getLogger("site2vault.robots")


class RobotsChecker:
    """Fetches, parses, and caches robots.txt per host."""

    def __init__(self, config):
        self.config = config
        self._cache: dict[str, RobotFileParser | None] = {}
        self._crawl_delays: dict[str, float | None] = {}
        self.user_agent = config.user_agent

    async def load_seed(self) -> None:
        """Check robots.txt for the seed URL. Exit if disallowed."""
        if self.config.ignore_robots:
            log.warning("robots.txt checking disabled (--ignore-robots)")
            return

        parsed = urlparse(self.config.seed_url)
        host = parsed.hostname
        if not host:
            return

        robots = await self._fetch_robots(parsed.scheme, host, parsed.port)
        if robots and not robots.can_fetch(self.user_agent, self.config.seed_url):
            log.error(
                "robots.txt disallows crawling the seed URL: %s\n"
                "Use --ignore-robots to override.",
                self.config.seed_url,
            )
            raise SystemExit(1)

    async def can_fetch(self, url: str) -> bool:
        """Check if a URL is allowed by robots.txt."""
        if self.config.ignore_robots:
            return True

        parsed = urlparse(url)
        host = parsed.hostname
        if not host:
            return True

        cache_key = f"{parsed.scheme}://{host}"
        if cache_key not in self._cache:
            robots = await self._fetch_robots(parsed.scheme, host, parsed.port)
            self._cache[cache_key] = robots

        robots = self._cache.get(cache_key)
        if robots is None:
            return True  # No robots.txt or fetch failed

        return robots.can_fetch(self.user_agent, url)

    def get_crawl_delay(self, host: str) -> float | None:
        """Get the Crawl-delay for a host, if any."""
        return self._crawl_delays.get(host)

    async def _fetch_robots(
        self, scheme: str, host: str, port: int | None
    ) -> RobotFileParser | None:
        """Fetch and parse robots.txt for a host."""
        import httpx

        if port and ((scheme == "http" and port != 80) or (scheme == "https" and port != 443)):
            robots_url = f"{scheme}://{host}:{port}/robots.txt"
        else:
            robots_url = f"{scheme}://{host}/robots.txt"

        cache_key = f"{scheme}://{host}"

        try:
            async with httpx.AsyncClient(
                timeout=httpx.Timeout(10.0),
                follow_redirects=True,
            ) as client:
                resp = await client.get(robots_url)

            if resp.status_code in (404, 410):
                log.debug("No robots.txt at %s (404/410)", robots_url)
                self._cache[cache_key] = None
                return None

            if resp.status_code >= 500:
                log.debug("robots.txt server error at %s (%d)", robots_url, resp.status_code)
                self._cache[cache_key] = None
                return None

            text = resp.text
            rp = RobotFileParser()
            rp.parse(text.splitlines())
            self._cache[cache_key] = rp

            # Extract Crawl-delay
            delay = self._parse_crawl_delay(text)
            if delay is not None:
                self._crawl_delays[host] = delay
                log.info("Host %s: Crawl-delay = %.1f", host, delay)

            return rp

        except Exception as e:
            log.warning("Failed to fetch robots.txt from %s: %s", robots_url, e)
            self._cache[cache_key] = None
            return None

    def _parse_crawl_delay(self, robots_text: str) -> float | None:
        """Extract Crawl-delay from robots.txt text."""
        # Look for Crawl-delay in our user-agent block or * block
        current_agent_applies = False
        delay = None

        for line in robots_text.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            if line.lower().startswith("user-agent:"):
                agent = line.split(":", 1)[1].strip().lower()
                current_agent_applies = (
                    agent == "*" or agent in self.user_agent.lower()
                )
            elif current_agent_applies and line.lower().startswith("crawl-delay:"):
                try:
                    delay = float(line.split(":", 1)[1].strip())
                except ValueError:
                    pass

        return delay
