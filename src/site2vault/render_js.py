"""Optional Playwright-based JS renderer (lazy import)."""

import logging

log = logging.getLogger("site2vault.render_js")


class PlaywrightFetcher:
    """Fetches pages using Playwright for JS-rendered content."""

    def __init__(self):
        self._browser = None
        self._context = None

    async def start(self) -> None:
        """Launch browser."""
        try:
            from playwright.async_api import async_playwright
        except ImportError:
            log.error(
                "Playwright is not installed. Install it with:\n"
                "  pip install 'site2vault[js]'\n"
                "  playwright install chromium"
            )
            raise SystemExit(1)

        self._pw = await async_playwright().start()
        self._browser = await self._pw.chromium.launch(headless=True)
        self._context = await self._browser.new_context()

    async def fetch(self, url: str) -> str:
        """Fetch a page and return rendered HTML."""
        if not self._context:
            await self.start()

        page = await self._context.new_page()
        try:
            await page.goto(url, wait_until="networkidle", timeout=10000)
            return await page.content()
        finally:
            await page.close()

    async def close(self) -> None:
        """Clean up browser resources."""
        if self._context:
            await self._context.close()
        if self._browser:
            await self._browser.close()
        if hasattr(self, "_pw"):
            await self._pw.stop()
