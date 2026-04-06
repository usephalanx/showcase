"""Tests for frontend Tailwind config, global styles, and index.html setup.

Validates that the core frontend configuration files exist, contain
the expected content structures, and follow project conventions.
"""

from __future__ import annotations

import os
import re
from pathlib import Path
from typing import List

import pytest

# Resolve paths relative to the repository root
REPO_ROOT: Path = Path(__file__).resolve().parent.parent
FRONTEND_DIR: Path = REPO_ROOT / "frontend"


class TestTailwindConfig:
    """Tests for frontend/tailwind.config.js."""

    @pytest.fixture()
    def config_content(self) -> str:
        """Read and return tailwind.config.js content."""
        config_path = FRONTEND_DIR / "tailwind.config.js"
        assert config_path.exists(), "tailwind.config.js must exist in frontend/"
        return config_path.read_text(encoding="utf-8")

    def test_tailwind_config_exists(self) -> None:
        """Verify tailwind.config.js exists at the expected location."""
        assert (FRONTEND_DIR / "tailwind.config.js").exists()

    def test_tailwind_config_not_empty(self, config_content: str) -> None:
        """Verify tailwind.config.js is non-empty."""
        assert len(config_content.strip()) > 0

    def test_content_paths_include_index_html(self, config_content: str) -> None:
        """Verify content array includes index.html."""
        assert "./index.html" in config_content

    def test_content_paths_include_src(self, config_content: str) -> None:
        """Verify content array includes src directory with proper extensions."""
        assert "./src/**/*.{js,ts,jsx,tsx}" in config_content

    def test_primary_color_palette_defined(self, config_content: str) -> None:
        """Verify primary color palette is defined with multiple shades."""
        assert "primary" in config_content
        # Check for at least the 500 shade
        assert "#3b82f6" in config_content

    def test_secondary_color_palette_defined(self, config_content: str) -> None:
        """Verify secondary color palette is defined with multiple shades."""
        assert "secondary" in config_content
        assert "#8b5cf6" in config_content

    def test_accent_color_palette_defined(self, config_content: str) -> None:
        """Verify accent color palette is defined with multiple shades."""
        assert "accent" in config_content
        assert "#10b981" in config_content

    def test_surface_color_palette_defined(self, config_content: str) -> None:
        """Verify surface color palette is defined for neutral tones."""
        assert "surface" in config_content
        assert "#f8fafc" in config_content

    def test_custom_font_family_inter(self, config_content: str) -> None:
        """Verify Inter font is configured as the primary sans-serif font."""
        assert "Inter" in config_content
        assert "fontFamily" in config_content

    def test_custom_border_radius(self, config_content: str) -> None:
        """Verify custom border radius values are defined."""
        assert "borderRadius" in config_content

    def test_custom_box_shadows(self, config_content: str) -> None:
        """Verify card and board shadow utilities are defined."""
        assert "card" in config_content
        assert "card-hover" in config_content
        assert "board" in config_content

    def test_color_shades_complete(self, config_content: str) -> None:
        """Verify each color palette has a full range of shades (50-950)."""
        required_shades: List[str] = ["50", "100", "200", "300", "400", "500", "600", "700", "800", "900", "950"]
        for shade in required_shades:
            # Each shade number should appear multiple times (once per color palette)
            count = config_content.count(f"'{shade}':") + config_content.count(f"{shade}:")
            assert count >= 4, f"Shade {shade} should appear for at least 4 color palettes (primary, secondary, accent, surface)"

    def test_exports_default_config(self, config_content: str) -> None:
        """Verify the config uses ESM export default syntax."""
        assert "export default" in config_content

    def test_plugins_array_present(self, config_content: str) -> None:
        """Verify plugins array is present in config."""
        assert "plugins" in config_content

    def test_custom_animations_defined(self, config_content: str) -> None:
        """Verify custom animations are defined for UI transitions."""
        assert "animation" in config_content
        assert "keyframes" in config_content


class TestGlobalCSS:
    """Tests for frontend/src/index.css."""

    @pytest.fixture()
    def css_content(self) -> str:
        """Read and return index.css content."""
        css_path = FRONTEND_DIR / "src" / "index.css"
        assert css_path.exists(), "src/index.css must exist in frontend/src/"
        return css_path.read_text(encoding="utf-8")

    def test_index_css_exists(self) -> None:
        """Verify index.css exists at the expected location."""
        assert (FRONTEND_DIR / "src" / "index.css").exists()

    def test_index_css_not_empty(self, css_content: str) -> None:
        """Verify index.css is non-empty."""
        assert len(css_content.strip()) > 0

    def test_tailwind_base_directive(self, css_content: str) -> None:
        """Verify @tailwind base directive is present."""
        assert "@tailwind base;" in css_content

    def test_tailwind_components_directive(self, css_content: str) -> None:
        """Verify @tailwind components directive is present."""
        assert "@tailwind components;" in css_content

    def test_tailwind_utilities_directive(self, css_content: str) -> None:
        """Verify @tailwind utilities directive is present."""
        assert "@tailwind utilities;" in css_content

    def test_directives_in_correct_order(self, css_content: str) -> None:
        """Verify Tailwind directives appear in the correct order."""
        base_pos = css_content.index("@tailwind base;")
        components_pos = css_content.index("@tailwind components;")
        utilities_pos = css_content.index("@tailwind utilities;")
        assert base_pos < components_pos < utilities_pos

    def test_base_layer_exists(self, css_content: str) -> None:
        """Verify @layer base is defined."""
        assert "@layer base" in css_content

    def test_components_layer_exists(self, css_content: str) -> None:
        """Verify @layer components is defined."""
        assert "@layer components" in css_content

    def test_font_smoothing_applied(self, css_content: str) -> None:
        """Verify font smoothing CSS properties are set."""
        assert "-webkit-font-smoothing: antialiased" in css_content
        assert "-moz-osx-font-smoothing: grayscale" in css_content

    def test_inter_font_family_set(self, css_content: str) -> None:
        """Verify Inter font family is referenced in base styles."""
        assert "Inter" in css_content

    def test_body_background_and_text(self, css_content: str) -> None:
        """Verify body has surface background and text colors applied."""
        assert "bg-surface-50" in css_content
        assert "text-surface-900" in css_content

    def test_btn_primary_component(self, css_content: str) -> None:
        """Verify .btn-primary component class is defined."""
        assert ".btn-primary" in css_content
        assert "bg-primary-600" in css_content

    def test_btn_secondary_component(self, css_content: str) -> None:
        """Verify .btn-secondary component class is defined."""
        assert ".btn-secondary" in css_content

    def test_card_component(self, css_content: str) -> None:
        """Verify .card component class is defined."""
        assert ".card" in css_content
        assert "shadow-card" in css_content

    def test_heading_typography_styles(self, css_content: str) -> None:
        """Verify heading elements have base typography styles."""
        for heading in ["h1", "h2", "h3", "h4"]:
            assert heading in css_content, f"{heading} typography style should be defined"

    def test_input_field_component(self, css_content: str) -> None:
        """Verify .input-field component class is defined."""
        assert ".input-field" in css_content

    def test_badge_components(self, css_content: str) -> None:
        """Verify badge component classes are defined."""
        assert ".badge" in css_content
        assert ".badge-primary" in css_content

    def test_disabled_state_on_buttons(self, css_content: str) -> None:
        """Verify buttons have disabled state styles."""
        assert "disabled:opacity-50" in css_content
        assert "disabled:cursor-not-allowed" in css_content

    def test_focus_visible_styles(self, css_content: str) -> None:
        """Verify :focus-visible styles are defined for accessibility."""
        assert ":focus-visible" in css_content

    def test_selection_styles(self, css_content: str) -> None:
        """Verify ::selection styles are defined."""
        assert "::selection" in css_content


class TestIndexHTML:
    """Tests for frontend/index.html."""

    @pytest.fixture()
    def html_content(self) -> str:
        """Read and return index.html content."""
        html_path = FRONTEND_DIR / "index.html"
        assert html_path.exists(), "index.html must exist in frontend/"
        return html_path.read_text(encoding="utf-8")

    def test_index_html_exists(self) -> None:
        """Verify index.html exists at the expected location."""
        assert (FRONTEND_DIR / "index.html").exists()

    def test_index_html_not_empty(self, html_content: str) -> None:
        """Verify index.html is non-empty."""
        assert len(html_content.strip()) > 0

    def test_doctype_declaration(self, html_content: str) -> None:
        """Verify HTML5 doctype is declared."""
        assert "<!doctype html>" in html_content.lower() or "<!DOCTYPE html>" in html_content

    def test_html_lang_attribute(self, html_content: str) -> None:
        """Verify html element has lang attribute set to en."""
        assert 'lang="en"' in html_content

    def test_charset_meta_tag(self, html_content: str) -> None:
        """Verify charset meta tag is present."""
        assert 'charset="UTF-8"' in html_content

    def test_viewport_meta_tag(self, html_content: str) -> None:
        """Verify viewport meta tag is present with correct content."""
        assert 'name="viewport"' in html_content
        assert 'width=device-width' in html_content
        assert 'initial-scale=1.0' in html_content

    def test_description_meta_tag(self, html_content: str) -> None:
        """Verify description meta tag is present."""
        assert 'name="description"' in html_content

    def test_theme_color_meta_tag(self, html_content: str) -> None:
        """Verify theme-color meta tag matches primary-500."""
        assert 'name="theme-color"' in html_content
        assert '#3b82f6' in html_content

    def test_robots_meta_tag(self, html_content: str) -> None:
        """Verify robots meta tag allows indexing."""
        assert 'name="robots"' in html_content
        assert 'index, follow' in html_content

    def test_open_graph_type(self, html_content: str) -> None:
        """Verify Open Graph type meta tag is present."""
        assert 'property="og:type"' in html_content
        assert 'content="website"' in html_content

    def test_open_graph_title(self, html_content: str) -> None:
        """Verify Open Graph title meta tag is present."""
        assert 'property="og:title"' in html_content

    def test_open_graph_description(self, html_content: str) -> None:
        """Verify Open Graph description meta tag is present."""
        assert 'property="og:description"' in html_content

    def test_open_graph_site_name(self, html_content: str) -> None:
        """Verify Open Graph site_name meta tag is present."""
        assert 'property="og:site_name"' in html_content

    def test_open_graph_locale(self, html_content: str) -> None:
        """Verify Open Graph locale meta tag is present."""
        assert 'property="og:locale"' in html_content

    def test_twitter_card_meta_tag(self, html_content: str) -> None:
        """Verify Twitter Card meta tag is present."""
        assert 'name="twitter:card"' in html_content
        assert 'summary_large_image' in html_content

    def test_twitter_title_meta_tag(self, html_content: str) -> None:
        """Verify Twitter title meta tag is present."""
        assert 'name="twitter:title"' in html_content

    def test_twitter_description_meta_tag(self, html_content: str) -> None:
        """Verify Twitter description meta tag is present."""
        assert 'name="twitter:description"' in html_content

    def test_canonical_link(self, html_content: str) -> None:
        """Verify canonical link element is present."""
        assert 'rel="canonical"' in html_content

    def test_favicon_link(self, html_content: str) -> None:
        """Verify favicon link element is present."""
        assert 'rel="icon"' in html_content
        assert 'type="image/svg+xml"' in html_content
        assert '/vite.svg' in html_content

    def test_title_tag(self, html_content: str) -> None:
        """Verify title tag is present with expected content."""
        assert "<title>" in html_content
        assert "Kanban Board" in html_content

    def test_root_div(self, html_content: str) -> None:
        """Verify root div element is present for React mounting."""
        assert 'id="root"' in html_content

    def test_main_tsx_script(self, html_content: str) -> None:
        """Verify main.tsx module script is loaded."""
        assert 'type="module"' in html_content
        assert 'src="/src/main.tsx"' in html_content

    def test_body_classes(self, html_content: str) -> None:
        """Verify body element has proper Tailwind utility classes."""
        assert 'bg-surface-50' in html_content
        assert 'text-surface-900' in html_content
        assert 'antialiased' in html_content

    def test_noscript_fallback(self, html_content: str) -> None:
        """Verify noscript fallback is present for accessibility."""
        assert '<noscript>' in html_content

    def test_google_fonts_preconnect(self, html_content: str) -> None:
        """Verify preconnect links for Google Fonts are present."""
        assert 'fonts.googleapis.com' in html_content
        assert 'fonts.gstatic.com' in html_content

    def test_inter_font_loaded(self, html_content: str) -> None:
        """Verify Inter font is loaded from Google Fonts."""
        assert 'Inter' in html_content
        assert 'fonts.googleapis.com/css2' in html_content


class TestFavicon:
    """Tests for the favicon SVG file."""

    def test_favicon_exists(self) -> None:
        """Verify favicon SVG file exists in public directory."""
        assert (FRONTEND_DIR / "public" / "vite.svg").exists()

    def test_favicon_is_valid_svg(self) -> None:
        """Verify favicon file contains valid SVG markup."""
        content = (FRONTEND_DIR / "public" / "vite.svg").read_text(encoding="utf-8")
        assert '<svg' in content
        assert '</svg>' in content
        assert 'xmlns="http://www.w3.org/2000/svg"' in content

    def test_favicon_uses_primary_color(self) -> None:
        """Verify favicon uses the primary brand color."""
        content = (FRONTEND_DIR / "public" / "vite.svg").read_text(encoding="utf-8")
        assert '#3b82f6' in content
