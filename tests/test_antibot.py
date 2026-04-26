"""Tests for antibot.py - anti-bot/challenge/trap detection."""

import pytest

from site2vault.antibot import AntibotDetector


@pytest.fixture
def detector():
    return AntibotDetector()


class TestCloudflareDetection:
    def test_cf_browser_verification(self, detector):
        body = '<div id="cf-browser-verification">Please wait...</div>'
        assert detector.check_response("https://x.com", 200, {}, body) == "cloudflare"

    def test_cf_challenge_in_body(self, detector):
        body = '<div class="cf-challenge">Checking...</div>'
        assert detector.check_response("https://x.com", 200, {}, body) == "cloudflare"

    def test_just_a_moment(self, detector):
        body = "<title>Just a moment...</title>"
        assert detector.check_response("https://x.com", 200, {}, body) == "cloudflare"

    def test_403_with_cf_ray(self, detector):
        headers = {"cf-ray": "abc123", "content-type": "text/html"}
        assert detector.check_response("https://x.com", 403, headers, "Blocked") == "cloudflare"

    def test_normal_403_without_cf_ray(self, detector):
        # 403 with small body is generic_block, not cloudflare
        result = detector.check_response("https://x.com", 403, {}, "Forbidden")
        assert result == "generic_block"


class TestCaptchaDetection:
    def test_recaptcha(self, detector):
        body = '<div class="g-recaptcha" data-sitekey="abc"></div>'
        assert detector.check_response("https://x.com", 200, {}, body) == "captcha"

    def test_hcaptcha(self, detector):
        body = '<div class="h-captcha"></div>'
        assert detector.check_response("https://x.com", 200, {}, body) == "captcha"

    def test_turnstile(self, detector):
        body = '<script src="turnstile"></script>'
        assert detector.check_response("https://x.com", 200, {}, body) == "captcha"

    def test_recaptcha_script(self, detector):
        body = '<script src="/recaptcha/api.js"></script>'
        assert detector.check_response("https://x.com", 200, {}, body) == "captcha"


class TestLoginWallDetection:
    def test_redirect_to_login(self, detector):
        result = detector.check_response(
            "https://x.com/page", 200, {}, "Content",
            final_url="https://x.com/login"
        )
        assert result == "login_wall"

    def test_redirect_to_signin(self, detector):
        result = detector.check_response(
            "https://x.com/page", 200, {}, "Content",
            final_url="https://x.com/signin"
        )
        assert result == "login_wall"

    def test_redirect_with_returnto(self, detector):
        result = detector.check_response(
            "https://x.com/page", 200, {}, "Content",
            final_url="https://x.com/auth?returnTo=/page"
        )
        assert result == "login_wall"

    def test_no_redirect_no_login_wall(self, detector):
        result = detector.check_response(
            "https://x.com/page", 200, {}, "Content",
            final_url="https://x.com/page"
        )
        assert result is None

    def test_no_final_url_no_login_wall(self, detector):
        result = detector.check_response(
            "https://x.com/page", 200, {}, "Content"
        )
        assert result is None


class TestConsentWallDetection:
    def test_onetrust_with_minimal_content(self, detector):
        body = '<div id="onetrust-banner">Accept cookies</div>'
        assert detector.check_response("https://x.com", 200, {}, body) == "consent_wall"

    def test_onetrust_with_real_content(self, detector):
        body = '<div id="onetrust-banner">Accept</div>' + "<p>" + "x" * 300 + "</p>"
        assert detector.check_response("https://x.com", 200, {}, body) is None

    def test_cookielaw(self, detector):
        body = '<div class="cookielaw">Consent required</div>'
        assert detector.check_response("https://x.com", 200, {}, body) == "consent_wall"


class TestGenericBlockDetection:
    def test_403_small_body(self, detector):
        assert detector.check_response("https://x.com", 403, {}, "Forbidden") == "generic_block"

    def test_403_large_body_not_block(self, detector):
        body = "x" * 3000
        # Large 403 body is NOT generic block (could be a real error page)
        assert detector.check_response("https://x.com", 403, {}, body) is None

    def test_200_with_access_denied_in_title(self, detector):
        body = "<html><title>Access Denied</title><body>Sorry</body></html>"
        assert detector.check_response("https://x.com", 200, {}, body) == "generic_block"

    def test_200_with_rate_limit_in_h1(self, detector):
        body = "<html><body><h1>Rate Limit Exceeded</h1></body></html>"
        assert detector.check_response("https://x.com", 200, {}, body) == "generic_block"

    def test_normal_200(self, detector):
        body = "<html><title>My Page</title><body><p>Content here</p></body></html>"
        assert detector.check_response("https://x.com", 200, {}, body) is None


class TestQueryExplosion:
    def test_under_threshold_passes(self, detector):
        for i in range(100):
            result = detector.check_bot_trap(
                f"https://x.com/search?q=term{i}", set()
            )
            assert result is None

    def test_over_threshold_detected(self, detector):
        for i in range(101):
            result = detector.check_bot_trap(
                f"https://x.com/search?q=term{i}", set()
            )
        assert result is not None
        assert "query_explosion" in result


class TestCalendarExplosion:
    def test_under_threshold_passes(self, detector):
        for i in range(10):
            result = detector.check_bot_trap(
                f"https://x.com/blog/2024/01/{i+1:02d}/post", set()
            )
            assert result is None

    def test_over_threshold_detected(self, detector):
        for i in range(11):
            result = detector.check_bot_trap(
                f"https://x.com/blog/2024/01/{i+1:02d}/post", set()
            )
        assert result is not None
        assert "calendar_explosion" in result

    def test_hyphenated_dates(self, detector):
        for i in range(11):
            result = detector.check_bot_trap(
                f"https://x.com/blog/2024-01-{i+1:02d}/post", set()
            )
        assert result is not None

    def test_no_date_in_url_passes(self, detector):
        result = detector.check_bot_trap("https://x.com/page", set())
        assert result is None


class TestDuplicateContent:
    def test_duplicate_detected(self, detector):
        existing = {"abc123"}
        result = detector.check_bot_trap(
            "https://x.com/page", existing, content_hash="abc123"
        )
        assert result == "duplicate_content"

    def test_unique_content_passes(self, detector):
        existing = {"abc123"}
        result = detector.check_bot_trap(
            "https://x.com/page", existing, content_hash="def456"
        )
        assert result is None

    def test_no_hash_passes(self, detector):
        existing = {"abc123"}
        result = detector.check_bot_trap("https://x.com/page", existing)
        assert result is None


class TestSessionParams:
    def test_phpsessid_detected(self):
        assert AntibotDetector.has_session_params(
            "https://x.com/page?phpsessid=abc123"
        )

    def test_jsessionid_detected(self):
        assert AntibotDetector.has_session_params(
            "https://x.com/page?jsessionid=xyz"
        )

    def test_sid_detected(self):
        assert AntibotDetector.has_session_params(
            "https://x.com/page?sid=abc"
        )

    def test_no_session_params(self):
        assert not AntibotDetector.has_session_params(
            "https://x.com/page?q=search"
        )

    def test_case_insensitive(self):
        assert AntibotDetector.has_session_params(
            "https://x.com/page?PHPSESSID=abc"
        )
