"""URL canonicalization.

Every URL entering the crawler passes through canonicalize() first.
Rules applied in order per spec section 6.
"""

from urllib.parse import urlparse, urlunparse, urlencode, parse_qs, quote, unquote

# Tracking and session query parameters to strip
TRACKING_PARAMS = frozenset({
    "utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content",
    "utm_id", "utm_source_platform", "utm_creative_format", "utm_marketing_tactic",
    "fbclid", "gclid", "mc_eid", "mc_cid", "ref", "ref_src",
    "_hsenc", "_hsmi", "igshid", "_ga", "yclid",
    "sid", "sess", "phpsessid", "jsessionid", "sessionid",
})


def canonicalize(url: str, seed_url: str | None = None) -> str:
    """Canonicalize a URL according to the spec rules.

    Args:
        url: The URL to canonicalize.
        seed_url: The seed URL for context (www handling, https forcing).

    Returns:
        The canonical URL string (without fragment).
    """
    canonical, _ = canonicalize_with_fragment(url, seed_url)
    return canonical


def canonicalize_with_fragment(url: str, seed_url: str | None = None) -> tuple[str, str | None]:
    """Canonicalize a URL and return (canonical_url, fragment) separately.

    Args:
        url: The URL to canonicalize.
        seed_url: The seed URL for context.

    Returns:
        Tuple of (canonical_url_without_fragment, fragment_or_None).
    """
    parsed = urlparse(url)

    # 1. Lowercase scheme and host
    scheme = parsed.scheme.lower()
    host = (parsed.hostname or "").lower()
    port = parsed.port

    # 2. Strip default ports
    if (scheme == "http" and port == 80) or (scheme == "https" and port == 443):
        port = None

    # 3. Force https when seed uses https
    if seed_url:
        seed_scheme = urlparse(seed_url).scheme.lower()
        if seed_scheme == "https" and scheme == "http":
            scheme = "https"

    # 4. Drop fragment, retain separately
    fragment = parsed.fragment or None

    # 5. Remove www. prefix only if seed host does not use www.
    if seed_url:
        seed_host = (urlparse(seed_url).hostname or "").lower()
        seed_uses_www = seed_host.startswith("www.")
    else:
        seed_uses_www = False

    if not seed_uses_www and host.startswith("www."):
        host = host[4:]

    # Reconstruct netloc with optional port
    netloc = host
    if port is not None:
        netloc = f"{host}:{port}"

    # 9. Percent-encode path segments per RFC 3986
    path = parsed.path
    # Decode then re-encode to normalize
    path = quote(unquote(path), safe="/:@!$&'()*+,;=-._~")

    # 6. Remove trailing slash unless path is exactly "/"
    if path != "/" and path.endswith("/"):
        path = path.rstrip("/")

    # Ensure root path
    if not path:
        path = "/"

    # 7. Strip tracking and session query parameters
    query_params = parse_qs(parsed.query, keep_blank_values=True)
    filtered_params = {
        k: v for k, v in query_params.items()
        if k.lower() not in TRACKING_PARAMS
    }

    # 8. Sort remaining query parameters alphabetically
    sorted_query = urlencode(
        sorted(
            ((k, v_item) for k, v_list in filtered_params.items() for v_item in v_list),
            key=lambda x: x[0],
        ),
        quote_via=quote,
    )

    # Reconstruct URL without fragment
    canonical = urlunparse((scheme, netloc, path, "", sorted_query, ""))

    return canonical, fragment
