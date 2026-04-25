"""Boilerplate CSS selectors and regex patterns for static stripping.

These target common documentation site cruft that trafilatura misses:
edit links, feedback widgets, version selectors, breadcrumbs, etc.
"""

# CSS selectors for elements to remove entirely
CSS_SELECTORS = [
    # Edit links
    "[class*='edit-this-page']",
    "[class*='edit-on-github']",
    "[id*='edit-this-page']",
    "[id*='edit-on-github']",
    "a[href*='github.com'][href*='/edit/']",
    # Feedback widgets
    "[class*='feedback']",
    "[class*='was-this-helpful']",
    "[id*='feedback']",
    "[id*='was-this-helpful']",
    # Last updated timestamps
    "[class*='last-updated']",
    "[class*='last-modified']",
    "[id*='last-updated']",
    "[id*='last-modified']",
    # Version selectors
    "[class*='version-selector']",
    "[class*='version-switcher']",
    "[id*='version-selector']",
    # Breadcrumbs
    "[class*='breadcrumb']",
    "[id*='breadcrumb']",
    "nav[aria-label='breadcrumb']",
    "nav[aria-label='Breadcrumb']",
    # Cookie/consent banners
    "[class*='cookie-banner']",
    "[class*='consent']",
    "[id*='cookie-banner']",
    "[id*='consent']",
    # On-this-page / TOC sidebar
    "[class*='on-this-page']",
    "[class*='table-of-contents']",
    "[id*='on-this-page']",
    "nav[aria-label='On this page']",
    "nav[aria-label='Table of contents']",
]

# Regex patterns for trailing paragraphs to strip (case-insensitive)
TRAILING_TEXT_PATTERNS = [
    r"^Last updated\b",
    r"^Last modified\b",
    r"^Edit this page\b",
    r"^Was this helpful\b",
    r"^Was this page helpful\b",
    r"^Edit on GitHub\b",
    r"^Suggest edits\b",
    r"^Previous\s*$",
    r"^Next\s*$",
]
