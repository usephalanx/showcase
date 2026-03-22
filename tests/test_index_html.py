"""Tests for index.html to verify structure, content, and styling.

Validates the Hello World page meets all acceptance criteria including
HTML5 doctype, proper structure, centered heading via flexbox, and
no external dependencies.
"""

from __future__ import annotations

import os
import re
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import pytest

INDEX_PATH: Path = Path(__file__).resolve().parent.parent / "index.html"


class HTMLStructureParser(HTMLParser):
    """Custom HTML parser that extracts structural information from an HTML document.

    Collects tags, attributes, and text content for validation.
    """

    def __init__(self) -> None:
        """Initialise the parser with empty collection structures."""
        super().__init__()
        self.tags: List[Tuple[str, Dict[str, Optional[str]]]] = []
        self.end_tags: List[str] = []
        self.text_content: Dict[str, List[str]] = {}
        self._current_tag: Optional[str] = None

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, Optional[str]]]) -> None:
        """Record an opening tag and its attributes.

        Args:
            tag: The tag name.
            attrs: A list of (attribute, value) pairs.
        """
        attr_dict = dict(attrs)
        self.tags.append((tag, attr_dict))
        self._current_tag = tag

    def handle_endtag(self, tag: str) -> None:
        """Record a closing tag.

        Args:
            tag: The tag name.
        """
        self.end_tags.append(tag)
        self._current_tag = None

    def handle_data(self, data: str) -> None:
        """Record text content associated with the current tag.

        Args:
            data: The text content.
        """
        if self._current_tag:
            if self._current_tag not in self.text_content:
                self.text_content[self._current_tag] = []
            stripped = data.strip()
            if stripped:
                self.text_content[self._current_tag].append(stripped)


@pytest.fixture(name="html_content")
def fixture_html_content() -> str:
    """Read and return the contents of index.html.

    Returns:
        The full text content of index.html.
    """
    return INDEX_PATH.read_text(encoding="utf-8")


@pytest.fixture(name="parsed")
def fixture_parsed(html_content: str) -> HTMLStructureParser:
    """Parse index.html and return the structure parser.

    Args:
        html_content: The raw HTML string.

    Returns:
        An HTMLStructureParser populated with the document's structure.
    """
    parser = HTMLStructureParser()
    parser.feed(html_content)
    return parser


def test_file_exists() -> None:
    """Verify index.html exists at the project root."""
    assert INDEX_PATH.exists(), f"index.html not found at {INDEX_PATH}"
    assert INDEX_PATH.is_file(), "index.html is not a regular file"


def test_has_html5_doctype(html_content: str) -> None:
    """Verify the first line contains '<!DOCTYPE html>'."""
    first_line = html_content.strip().splitlines()[0].strip()
    assert first_line.lower() == "<!doctype html>", (
        f"Expected '<!DOCTYPE html>' as first line, got: {first_line!r}"
    )


def test_has_h1_with_hello_world(parsed: HTMLStructureParser) -> None:
    """Verify there is exactly one h1 element with text content 'Hello World'."""
    h1_tags = [(tag, attrs) for tag, attrs in parsed.tags if tag == "h1"]
    assert len(h1_tags) == 1, f"Expected exactly 1 <h1> tag, found {len(h1_tags)}"

    h1_texts = parsed.text_content.get("h1", [])
    assert len(h1_texts) == 1, f"Expected exactly 1 text node in <h1>, found {len(h1_texts)}"
    assert h1_texts[0] == "Hello World", (
        f"Expected h1 text to be 'Hello World', got: {h1_texts[0]!r}"
    )


def test_body_has_flexbox_centering(parsed: HTMLStructureParser) -> None:
    """Verify the body tag's style attribute contains flexbox centering properties."""
    body_tags = [(tag, attrs) for tag, attrs in parsed.tags if tag == "body"]
    assert len(body_tags) == 1, f"Expected exactly 1 <body> tag, found {len(body_tags)}"

    _, attrs = body_tags[0]
    style = attrs.get("style", "")
    assert style is not None, "<body> tag must have a style attribute"

    # Normalise whitespace for matching
    style_normalised = re.sub(r"\s+", "", style)

    required_properties = [
        "display:flex",
        "justify-content:center",
        "align-items:center",
    ]
    for prop in required_properties:
        assert prop in style_normalised, (
            f"Missing '{prop}' in body style attribute. Got: {style!r}"
        )


def test_body_has_margin_zero(parsed: HTMLStructureParser) -> None:
    """Verify the body style includes margin:0 to remove default browser margin."""
    body_tags = [(tag, attrs) for tag, attrs in parsed.tags if tag == "body"]
    _, attrs = body_tags[0]
    style = attrs.get("style", "")
    style_normalised = re.sub(r"\s+", "", style or "")
    assert "margin:0" in style_normalised, (
        f"Body style must include 'margin:0'. Got: {style!r}"
    )


def test_body_has_min_height_100vh(parsed: HTMLStructureParser) -> None:
    """Verify the body style includes min-height:100vh for full viewport centering."""
    body_tags = [(tag, attrs) for tag, attrs in parsed.tags if tag == "body"]
    _, attrs = body_tags[0]
    style = attrs.get("style", "")
    style_normalised = re.sub(r"\s+", "", style or "")
    assert "min-height:100vh" in style_normalised, (
        f"Body style must include 'min-height:100vh'. Got: {style!r}"
    )


def test_no_external_dependencies(html_content: str) -> None:
    """Verify there are no external stylesheet links, script sources, or @import rules."""
    content_lower = html_content.lower()

    # No <link rel="stylesheet"> tags
    assert "<link" not in content_lower or 'rel="stylesheet"' not in content_lower, (
        "Found external stylesheet <link> tag; the page must be self-contained"
    )

    # No <script src="..."> tags
    script_src_pattern = re.compile(r"<script[^>]+src\s*=", re.IGNORECASE)
    assert not script_src_pattern.search(html_content), (
        "Found <script src=...> tag; the page must have no external scripts"
    )

    # No @import rules
    assert "@import" not in content_lower, (
        "Found @import rule; the page must have no external imports"
    )


def test_valid_html5_structure(parsed: HTMLStructureParser) -> None:
    """Verify presence of html, head, and body tags, plus lang attribute on html."""
    tag_names = [tag for tag, _ in parsed.tags]

    assert "html" in tag_names, "Missing <html> tag"
    assert "head" in tag_names, "Missing <head> tag"
    assert "body" in tag_names, "Missing <body> tag"

    # Check lang attribute on <html>
    html_tags = [(tag, attrs) for tag, attrs in parsed.tags if tag == "html"]
    assert len(html_tags) >= 1, "Missing <html> tag"
    _, html_attrs = html_tags[0]
    assert html_attrs.get("lang") == "en", (
        f"Expected lang='en' on <html>, got: {html_attrs.get('lang')!r}"
    )


def test_has_charset_meta(parsed: HTMLStructureParser) -> None:
    """Verify a <meta charset="UTF-8"> tag is present in the document."""
    meta_tags = [(tag, attrs) for tag, attrs in parsed.tags if tag == "meta"]
    charset_metas = [
        attrs for _, attrs in meta_tags
        if attrs.get("charset", "").upper() == "UTF-8"
    ]
    assert len(charset_metas) >= 1, "Missing <meta charset='UTF-8'> tag"


def test_has_viewport_meta(parsed: HTMLStructureParser) -> None:
    """Verify a viewport meta tag is present for mobile rendering."""
    meta_tags = [(tag, attrs) for tag, attrs in parsed.tags if tag == "meta"]
    viewport_metas = [
        attrs for _, attrs in meta_tags
        if attrs.get("name", "").lower() == "viewport"
    ]
    assert len(viewport_metas) >= 1, "Missing <meta name='viewport'> tag"


def test_has_title(parsed: HTMLStructureParser) -> None:
    """Verify the document has a <title> tag with 'Hello World' content."""
    title_tags = [(tag, attrs) for tag, attrs in parsed.tags if tag == "title"]
    assert len(title_tags) >= 1, "Missing <title> tag"

    title_texts = parsed.text_content.get("title", [])
    assert len(title_texts) >= 1, "<title> tag has no text content"
    assert title_texts[0] == "Hello World", (
        f"Expected title 'Hello World', got: {title_texts[0]!r}"
    )


def test_well_formed_html(parsed: HTMLStructureParser) -> None:
    """Verify all major opened tags are properly closed."""
    # Self-closing/void tags that don't require closing
    void_tags = {
        "meta", "link", "br", "hr", "img", "input",
        "area", "base", "col", "embed", "source", "track", "wbr",
    }

    opened = [tag for tag, _ in parsed.tags if tag not in void_tags]
    closed = list(parsed.end_tags)

    for tag in ["html", "head", "body", "h1", "title"]:
        open_count = opened.count(tag)
        close_count = closed.count(tag)
        assert open_count == close_count, (
            f"Tag <{tag}> opened {open_count} time(s) but closed {close_count} time(s)"
        )


def test_no_other_html_css_js_files() -> None:
    """Verify no other HTML, CSS, or JS files were created at the project root."""
    project_root = INDEX_PATH.parent
    for ext in ("*.html", "*.css", "*.js"):
        files = list(project_root.glob(ext))
        if ext == "*.html":
            # Only index.html should exist
            html_files = [f.name for f in files]
            assert html_files == ["index.html"] or set(html_files) == {"index.html"}, (
                f"Expected only index.html but found: {html_files}"
            )
        else:
            assert len(files) == 0, (
                f"Unexpected {ext} files found at project root: {[f.name for f in files]}"
            )
