"""Tests to verify the static/index.html file exists and is well-formed."""

from __future__ import annotations

from pathlib import Path


STATIC_HTML_PATH = Path(__file__).parent.parent / "static" / "index.html"


def test_static_index_html_exists() -> None:
    """The static/index.html file must exist in the project."""
    assert STATIC_HTML_PATH.exists(), f"Expected {STATIC_HTML_PATH} to exist"


def test_static_index_html_is_not_empty() -> None:
    """The static/index.html file must not be empty."""
    content = STATIC_HTML_PATH.read_text(encoding="utf-8")
    assert len(content.strip()) > 0


def test_static_index_html_has_html_structure() -> None:
    """The static/index.html must have basic HTML5 structure."""
    content = STATIC_HTML_PATH.read_text(encoding="utf-8")
    assert "<!DOCTYPE html>" in content
    assert "<html" in content
    assert "<head>" in content
    assert "<body>" in content
    assert "</html>" in content


def test_static_index_html_has_style_tag() -> None:
    """The static/index.html must contain inline CSS."""
    content = STATIC_HTML_PATH.read_text(encoding="utf-8")
    assert "<style>" in content
    assert "</style>" in content


def test_static_index_html_has_script_tag() -> None:
    """The static/index.html must contain inline JavaScript."""
    content = STATIC_HTML_PATH.read_text(encoding="utf-8")
    assert "<script>" in content
    assert "</script>" in content


def test_static_index_html_has_charset() -> None:
    """The static/index.html must declare UTF-8 charset."""
    content = STATIC_HTML_PATH.read_text(encoding="utf-8")
    assert 'charset="UTF-8"' in content or "charset=utf-8" in content.lower()


def test_static_index_html_has_title() -> None:
    """The static/index.html must have a <title> element."""
    content = STATIC_HTML_PATH.read_text(encoding="utf-8")
    assert "<title>" in content
    assert "Todo App" in content
