"""Tests for index.html structure and content.

Validates that the HTML entry point contains the required elements
for a Vite + React application.
"""

from __future__ import annotations

from pathlib import Path

import pytest

ROOT_DIR = Path(__file__).resolve().parent.parent
INDEX_HTML_PATH = ROOT_DIR / "index.html"


@pytest.fixture()
def index_html_content() -> str:
    """Read and return the contents of index.html."""
    assert INDEX_HTML_PATH.exists(), "index.html must exist at the project root"
    return INDEX_HTML_PATH.read_text(encoding="utf-8")


def test_index_html_exists() -> None:
    """index.html should exist at the project root."""
    assert INDEX_HTML_PATH.exists()


def test_doctype_present(index_html_content: str) -> None:
    """index.html should start with an HTML5 doctype declaration."""
    assert index_html_content.strip().startswith("<!DOCTYPE html>")


def test_html_lang_attribute(index_html_content: str) -> None:
    """The <html> element should have a lang attribute set to 'en'."""
    assert '<html lang="en">' in index_html_content


def test_meta_charset(index_html_content: str) -> None:
    """A UTF-8 charset meta tag should be present."""
    assert '<meta charset="UTF-8"' in index_html_content


def test_meta_viewport(index_html_content: str) -> None:
    """A viewport meta tag should be present for responsive design."""
    assert 'name="viewport"' in index_html_content
    assert 'width=device-width' in index_html_content


def test_root_div(index_html_content: str) -> None:
    """A <div id='root'></div> mount point should be present."""
    assert '<div id="root"></div>' in index_html_content


def test_script_module_tag(index_html_content: str) -> None:
    """A script tag with type='module' pointing to /src/main.tsx should exist."""
    assert '<script type="module" src="/src/main.tsx"></script>' in index_html_content


def test_title_present(index_html_content: str) -> None:
    """The page should have a <title> element."""
    assert "<title>" in index_html_content
    assert "</title>" in index_html_content
