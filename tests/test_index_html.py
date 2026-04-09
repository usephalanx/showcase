"""Tests for the index.html entry point file.

Validates that index.html exists, is a valid HTML5 document, contains
the required root div and module script tag.
"""

from pathlib import Path

import pytest

INDEX_PATH = Path(__file__).resolve().parent.parent / "index.html"


@pytest.fixture()
def html_content() -> str:
    """Read and return the contents of index.html."""
    assert INDEX_PATH.exists(), f"index.html not found at {INDEX_PATH}"
    return INDEX_PATH.read_text(encoding="utf-8")


def test_index_html_exists() -> None:
    """index.html must exist in the project root."""
    assert INDEX_PATH.exists()


def test_has_doctype(html_content: str) -> None:
    """index.html must start with an HTML5 doctype."""
    assert html_content.strip().lower().startswith("<!doctype html>")


def test_has_lang_attribute(html_content: str) -> None:
    """The <html> tag must include a lang attribute."""
    assert 'lang="en"' in html_content


def test_has_root_div(html_content: str) -> None:
    """The document must contain a <div id='root'></div>."""
    assert '<div id="root"></div>' in html_content


def test_has_module_script(html_content: str) -> None:
    """The document must include a module script tag pointing to /src/main.tsx."""
    assert '<script type="module" src="/src/main.tsx"></script>' in html_content


def test_has_charset_meta(html_content: str) -> None:
    """The document must declare UTF-8 charset."""
    assert 'charset="UTF-8"' in html_content


def test_has_viewport_meta(html_content: str) -> None:
    """The document must include a viewport meta tag."""
    assert 'name="viewport"' in html_content


def test_no_external_cdn_links(html_content: str) -> None:
    """The document must not include any external CDN links."""
    # Check for common CDN patterns
    cdn_patterns = [
        "cdn.jsdelivr.net",
        "cdnjs.cloudflare.com",
        "unpkg.com",
        "googleapis.com",
    ]
    for pattern in cdn_patterns:
        assert pattern not in html_content, f"Found CDN link: {pattern}"


def test_has_title(html_content: str) -> None:
    """The document must have a <title> tag."""
    assert "<title>" in html_content
    assert "</title>" in html_content
