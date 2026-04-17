"""Tests for index.html structure, content, and inline CSS.

Validates that index.html meets all acceptance criteria:
- Valid HTML5 document structure
- Correct meta tags and title
- Navy blue background with white centered text
- Flexbox centering with full viewport height
- No external stylesheets or scripts
"""

from __future__ import annotations

import os
import re
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import pytest

# ---------------------------------------------------------------------------
# Fixtures & helpers
# ---------------------------------------------------------------------------

INDEX_PATH: Path = Path(__file__).resolve().parent.parent / "index.html"


@pytest.fixture(scope="module")
def html_content() -> str:
    """Read and return the full content of index.html."""
    assert INDEX_PATH.exists(), f"index.html not found at {INDEX_PATH}"
    return INDEX_PATH.read_text(encoding="utf-8")


class SimpleHTMLParser(HTMLParser):
    """Minimal HTML parser that collects tags, attributes, and text nodes."""

    def __init__(self) -> None:
        """Initialise the parser with empty collection containers."""
        super().__init__()
        self.tags: List[Tuple[str, Dict[str, Optional[str]]]] = []
        self.end_tags: List[str] = []
        self.current_tag: Optional[str] = None
        self.current_attrs: Dict[str, Optional[str]] = {}
        self.text_by_tag: Dict[str, List[str]] = {}
        self.style_contents: List[str] = []
        self._in_style: bool = False
        self._in_title: bool = False
        self.title_text: str = ""
        self._in_h1: bool = False
        self.h1_texts: List[str] = []
        self._current_h1_text: str = ""

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, Optional[str]]]) -> None:
        """Record opening tags and their attributes."""
        attr_dict = dict(attrs)
        self.tags.append((tag, attr_dict))
        self.current_tag = tag
        self.current_attrs = attr_dict
        if tag == "style":
            self._in_style = True
        if tag == "title":
            self._in_title = True
        if tag == "h1":
            self._in_h1 = True
            self._current_h1_text = ""

    def handle_endtag(self, tag: str) -> None:
        """Record closing tags."""
        self.end_tags.append(tag)
        if tag == "style":
            self._in_style = False
        if tag == "title":
            self._in_title = False
        if tag == "h1":
            self._in_h1 = False
            self.h1_texts.append(self._current_h1_text.strip())

    def handle_data(self, data: str) -> None:
        """Capture text content within relevant tags."""
        if self._in_style:
            self.style_contents.append(data)
        if self._in_title:
            self.title_text += data
        if self._in_h1:
            self._current_h1_text += data


@pytest.fixture(scope="module")
def parsed(html_content: str) -> SimpleHTMLParser:
    """Return a parsed representation of index.html."""
    parser = SimpleHTMLParser()
    parser.feed(html_content)
    return parser


@pytest.fixture(scope="module")
def style_block(parsed: SimpleHTMLParser) -> str:
    """Return the concatenated CSS from all <style> blocks."""
    return "\n".join(parsed.style_contents)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_file_exists() -> None:
    """index.html must exist at the repository root."""
    assert INDEX_PATH.exists(), f"Expected index.html at {INDEX_PATH}"


def test_has_html5_doctype(html_content: str) -> None:
    """File must start with the HTML5 doctype declaration."""
    stripped = html_content.lstrip()
    assert stripped.lower().startswith("<!doctype html>"), (
        "index.html must begin with <!DOCTYPE html>"
    )


def test_html_lang_attribute(parsed: SimpleHTMLParser) -> None:
    """The <html> tag must have lang='en'."""
    html_tags = [(tag, attrs) for tag, attrs in parsed.tags if tag == "html"]
    assert len(html_tags) >= 1, "No <html> tag found"
    attrs = html_tags[0][1]
    assert attrs.get("lang") == "en", "<html> tag must have lang='en'"


def test_has_charset_meta(parsed: SimpleHTMLParser) -> None:
    """A <meta charset='UTF-8'> tag must be present."""
    meta_tags = [(tag, attrs) for tag, attrs in parsed.tags if tag == "meta"]
    charset_found = any(
        attrs.get("charset", "").upper() == "UTF-8" for _, attrs in meta_tags
    )
    assert charset_found, "Missing <meta charset='UTF-8'>"


def test_has_viewport_meta(parsed: SimpleHTMLParser) -> None:
    """A viewport meta tag with width=device-width must be present."""
    meta_tags = [(tag, attrs) for tag, attrs in parsed.tags if tag == "meta"]
    viewport_found = any(
        attrs.get("name", "").lower() == "viewport"
        and "width=device-width" in (attrs.get("content", ""))
        for _, attrs in meta_tags
    )
    assert viewport_found, "Missing <meta name='viewport' content='width=device-width, ...'>"


def test_title_is_hello_phalanx(parsed: SimpleHTMLParser) -> None:
    """The <title> element must contain exactly 'Hello Phalanx'."""
    assert parsed.title_text.strip() == "Hello Phalanx", (
        f"Expected title 'Hello Phalanx', got '{parsed.title_text.strip()}'"
    )


def test_h1_contains_hello_phalanx(parsed: SimpleHTMLParser) -> None:
    """A single <h1> with exact text 'Hello Phalanx' must exist."""
    assert len(parsed.h1_texts) >= 1, "No <h1> element found"
    assert parsed.h1_texts[0] == "Hello Phalanx", (
        f"Expected h1 text 'Hello Phalanx', got '{parsed.h1_texts[0]}'"
    )


def test_only_one_h1(parsed: SimpleHTMLParser) -> None:
    """Exactly one <h1> element must be present in the document."""
    h1_count = sum(1 for tag, _ in parsed.tags if tag == "h1")
    assert h1_count == 1, f"Expected exactly 1 <h1>, found {h1_count}"


def test_no_external_stylesheets(parsed: SimpleHTMLParser) -> None:
    """No <link rel='stylesheet'> tags should be present."""
    link_tags = [(tag, attrs) for tag, attrs in parsed.tags if tag == "link"]
    stylesheet_links = [
        attrs for _, attrs in link_tags
        if attrs.get("rel", "").lower() == "stylesheet"
    ]
    assert len(stylesheet_links) == 0, "External stylesheets are not allowed"


def test_no_script_tags(parsed: SimpleHTMLParser) -> None:
    """No <script> elements should be present."""
    script_tags = [tag for tag, _ in parsed.tags if tag == "script"]
    assert len(script_tags) == 0, "<script> tags are not allowed"


def test_inline_style_has_navy_background(style_block: str) -> None:
    """The style block must set background-color to #001f3f."""
    normalised = style_block.replace(" ", "").lower()
    assert "background-color:#001f3f" in normalised, (
        "Style must contain background-color: #001f3f"
    )


def test_inline_style_has_white_text(style_block: str) -> None:
    """The style block must set color to #ffffff."""
    normalised = style_block.replace(" ", "").lower()
    assert "color:#ffffff" in normalised, (
        "Style must contain color: #ffffff"
    )


def test_inline_style_has_flexbox_centering(style_block: str) -> None:
    """The style block must use flexbox centering on body."""
    normalised = style_block.replace(" ", "").lower()
    assert "display:flex" in normalised, "Style must contain display: flex"
    assert "justify-content:center" in normalised, (
        "Style must contain justify-content: center"
    )
    assert "align-items:center" in normalised, (
        "Style must contain align-items: center"
    )


def test_body_has_min_height_100vh(style_block: str) -> None:
    """The style block must set min-height: 100vh on the body."""
    normalised = style_block.replace(" ", "").lower()
    assert "min-height:100vh" in normalised, (
        "Style must contain min-height: 100vh"
    )


def test_body_margin_zero(style_block: str) -> None:
    """The style block must set margin: 0 on body."""
    normalised = style_block.replace(" ", "").lower()
    assert "margin:0" in normalised, "Style must contain margin: 0"


def test_h1_font_size_large(style_block: str) -> None:
    """The h1 must have a large font-size (4rem or larger)."""
    normalised = style_block.replace(" ", "").lower()
    assert "font-size:4rem" in normalised, (
        "Style must contain font-size: 4rem (or larger) for h1"
    )


def test_font_family_sans_serif(style_block: str) -> None:
    """The style block must include a sans-serif font-family."""
    normalised = style_block.lower()
    assert "sans-serif" in normalised, (
        "Style must include sans-serif in font-family"
    )


def test_no_other_files_required(html_content: str) -> None:
    """No local file references (img src, href to local files) should exist."""
    # Check for common local resource patterns (excluding the # in colors)
    local_patterns = [
        r'src\s*=\s*["\'](?!https?://)',
        r'href\s*=\s*["\'](?!https?://)(?!#)',
    ]
    for pattern in local_patterns:
        matches = re.findall(pattern, html_content, re.IGNORECASE)
        assert len(matches) == 0, (
            f"Found local file reference matching pattern '{pattern}': {matches}"
        )
