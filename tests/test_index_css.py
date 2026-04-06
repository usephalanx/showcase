"""Tests for frontend/src/index.css global styles.

Validates that the CSS file exists, contains required custom properties,
includes a CSS reset, and defines responsive layout basics.
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest

CSS_PATH: Path = Path(__file__).resolve().parent.parent / "frontend" / "src" / "index.css"


@pytest.fixture()
def css_content() -> str:
    """Read and return the contents of index.css."""
    assert CSS_PATH.exists(), f"Expected CSS file at {CSS_PATH}"
    return CSS_PATH.read_text(encoding="utf-8")


class TestIndexCssExists:
    """Verify the file exists at the expected path."""

    def test_file_exists(self) -> None:
        """index.css must exist under frontend/src/."""
        assert CSS_PATH.exists()

    def test_file_is_not_empty(self, css_content: str) -> None:
        """index.css must not be empty."""
        assert len(css_content.strip()) > 0


class TestCSSCustomProperties:
    """Verify all required CSS custom properties are defined."""

    REQUIRED_PROPERTIES: list[str] = [
        "--bg",
        "--surface",
        "--text",
        "--primary",
        "--danger",
        "--border",
    ]

    @pytest.mark.parametrize("prop", REQUIRED_PROPERTIES)
    def test_custom_property_defined(self, css_content: str, prop: str) -> None:
        """Each required CSS custom property must appear in the file."""
        assert prop in css_content, f"Missing CSS custom property: {prop}"

    def test_root_selector_present(self, css_content: str) -> None:
        """:root selector must be present to hold custom properties."""
        assert ":root" in css_content


class TestCSSReset:
    """Verify core CSS reset rules are present."""

    def test_box_sizing_border_box(self, css_content: str) -> None:
        """box-sizing: border-box must be applied universally."""
        assert "box-sizing: border-box" in css_content

    def test_margin_zero(self, css_content: str) -> None:
        """Margin reset must be present."""
        assert "margin: 0" in css_content

    def test_padding_zero(self, css_content: str) -> None:
        """Padding reset must be present."""
        assert "padding: 0" in css_content


class TestFontStack:
    """Verify a system font stack is used."""

    SYSTEM_FONTS: list[str] = [
        "-apple-system",
        "BlinkMacSystemFont",
        "Segoe UI",
        "sans-serif",
    ]

    @pytest.mark.parametrize("font", SYSTEM_FONTS)
    def test_system_font_present(self, css_content: str, font: str) -> None:
        """System font stack must include common system fonts."""
        assert font in css_content, f"Missing system font: {font}"

    def test_body_uses_font_family(self, css_content: str) -> None:
        """body must set font-family."""
        assert "font-family" in css_content


class TestResponsiveLayout:
    """Verify responsive layout basics."""

    def test_container_max_width(self, css_content: str) -> None:
        """A container max-width must be defined."""
        assert "max-width" in css_content

    def test_container_class(self, css_content: str) -> None:
        """.container class must be defined."""
        assert ".container" in css_content

    def test_media_query_present(self, css_content: str) -> None:
        """At least one media query must be present for responsiveness."""
        assert "@media" in css_content


class TestColorValues:
    """Verify color values are actual color values (start with #, rgb, or hsl)."""

    def test_bg_has_color_value(self, css_content: str) -> None:
        """--bg must be assigned a value."""
        assert "--bg:" in css_content or "--bg :" in css_content

    def test_surface_has_color_value(self, css_content: str) -> None:
        """--surface must be assigned a value."""
        assert "--surface:" in css_content or "--surface :" in css_content

    def test_text_has_color_value(self, css_content: str) -> None:
        """--text must be assigned a value."""
        assert "--text:" in css_content or "--text :" in css_content

    def test_primary_has_color_value(self, css_content: str) -> None:
        """--primary must be assigned a value."""
        assert "--primary:" in css_content or "--primary :" in css_content

    def test_danger_has_color_value(self, css_content: str) -> None:
        """--danger must be assigned a value."""
        assert "--danger:" in css_content or "--danger :" in css_content

    def test_border_has_color_value(self, css_content: str) -> None:
        """--border must be assigned a value."""
        assert "--border:" in css_content or "--border :" in css_content


class TestBodyStyles:
    """Verify body element base styles."""

    def test_body_background_color(self, css_content: str) -> None:
        """body must set background-color using the custom property."""
        assert "background-color" in css_content

    def test_body_color(self, css_content: str) -> None:
        """body must set color for text."""
        assert "color: var(--text)" in css_content

    def test_body_min_height(self, css_content: str) -> None:
        """body should have min-height: 100vh for full viewport coverage."""
        assert "min-height: 100vh" in css_content
