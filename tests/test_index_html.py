"""Tests for index.html structure, styling, and content.

Validates that the Hello World page meets all requirements:
- HTML5 doctype and semantic structure
- Embedded flexbox centering styles
- Single <h1> with correct text and large font-size
- No external resources or frameworks
"""

from __future__ import annotations

import os
import re
from pathlib import Path
from html.parser import HTMLParser
from typing import Any, Dict, List, Optional, Tuple

import pytest

# Resolve the project root (parent of tests/)
PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent
INDEX_HTML_PATH: Path = PROJECT_ROOT / "index.html"


class SimpleHTMLAnalyzer(HTMLParser):
    """A lightweight HTML parser that collects structural information.

    Attributes:
        tags: List of (tag, attrs_dict) tuples in document order.
        tag_stack: Current nesting stack of open tags.
        tag_contents: Mapping from tag name to list of text content strings.
        style_contents: List of text contents found inside <style> tags.
        current_tag: The tag currently being processed.
        inside: Set of ancestor tags for current position.
        head_tags: Tags found inside <head>.
        body_tags: Tags found inside <body>.
        link_tags: All <link> tag attribute dicts.
        script_tags: All <script> tag attribute dicts.
        img_tags: All <img> tag attribute dicts.
        title_text: Text content of the <title> tag.
        h1_texts: List of text content of all <h1> tags.
        h1_count: Number of <h1> tags found in <body>.
    """

    def __init__(self) -> None:
        """Initialise the parser with empty collections."""
        super().__init__()
        self.tags: List[Tuple[str, Dict[str, Optional[str]]]] = []
        self.tag_stack: List[str] = []
        self.style_contents: List[str] = []
        self.current_tag: Optional[str] = None
        self.head_tags: List[Tuple[str, Dict[str, Optional[str]]]] = []
        self.body_tags: List[Tuple[str, Dict[str, Optional[str]]]] = []
        self.link_tags: List[Dict[str, Optional[str]]] = []
        self.script_tags: List[Dict[str, Optional[str]]] = []
        self.img_tags: List[Dict[str, Optional[str]]] = []
        self.title_text: str = ""
        self.h1_texts: List[str] = []
        self.h1_count: int = 0
        self._current_text_buffer: str = ""
        self._in_head: bool = False
        self._in_body: bool = False
        self._in_style: bool = False
        self._in_title: bool = False
        self._in_h1: bool = False
        self._html_attrs: Dict[str, Optional[str]] = {}

    def handle_starttag(self, tag: str, attrs: list[tuple[str, Optional[str]]]) -> None:
        """Record tag and attributes, track nesting context."""
        attrs_dict = dict(attrs)
        self.tags.append((tag, attrs_dict))
        self.tag_stack.append(tag)
        self.current_tag = tag

        if tag == "html":
            self._html_attrs = attrs_dict
        elif tag == "head":
            self._in_head = True
        elif tag == "body":
            self._in_body = True
        elif tag == "style" and self._in_head:
            self._in_style = True
            self._current_text_buffer = ""
        elif tag == "title" and self._in_head:
            self._in_title = True
            self._current_text_buffer = ""
        elif tag == "h1" and self._in_body:
            self._in_h1 = True
            self.h1_count += 1
            self._current_text_buffer = ""
        elif tag == "link":
            self.link_tags.append(attrs_dict)
        elif tag == "script":
            self.script_tags.append(attrs_dict)
        elif tag == "img":
            self.img_tags.append(attrs_dict)

        if self._in_head:
            self.head_tags.append((tag, attrs_dict))
        if self._in_body:
            self.body_tags.append((tag, attrs_dict))

    def handle_endtag(self, tag: str) -> None:
        """Track closing tags and finalise collected text."""
        if tag == "style" and self._in_style:
            self._in_style = False
            self.style_contents.append(self._current_text_buffer)
        elif tag == "title" and self._in_title:
            self._in_title = False
            self.title_text = self._current_text_buffer.strip()
        elif tag == "h1" and self._in_h1:
            self._in_h1 = False
            self.h1_texts.append(self._current_text_buffer.strip())
        elif tag == "head":
            self._in_head = False
        elif tag == "body":
            self._in_body = False

        if self.tag_stack and self.tag_stack[-1] == tag:
            self.tag_stack.pop()

    def handle_data(self, data: str) -> None:
        """Collect text data within relevant tags."""
        if self._in_style or self._in_title or self._in_h1:
            self._current_text_buffer += data

    @property
    def html_lang(self) -> Optional[str]:
        """Return the lang attribute of the <html> tag, if present."""
        return self._html_attrs.get("lang")


@pytest.fixture(scope="module")
def raw_content() -> str:
    """Read and return the raw file content of index.html."""
    assert INDEX_HTML_PATH.exists(), f"index.html not found at {INDEX_HTML_PATH}"
    return INDEX_HTML_PATH.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def parsed(raw_content: str) -> SimpleHTMLAnalyzer:
    """Parse index.html and return the analyser with collected data."""
    analyzer = SimpleHTMLAnalyzer()
    analyzer.feed(raw_content)
    return analyzer


@pytest.fixture(scope="module")
def style_text(parsed: SimpleHTMLAnalyzer) -> str:
    """Return the combined text content of all <style> blocks."""
    return "\n".join(parsed.style_contents)


# ---- Test 1 ----
def test_file_exists() -> None:
    """Assert that index.html exists at the project root."""
    assert INDEX_HTML_PATH.exists(), f"Expected index.html at {INDEX_HTML_PATH}"
    assert INDEX_HTML_PATH.is_file(), "index.html must be a regular file"


# ---- Test 2 ----
def test_has_html5_doctype(raw_content: str) -> None:
    """Assert the very first line is the HTML5 doctype declaration."""
    first_line = raw_content.strip().splitlines()[0].strip()
    assert first_line.lower() == "<!doctype html>", (
        f"Expected '<!DOCTYPE html>' as first line, got '{first_line}'"
    )


# ---- Test 3 ----
def test_has_html_lang_attribute(parsed: SimpleHTMLAnalyzer) -> None:
    """Assert the <html> tag has a 'lang' attribute."""
    assert parsed.html_lang is not None, "<html> tag must have a 'lang' attribute"
    assert len(parsed.html_lang) > 0, "'lang' attribute must not be empty"


# ---- Test 4 ----
def test_has_meta_charset(parsed: SimpleHTMLAnalyzer) -> None:
    """Assert a <meta charset='UTF-8'> tag exists inside <head>."""
    charset_metas = [
        attrs
        for tag, attrs in parsed.head_tags
        if tag == "meta" and "charset" in attrs
    ]
    assert len(charset_metas) > 0, "Expected <meta charset=...> in <head>"
    charset_value = charset_metas[0]["charset"]
    assert charset_value is not None and charset_value.upper() == "UTF-8", (
        f"Expected charset='UTF-8', got '{charset_value}'"
    )


# ---- Test 5 ----
def test_has_meta_viewport(parsed: SimpleHTMLAnalyzer) -> None:
    """Assert a <meta name='viewport'> tag exists inside <head>."""
    viewport_metas = [
        attrs
        for tag, attrs in parsed.head_tags
        if tag == "meta" and attrs.get("name", "").lower() == "viewport"
    ]
    assert len(viewport_metas) > 0, "Expected <meta name='viewport'> in <head>"
    assert viewport_metas[0].get("content"), "viewport meta must have 'content' attribute"


# ---- Test 6 ----
def test_has_title(parsed: SimpleHTMLAnalyzer) -> None:
    """Assert a <title> tag exists inside <head> with non-empty text."""
    title_tags = [tag for tag, _ in parsed.head_tags if tag == "title"]
    assert len(title_tags) > 0, "Expected <title> in <head>"
    assert len(parsed.title_text) > 0, "<title> must have non-empty text content"


# ---- Test 7 ----
def test_has_style_block(parsed: SimpleHTMLAnalyzer, style_text: str) -> None:
    """Assert at least one <style> tag exists inside <head> with content."""
    style_tags = [tag for tag, _ in parsed.head_tags if tag == "style"]
    assert len(style_tags) > 0, "Expected <style> in <head>"
    assert len(style_text.strip()) > 0, "<style> block must have non-empty content"


# ---- Test 8 ----
def test_style_contains_flexbox_centering(style_text: str) -> None:
    """Assert the style block contains flexbox centering properties."""
    normalized = style_text.replace(" ", "").lower()
    assert "display:flex" in normalized, "Style must contain 'display: flex'"
    assert "justify-content:center" in normalized, "Style must contain 'justify-content: center'"
    assert "align-items:center" in normalized, "Style must contain 'align-items: center'"


# ---- Test 9 ----
def test_style_contains_full_height(style_text: str) -> None:
    """Assert the style block sets height to 100% or 100vh."""
    normalized = style_text.replace(" ", "").lower()
    has_100_percent = "height:100%" in normalized
    has_100vh = "height:100vh" in normalized
    has_min_100vh = "min-height:100vh" in normalized
    assert has_100_percent or has_100vh or has_min_100vh, (
        "Style must contain 'height: 100%', 'height: 100vh', or 'min-height: 100vh'"
    )


# ---- Test 10 ----
def test_body_contains_h1(parsed: SimpleHTMLAnalyzer) -> None:
    """Assert exactly one <h1> tag exists inside <body>."""
    assert parsed.h1_count == 1, (
        f"Expected exactly 1 <h1> in <body>, found {parsed.h1_count}"
    )


# ---- Test 11 ----
def test_h1_text_is_hello_world(parsed: SimpleHTMLAnalyzer) -> None:
    """Assert the <h1> tag's text content is 'Hello World'."""
    assert len(parsed.h1_texts) > 0, "No <h1> text content found"
    assert parsed.h1_texts[0] == "Hello World", (
        f"Expected h1 text 'Hello World', got '{parsed.h1_texts[0]}'"
    )


# ---- Test 12 ----
def test_h1_font_size_at_least_4rem(style_text: str) -> None:
    """Assert the h1 rule includes font-size of 4rem or larger."""
    # Look for font-size declarations with rem units
    matches = re.findall(r"font-size\s*:\s*([\d.]+)\s*rem", style_text)
    assert len(matches) > 0, "Expected a font-size declaration with rem units in style"
    sizes = [float(m) for m in matches]
    assert any(s >= 4.0 for s in sizes), (
        f"Expected font-size >= 4rem, found sizes: {sizes}"
    )


# ---- Test 13 ----
def test_no_external_resources(parsed: SimpleHTMLAnalyzer, raw_content: str) -> None:
    """Assert no external stylesheets, scripts with src, or images exist."""
    # No <link rel="stylesheet">
    stylesheet_links = [
        attrs
        for attrs in parsed.link_tags
        if attrs.get("rel", "").lower() == "stylesheet"
    ]
    assert len(stylesheet_links) == 0, "No external stylesheets allowed"

    # No <script src="...">
    external_scripts = [
        attrs
        for attrs in parsed.script_tags
        if "src" in attrs
    ]
    assert len(external_scripts) == 0, "No external scripts allowed"

    # No <img> tags
    assert len(parsed.img_tags) == 0, "No <img> tags allowed"


# ---- Test 14 ----
def test_file_is_self_contained() -> None:
    """Assert no .css, .js, or other asset files are referenced alongside index.html."""
    # Check that no separate .css or .js files exist at the project root
    # that would indicate the page is not self-contained
    for ext in (".css", ".js"):
        asset_files = list(PROJECT_ROOT.glob(f"*{ext}"))
        assert len(asset_files) == 0, (
            f"Found external {ext} files at project root: {asset_files}. "
            f"The page must be fully self-contained in index.html."
        )
