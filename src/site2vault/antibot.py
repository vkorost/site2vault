"""Anti-bot / challenge / trap detection.

Inspects responses for signs of blocking, CAPTCHAs, login walls,
consent walls, and bot traps (query explosion, calendar explosion,
session IDs, duplicate content).
"""

import logging
import re
from collections import defaultdict
from urllib.parse import urlparse, parse_qs

log = logging.getLogger("site2vault.antibot")

# Cloudflare challenge signatures
CF_SIGNATURES = [
    "cf-browser-verification",
    "cf-challenge",
    "Just a moment...",
]

# CAPTCHA signatures
CAPTCHA_SIGNATURES = [
    "g-recaptcha",
    "h-captcha",
    "turnstile",
    "/recaptcha/api.js",
]

# Login wall redirect patterns
LOGIN_PATHS = {"/login", "/signin", "/auth", "/sign-in", "/log-in"}
LOGIN_QUERY_KEYS = {"returnto", "redirect", "return_to", "redirect_uri", "next"}

# GDPR consent framework signatures
CONSENT_SIGNATURES = ["onetrust", "cookielaw", "quantcast"]

# Generic block page text (case-insensitive)
BLOCK_TEXTS = ["access denied", "forbidden", "rate limit", "too many requests"]


class AntibotDetector:
    """Detects anti-bot measures in HTTP responses."""

    def __init__(self):
        self._path_query_counts: dict[str, int] = defaultdict(int)
        self._date_urls: dict[str, list[str]] = defaultdict(list)

    def check_response(
        self,
        url: str,
        status_code: int,
        headers: dict[str, str],
        body: str,
        final_url: str | None = None,
    ) -> str | None:
        """Check a response for anti-bot signals.

        Returns a signal string if detected (e.g. 'cloudflare', 'captcha'),
        or None if the response appears genuine.
        """
        # Cloudflare challenge
        if self._is_cloudflare(status_code, headers, body):
            return "cloudflare"

        # CAPTCHA
        if self._is_captcha(body):
            return "captcha"

        # Login wall
        if self._is_login_wall(url, final_url):
            return "login_wall"

        # Consent wall
        if self._is_consent_wall(body):
            return "consent_wall"

        # Generic block
        if self._is_generic_block(status_code, body):
            return "generic_block"

        return None

    def check_bot_trap(self, url: str, existing_content_hashes: set[str],
                       content_hash: str | None = None) -> str | None:
        """Check if a URL is a bot trap.

        Returns a reason string if trapped, or None if safe.
        """
        # Query explosion
        reason = self._check_query_explosion(url)
        if reason:
            return reason

        # Calendar explosion
        reason = self._check_calendar_explosion(url)
        if reason:
            return reason

        # Duplicate content
        if content_hash and content_hash in existing_content_hashes:
            return "duplicate_content"

        return None

    def _is_cloudflare(
        self, status_code: int, headers: dict[str, str], body: str
    ) -> bool:
        # 403 with cf-ray header
        if status_code == 403 and "cf-ray" in {k.lower() for k in headers}:
            return True
        # Body signatures
        body_lower = body.lower() if body else ""
        return any(sig.lower() in body_lower for sig in CF_SIGNATURES)

    def _is_captcha(self, body: str) -> bool:
        body_lower = body.lower() if body else ""
        return any(sig.lower() in body_lower for sig in CAPTCHA_SIGNATURES)

    def _is_login_wall(self, original_url: str, final_url: str | None) -> bool:
        if not final_url or final_url == original_url:
            return False
        parsed = urlparse(final_url)
        path_lower = parsed.path.lower().rstrip("/")
        # Check if redirect landed on a login page
        if any(path_lower.endswith(lp) for lp in LOGIN_PATHS):
            return True
        # Check query for redirect params
        query = parse_qs(parsed.query)
        return bool(LOGIN_QUERY_KEYS & {k.lower() for k in query})

    def _is_consent_wall(self, body: str) -> bool:
        if not body:
            return False
        body_lower = body.lower()
        has_consent = any(sig in body_lower for sig in CONSENT_SIGNATURES)
        if not has_consent:
            return False
        # Only a consent wall if actual content is minimal
        # Strip tags roughly
        text_only = re.sub(r"<[^>]+>", "", body)
        return len(text_only.strip()) < 200

    def _is_generic_block(self, status_code: int, body: str) -> bool:
        if not body:
            return False
        body_lower = body.lower()

        # 403 with small body
        if status_code == 403 and len(body) < 2048:
            return True

        # 200 with block language in title or h1
        if status_code == 200:
            # Extract title
            title_match = re.search(r"<title[^>]*>(.*?)</title>", body_lower, re.DOTALL)
            h1_match = re.search(r"<h1[^>]*>(.*?)</h1>", body_lower, re.DOTALL)
            check_text = ""
            if title_match:
                check_text += title_match.group(1)
            if h1_match:
                check_text += " " + h1_match.group(1)
            return any(bt in check_text for bt in BLOCK_TEXTS)

        return False

    def _check_query_explosion(self, url: str) -> str | None:
        """Detect query parameter explosion."""
        parsed = urlparse(url)
        path = parsed.path
        if not parsed.query:
            return None

        self._path_query_counts[path] += 1
        if self._path_query_counts[path] > 100:
            return f"query_explosion:{path}"
        return None

    def _check_calendar_explosion(self, url: str) -> str | None:
        """Detect calendar URL explosion."""
        # Match /YYYY/MM/DD/ or /YYYY-MM-DD/
        date_match = re.search(
            r"/(\d{4})[/-](\d{2})[/-](\d{2})", url
        )
        if not date_match:
            return None

        parsed = urlparse(url)
        # Use path prefix before the date as the key
        path = parsed.path
        date_pos = path.find(date_match.group(0))
        prefix = path[:date_pos] if date_pos > 0 else "/"

        self._date_urls[prefix].append(url)
        if len(self._date_urls[prefix]) > 10:
            return f"calendar_explosion:{prefix}"
        return None

    @staticmethod
    def has_session_params(url: str) -> bool:
        """Check if URL contains session ID parameters."""
        parsed = urlparse(url)
        query = parse_qs(parsed.query)
        session_params = {"sid", "sess", "phpsessid", "jsessionid", "sessionid"}
        return bool(session_params & {k.lower() for k in query})
