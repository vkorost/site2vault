"""Tests for URL canonicalization - targeting 100% coverage."""

import pytest

from site2vault.canonical import canonicalize, canonicalize_with_fragment, TRACKING_PARAMS


class TestLowercaseSchemeAndHost:
    def test_uppercase_scheme(self):
        assert canonicalize("HTTP://Example.COM/page") == "http://example.com/page"

    def test_mixed_case_host(self):
        assert canonicalize("https://ExAmPlE.CoM/path") == "https://example.com/path"

    def test_scheme_and_host_lowered(self):
        assert canonicalize("HTTPS://WWW.EXAMPLE.COM/Page") == "https://example.com/Page"


class TestStripDefaultPorts:
    def test_http_port_80_stripped(self):
        assert canonicalize("http://example.com:80/page") == "http://example.com/page"

    def test_https_port_443_stripped(self):
        assert canonicalize("https://example.com:443/page") == "https://example.com/page"

    def test_non_default_port_kept(self):
        assert canonicalize("https://example.com:8080/page") == "https://example.com:8080/page"

    def test_http_port_443_kept(self):
        assert canonicalize("http://example.com:443/page") == "http://example.com:443/page"


class TestForceHttps:
    def test_http_upgraded_when_seed_is_https(self):
        result = canonicalize("http://example.com/page", seed_url="https://example.com")
        assert result == "https://example.com/page"

    def test_http_kept_when_seed_is_http(self):
        result = canonicalize("http://example.com/page", seed_url="http://example.com")
        assert result == "http://example.com/page"

    def test_https_stays_https(self):
        result = canonicalize("https://example.com/page", seed_url="https://example.com")
        assert result == "https://example.com/page"


class TestFragmentSeparation:
    def test_fragment_stripped_from_canonical(self):
        assert canonicalize("https://example.com/page#section") == "https://example.com/page"

    def test_fragment_returned_separately(self):
        url, frag = canonicalize_with_fragment("https://example.com/page#install-guide")
        assert url == "https://example.com/page"
        assert frag == "install-guide"

    def test_no_fragment_returns_none(self):
        url, frag = canonicalize_with_fragment("https://example.com/page")
        assert url == "https://example.com/page"
        assert frag is None

    def test_empty_fragment_returns_none(self):
        url, frag = canonicalize_with_fragment("https://example.com/page#")
        assert url == "https://example.com/page"
        assert frag is None


class TestWwwNormalization:
    def test_www_removed_when_seed_has_no_www(self):
        result = canonicalize("https://www.example.com/page", seed_url="https://example.com")
        assert result == "https://example.com/page"

    def test_www_kept_when_seed_has_www(self):
        result = canonicalize("https://www.example.com/page", seed_url="https://www.example.com")
        assert result == "https://www.example.com/page"

    def test_www_removed_when_no_seed(self):
        result = canonicalize("https://www.example.com/page")
        assert result == "https://example.com/page"

    def test_non_www_unchanged_when_seed_has_www(self):
        result = canonicalize("https://example.com/page", seed_url="https://www.example.com")
        assert result == "https://example.com/page"


class TestTrailingSlash:
    def test_trailing_slash_removed(self):
        assert canonicalize("https://example.com/page/") == "https://example.com/page"

    def test_root_slash_kept(self):
        assert canonicalize("https://example.com/") == "https://example.com/"

    def test_no_trailing_slash_unchanged(self):
        assert canonicalize("https://example.com/page") == "https://example.com/page"

    def test_multiple_trailing_slashes_removed(self):
        assert canonicalize("https://example.com/page///") == "https://example.com/page"


class TestTrackingParams:
    def test_utm_params_stripped(self):
        url = "https://example.com/page?utm_source=twitter&utm_medium=social&key=val"
        assert canonicalize(url) == "https://example.com/page?key=val"

    def test_fbclid_stripped(self):
        url = "https://example.com/page?fbclid=abc123&q=test"
        assert canonicalize(url) == "https://example.com/page?q=test"

    def test_gclid_stripped(self):
        url = "https://example.com/page?gclid=xyz&q=test"
        assert canonicalize(url) == "https://example.com/page?q=test"

    def test_all_tracking_stripped_leaves_no_query(self):
        url = "https://example.com/page?utm_source=a&fbclid=b&gclid=c"
        assert canonicalize(url) == "https://example.com/page"

    def test_case_insensitive_param_matching(self):
        url = "https://example.com/page?UTM_SOURCE=twitter&key=val"
        assert canonicalize(url) == "https://example.com/page?key=val"


class TestSessionIdStripping:
    def test_phpsessid_stripped(self):
        url = "https://example.com/page?phpsessid=abc123&q=test"
        assert canonicalize(url) == "https://example.com/page?q=test"

    def test_jsessionid_stripped(self):
        url = "https://example.com/page?jsessionid=xyz&q=test"
        assert canonicalize(url) == "https://example.com/page?q=test"

    def test_sessionid_stripped(self):
        url = "https://example.com/page?sessionid=123&q=test"
        assert canonicalize(url) == "https://example.com/page?q=test"

    def test_sid_stripped(self):
        url = "https://example.com/page?sid=abc&q=test"
        assert canonicalize(url) == "https://example.com/page?q=test"

    def test_sess_stripped(self):
        url = "https://example.com/page?sess=abc&q=test"
        assert canonicalize(url) == "https://example.com/page?q=test"


class TestQuerySorting:
    def test_params_sorted_alphabetically(self):
        url = "https://example.com/page?z=1&a=2&m=3"
        assert canonicalize(url) == "https://example.com/page?a=2&m=3&z=1"

    def test_already_sorted(self):
        url = "https://example.com/page?a=1&b=2&c=3"
        assert canonicalize(url) == "https://example.com/page?a=1&b=2&c=3"


class TestPercentEncoding:
    def test_spaces_encoded(self):
        url = "https://example.com/my page/doc"
        result = canonicalize(url)
        assert "my%20page" in result

    def test_already_encoded_normalized(self):
        url = "https://example.com/p%61ge"
        result = canonicalize(url)
        assert result == "https://example.com/page"

    def test_safe_characters_not_double_encoded(self):
        url = "https://example.com/path/to/page"
        result = canonicalize(url)
        assert result == "https://example.com/path/to/page"


class TestEdgeCases:
    def test_empty_path_gets_slash(self):
        result = canonicalize("https://example.com")
        assert result == "https://example.com/"

    def test_preserves_path_case(self):
        result = canonicalize("https://example.com/CamelCase/Page")
        assert result == "https://example.com/CamelCase/Page"

    def test_complex_url(self):
        url = "HTTPS://WWW.Example.COM:443/Path/Page/?utm_source=x&key=val&fbclid=y#section"
        result = canonicalize(url)
        assert result == "https://example.com/Path/Page?key=val"

    def test_no_seed_url(self):
        result = canonicalize("https://example.com/page")
        assert result == "https://example.com/page"

    def test_tracking_params_constant_has_expected_entries(self):
        expected = {"utm_source", "fbclid", "gclid", "phpsessid", "jsessionid", "sessionid"}
        assert expected.issubset(TRACKING_PARAMS)
