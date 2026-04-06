"""Tests validating the structure and content of src/index.css.

These are simple textual / structural checks – no CSS parser required.
"""

from __future__ import annotations

from pathlib import Path

import pytest

INDEX_CSS_PATH: Path = Path(__file__).resolve().parent.parent / "src" / "index.css"


@pytest.fixture()
def css_content() -> str:
    """Read and return the full text of src/index.css."""
    assert INDEX_CSS_PATH.exists(), f"{INDEX_CSS_PATH} does not exist"
    return INDEX_CSS_PATH.read_text(encoding="utf-8")


class TestIndexCssExists:
    """Ensure src/index.css is present."""

    def test_file_exists(self) -> None:
        """src/index.css must exist."""
        assert INDEX_CSS_PATH.exists()

    def test_file_is_not_empty(self, css_content: str) -> None:
        """src/index.css must not be empty."""
        assert len(css_content.strip()) > 0


class TestCssReset:
    """Verify the file contains a CSS reset."""

    def test_box_sizing_border_box(self, css_content: str) -> None:
        """The reset must set box-sizing: border-box."""
        assert "box-sizing: border-box" in css_content

    def test_margin_zero(self, css_content: str) -> None:
        """The reset must zero out margins."""
        assert "margin: 0" in css_content

    def test_padding_zero(self, css_content: str) -> None:
        """The reset must zero out padding."""
        assert "padding: 0" in css_content

    def test_universal_selector(self, css_content: str) -> None:
        """The reset must use the universal selector."""
        assert "*," in css_content or "* {" in css_content or "*::" in css_content


class TestSystemFontStack:
    """Verify a system font stack is defined."""

    def test_contains_apple_system(self, css_content: str) -> None:
        """Must reference -apple-system."""
        assert "-apple-system" in css_content

    def test_contains_segoe_ui(self, css_content: str) -> None:
        """Must reference Segoe UI."""
        assert "Segoe UI" in css_content

    def test_contains_roboto(self, css_content: str) -> None:
        """Must reference Roboto."""
        assert "Roboto" in css_content

    def test_contains_sans_serif(self, css_content: str) -> None:
        """Must include a generic sans-serif fallback."""
        assert "sans-serif" in css_content

    def test_font_family_custom_property(self, css_content: str) -> None:
        """A --font-family custom property should be defined."""
        assert "--font-family" in css_content


class TestNeutralColorPalette:
    """Verify a neutral colour palette is provided via custom properties."""

    @pytest.mark.parametrize(
        "token",
        [
            "--color-white",
            "--color-gray-50",
            "--color-gray-100",
            "--color-gray-200",
            "--color-gray-300",
            "--color-gray-400",
            "--color-gray-500",
            "--color-gray-600",
            "--color-gray-700",
            "--color-gray-800",
            "--color-gray-900",
            "--color-black",
        ],
    )
    def test_neutral_color_defined(self, css_content: str, token: str) -> None:
        """Each neutral colour token must be present."""
        assert token in css_content

    def test_semantic_bg_token(self, css_content: str) -> None:
        """A semantic --color-bg token must be defined."""
        assert "--color-bg" in css_content

    def test_semantic_text_token(self, css_content: str) -> None:
        """A semantic --color-text token must be defined."""
        assert "--color-text" in css_content

    def test_semantic_border_token(self, css_content: str) -> None:
        """A semantic --color-border token must be defined."""
        assert "--color-border" in css_content


class TestContainerMaxWidth:
    """Verify a container class with max-width is defined."""

    def test_container_class_exists(self, css_content: str) -> None:
        """A .container rule must be present."""
        assert ".container" in css_content

    def test_max_width_property(self, css_content: str) -> None:
        """The file must set a max-width."""
        assert "max-width" in css_content

    def test_container_max_width_custom_property(self, css_content: str) -> None:
        """A --container-max-width custom property should be defined."""
        assert "--container-max-width" in css_content

    def test_margin_auto_centering(self, css_content: str) -> None:
        """Container should be centred with auto margins."""
        assert "margin-inline: auto" in css_content or "margin: 0 auto" in css_content


class TestBodyStyles:
    """Verify base body styles are set."""

    def test_body_background(self, css_content: str) -> None:
        """Body must set a background-color."""
        assert "background-color" in css_content

    def test_body_color(self, css_content: str) -> None:
        """Body must set a text color."""
        # Look for 'color:' on a body rule; we'll just check 'color:' is present
        assert "color:" in css_content

    def test_body_font_family(self, css_content: str) -> None:
        """Body must apply the font-family."""
        assert "font-family" in css_content

    def test_body_line_height(self, css_content: str) -> None:
        """Body must set line-height."""
        assert "line-height" in css_content
