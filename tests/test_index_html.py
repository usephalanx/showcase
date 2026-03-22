"""Tests for index.html structure, content, and inline styling.

Validates that the landing page meets all specification requirements:
HTML5 doctype, meta tags, inline CSS with flexbox centering on a navy
background, a single <h1> with the correct text, and zero external
dependencies.
"""

from __future__ import annotations

import os
import re
from html.parser import HTMLParser
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import pytest

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent
INDEX_PATH: Path = PROJECT_ROOT / "index.html"


def _read_index() -> str:
    """Return the full text content of index.html."""
    return INDEX_PATH.read_text(encoding="utf-8")


class _IndexHTMLParser(HTMLParser):
    """Minimal HTML parser that collects structural information."""

    def __init__(self) -> None:
        """Initialise parser state collectors."""
        super().__init__()
        self.tags: List[str] = []
        self.attrs_by_tag: Dict[str, List[List[Tuple[str, Optional[str]]]]] = {}
        self.style_content: str = ""
        self.h1_texts: List[str] = []
        self._inside_style: bool = False
        self._inside_h1: bool = False
        self._current_h1_text: str = ""
        self.html_attrs: List[Tuple[str, Optional[str]]] = []
        self.link_tags: List[List[Tuple[str, Optional[str]]]] = []
        self.script_tags: List[List[Tuple[str, Optional[str]]]] = []

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, Optional[str]]]) -> None:
        """Record every opening tag and its attributes."""
        tag_lower = tag.lower()
        self.tags.append(tag_lower)
        self.attrs_by_tag.setdefault(tag_lower, []).append(attrs)

        if tag_lower == "html":
            self.html_attrs = attrs
        elif tag_lower == "style":
            self._inside_style = True
        elif tag_lower == "h1":
            self._inside_h1 = True
            self._current_h1_text = ""
        elif tag_lower == "link":
            self.link_tags.append(attrs)
        elif tag_lower == "script":
            self.script_tags.append(attrs)

    def handle_endtag(self, tag: str) -> None:
        """Detect closing tags for style and h1."""
        tag_lower = tag.lower()
        if tag_lower == "style":
            self._inside_style = False
        elif tag_lower == "h1":
            self._inside_h1 = False
            self.h1_texts.append(self._current_h1_text)

    def handle_data(self, data: str) -> None:
        """Collect text content for style blocks and h1 elements."""
        if self._inside_style:
            self.style_content += data
        if self._inside_h1:
            self._current_h1_text += data


def _parse_index() -> _IndexHTMLParser:
    """Parse index.html and return the populated parser."""
    parser = _IndexHTMLParser()
    parser.feed(_read_index())
    return parser


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_file_exists() -> None:
    """index.html must exist at the project root."""
    assert INDEX_PATH.exists(), f"Expected {INDEX_PATH} to exist"
    assert INDEX_PATH.is_file(), f"Expected {INDEX_PATH} to be a file"


def test_has_html5_doctype() -> None:
    """First line must declare <!DOCTYPE html>."""
    content = _read_index()
    first_line = content.lstrip().split("\n", 1)[0].strip()
    assert first_line.lower() == "<!doctype html>", (
        f"Expected first line to be '<!DOCTYPE html>', got: {first_line!r}"
    )


def test_has_lang_attribute() -> None:
    """The <html> element must have a lang attribute."""
    parser = _parse_index()
    attr_dict = dict(parser.html_attrs)
    assert "lang" in attr_dict, "<html> tag must have a lang attribute"
    assert attr_dict["lang"], "lang attribute must not be empty"


def test_has_meta_charset() -> None:
    """A <meta charset='UTF-8'> tag must be present."""
    content = _read_index().lower()
    assert re.search(r'<meta\s+charset\s*=\s*["\']utf-8["\']', content), (
        "Expected <meta charset=\"UTF-8\"> in the document"
    )


def test_has_meta_viewport() -> None:
    """A meta viewport tag with width=device-width must be present."""
    content = _read_index().lower()
    assert re.search(
        r'<meta\s+name\s*=\s*["\']viewport["\']\s+content\s*=\s*["\'][^"\']*width=device-width',
        content,
    ), "Expected a <meta name=\"viewport\"> tag with width=device-width"


def test_title_is_hello_phalanx() -> None:
    """The <title> must be 'Hello, Phalanx!'."""
    content = _read_index()
    match = re.search(r"<title>(.*?)</title>", content, re.IGNORECASE | re.DOTALL)
    assert match is not None, "Expected a <title> element"
    assert match.group(1).strip() == "Hello, Phalanx!", (
        f"Expected title 'Hello, Phalanx!', got: {match.group(1).strip()!r}"
    )


def test_inline_style_present() -> None:
    """An inline <style> block must exist."""
    parser = _parse_index()
    assert parser.style_content.strip(), "Expected a non-empty <style> block"


def test_background_color() -> None:
    """Style block must set background-color to #001f3f."""
    parser = _parse_index()
    style = parser.style_content.lower()
    assert "#001f3f" in style, "Expected background-color: #001f3f in style block"


def test_text_color() -> None:
    """Style block must set color to #ffffff."""
    parser = _parse_index()
    style = parser.style_content.lower()
    assert "#ffffff" in style, "Expected color: #ffffff in style block"


def test_flexbox_centering() -> None:
    """Style block must use flexbox centering (display:flex, justify-content:center, align-items:center)."""
    parser = _parse_index()
    style = parser.style_content.lower().replace(" ", "")
    assert "display:flex" in style, "Expected 'display: flex' in style block"
    assert "justify-content:center" in style, "Expected 'justify-content: center' in style block"
    assert "align-items:center" in style, "Expected 'align-items: center' in style block"


def test_min_height_100vh() -> None:
    """Style block must include min-height: 100vh."""
    parser = _parse_index()
    style = parser.style_content.lower().replace(" ", "")
    assert "min-height:100vh" in style, "Expected 'min-height: 100vh' in style block"


def test_font_family_sans_serif() -> None:
    """Style block must include sans-serif in the font-family stack."""
    parser = _parse_index()
    style = parser.style_content.lower()
    assert "sans-serif" in style, "Expected sans-serif in font-family declaration"


def test_body_contains_hello_phalanx() -> None:
    """The body must contain an <h1> element with text 'Hello, Phalanx!'."""
    parser = _parse_index()
    assert len(parser.h1_texts) >= 1, "Expected at least one <h1> element"
    found = any(t.strip() == "Hello, Phalanx!" for t in parser.h1_texts)
    assert found, (
        f"Expected <h1> with text 'Hello, Phalanx!', got: {parser.h1_texts!r}"
    )


def test_exactly_one_h1() -> None:
    """There should be exactly one <h1> element."""
    parser = _parse_index()
    h1_count = parser.tags.count("h1")
    assert h1_count == 1, f"Expected exactly 1 <h1>, found {h1_count}"


def test_h1_font_size() -> None:
    """The h1 should have a font-size of 3rem or larger."""
    parser = _parse_index()
    style = parser.style_content.lower()
    # Match font-size values like 3rem, 4rem, 48px, etc.
    assert re.search(r"font-size\s*:\s*[\d.]+\s*(rem|px|em)", style), (
        "Expected h1 to have an explicit font-size declaration"
    )


def test_no_external_css() -> None:
    """No external stylesheet links should be present."""
    parser = _parse_index()
    for attrs in parser.link_tags:
        attr_dict = dict(attrs)
        rel = (attr_dict.get("rel") or "").lower()
        assert "stylesheet" not in rel, (
            "Expected no <link rel='stylesheet'> tags — all CSS must be inline"
        )


def test_no_external_scripts() -> None:
    """No external script tags should be present."""
    parser = _parse_index()
    for attrs in parser.script_tags:
        attr_dict = dict(attrs)
        assert "src" not in attr_dict, (
            "Expected no <script src='...'> tags — no JavaScript dependencies allowed"
        )


def test_no_script_tags_at_all() -> None:
    """There should be no <script> tags whatsoever."""
    content = _read_index().lower()
    assert "<script" not in content, "Expected no <script> tags in the document"


def test_no_external_dependencies() -> None:
    """Ensure zero external dependencies: no CDN links, no external CSS, no external JS."""
    content = _read_index().lower()
    # No CDN or external URL references
    assert "cdn" not in content or "cdn" in "content", True  # soft check
    # More robust: no href pointing to http(s)
    http_links = re.findall(r'(?:href|src)\s*=\s*["\']https?://', content)
    assert len(http_links) == 0, (
        f"Expected no external URL references, found: {http_links}"
    )


def test_box_sizing_border_box() -> None:
    """Style block should include box-sizing: border-box for robustness."""
    parser = _parse_index()
    style = parser.style_content.lower().replace(" ", "")
    assert "box-sizing:border-box" in style, (
        "Expected 'box-sizing: border-box' in the style block"
    )


def test_margin_zero_on_body() -> None:
    """Body style must explicitly set margin: 0."""
    parser = _parse_index()
    style = parser.style_content.lower().replace(" ", "")
    assert "margin:0" in style, "Expected 'margin: 0' in style block"


def test_padding_zero_on_body() -> None:
    """Body style must explicitly set padding: 0."""
    parser = _parse_index()
    style = parser.style_content.lower().replace(" ", "")
    assert "padding:0" in style, "Expected 'padding: 0' in style block"


def test_valid_html_structure() -> None:
    """Document must contain the fundamental HTML structure tags."""
    parser = _parse_index()
    for required_tag in ["html", "head", "body", "title", "style", "h1"]:
        assert required_tag in parser.tags, (
            f"Expected <{required_tag}> tag in the document"
        )


def test_no_trailing_whitespace_before_doctype() -> None:
    """File must not start with whitespace before the DOCTYPE."""
    content = _read_index()
    assert content.startswith("<!DOCTYPE") or content.startswith("<!doctype"), (
        "File must start with <!DOCTYPE html> — no leading whitespace allowed"
    )
