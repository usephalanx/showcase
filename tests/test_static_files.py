"""Tests for static scaffolding files: index.html and src/index.css.

Verifies that the HTML entry point and global stylesheet exist with
the required content and structure.
"""

from pathlib import Path

import pytest

ROOT_DIR = Path(__file__).resolve().parent.parent


class TestIndexHtml:
    """Tests for the index.html entry point."""

    @pytest.fixture()
    def html_content(self) -> str:
        """Read and return the contents of index.html."""
        path = ROOT_DIR / "index.html"
        assert path.exists(), "index.html must exist at the project root"
        return path.read_text(encoding="utf-8")

    def test_index_html_exists(self) -> None:
        """index.html exists at the project root."""
        path = ROOT_DIR / "index.html"
        assert path.exists()

    def test_has_doctype(self, html_content: str) -> None:
        """index.html starts with a DOCTYPE declaration."""
        assert html_content.strip().startswith("<!DOCTYPE html>")

    def test_has_root_div(self, html_content: str) -> None:
        """index.html contains a div with id='root'."""
        assert 'id="root"' in html_content

    def test_has_lang_attribute(self, html_content: str) -> None:
        """index.html has a lang attribute on the html element."""
        assert 'lang="en"' in html_content

    def test_has_meta_charset(self, html_content: str) -> None:
        """index.html specifies UTF-8 charset."""
        assert 'charset="UTF-8"' in html_content

    def test_has_viewport_meta(self, html_content: str) -> None:
        """index.html includes a viewport meta tag."""
        assert 'name="viewport"' in html_content

    def test_has_script_module(self, html_content: str) -> None:
        """index.html includes a module script pointing to main.tsx."""
        assert 'type="module"' in html_content
        assert "src=" in html_content
        assert "main.tsx" in html_content

    def test_has_title(self, html_content: str) -> None:
        """index.html contains a title element."""
        assert "<title>" in html_content
        assert "</title>" in html_content


class TestIndexCss:
    """Tests for src/index.css global styles."""

    @pytest.fixture()
    def css_content(self) -> str:
        """Read and return the contents of src/index.css."""
        path = ROOT_DIR / "src" / "index.css"
        assert path.exists(), "src/index.css must exist"
        return path.read_text(encoding="utf-8")

    def test_index_css_exists(self) -> None:
        """src/index.css exists."""
        path = ROOT_DIR / "src" / "index.css"
        assert path.exists()

    def test_has_box_sizing_reset(self, css_content: str) -> None:
        """src/index.css includes a box-sizing: border-box reset."""
        assert "box-sizing" in css_content
        assert "border-box" in css_content

    def test_has_font_family(self, css_content: str) -> None:
        """src/index.css specifies a font-family."""
        assert "font-family" in css_content

    def test_has_body_rule(self, css_content: str) -> None:
        """src/index.css contains a body rule."""
        assert "body" in css_content

    def test_has_centered_layout(self, css_content: str) -> None:
        """src/index.css uses flexbox or similar for centered layout."""
        assert "display: flex" in css_content or "display:flex" in css_content
        assert "justify-content: center" in css_content or "justify-content:center" in css_content

    def test_has_root_selector(self, css_content: str) -> None:
        """src/index.css styles the #root element."""
        assert "#root" in css_content

    def test_has_max_width(self, css_content: str) -> None:
        """src/index.css constrains the root element width."""
        assert "max-width" in css_content

    def test_has_universal_reset(self, css_content: str) -> None:
        """src/index.css includes a universal selector reset."""
        assert "*" in css_content
        assert "margin: 0" in css_content or "margin:0" in css_content
        assert "padding: 0" in css_content or "padding:0" in css_content
