"""Tests validating the frontend entry files exist and contain expected content.

These tests verify the structural correctness of index.html, main.tsx,
index.css, and App.tsx without requiring a running dev server.
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"


class TestIndexHtml:
    """Tests for frontend/index.html."""

    @pytest.fixture(autouse=True)
    def _load_html(self) -> None:
        """Load the index.html content."""
        self.path = FRONTEND_DIR / "index.html"
        assert self.path.exists(), f"{self.path} does not exist"
        self.content = self.path.read_text(encoding="utf-8")

    def test_has_doctype(self) -> None:
        """Verify HTML5 doctype declaration."""
        assert self.content.strip().startswith("<!doctype html>") or self.content.strip().startswith("<!DOCTYPE html>")

    def test_has_charset_meta(self) -> None:
        """Verify charset meta tag is present."""
        assert 'charset="UTF-8"' in self.content or "charset=\"utf-8\"" in self.content.lower()

    def test_has_viewport_meta(self) -> None:
        """Verify viewport meta tag is present."""
        assert 'name="viewport"' in self.content
        assert 'width=device-width' in self.content

    def test_has_description_meta(self) -> None:
        """Verify description meta tag is present."""
        assert 'name="description"' in self.content

    def test_has_og_tags(self) -> None:
        """Verify Open Graph meta tags are present."""
        assert 'property="og:type"' in self.content
        assert 'property="og:title"' in self.content
        assert 'property="og:description"' in self.content
        assert 'property="og:image"' in self.content
        assert 'property="og:site_name"' in self.content

    def test_has_theme_color(self) -> None:
        """Verify theme-color meta tag."""
        assert 'name="theme-color"' in self.content

    def test_has_canonical_link(self) -> None:
        """Verify canonical link tag."""
        assert 'rel="canonical"' in self.content

    def test_has_root_div(self) -> None:
        """Verify root div mount point."""
        assert 'id="root"' in self.content

    def test_has_noscript(self) -> None:
        """Verify noscript fallback."""
        assert '<noscript>' in self.content

    def test_has_module_script(self) -> None:
        """Verify the entry module script tag."""
        assert 'type="module"' in self.content
        assert 'src="/src/main.tsx"' in self.content

    def test_has_lang_attribute(self) -> None:
        """Verify html lang attribute."""
        assert 'lang="en"' in self.content

    def test_has_title(self) -> None:
        """Verify page title."""
        assert '<title>' in self.content
        assert '</title>' in self.content

    def test_has_favicon(self) -> None:
        """Verify favicon link."""
        assert 'favicon' in self.content


class TestMainTsx:
    """Tests for frontend/src/main.tsx."""

    @pytest.fixture(autouse=True)
    def _load_main(self) -> None:
        """Load the main.tsx content."""
        self.path = FRONTEND_DIR / "src" / "main.tsx"
        assert self.path.exists(), f"{self.path} does not exist"
        self.content = self.path.read_text(encoding="utf-8")

    def test_imports_react(self) -> None:
        """Verify React is imported."""
        assert "import React" in self.content

    def test_imports_react_dom(self) -> None:
        """Verify ReactDOM is imported."""
        assert "from 'react-dom/client'" in self.content

    def test_imports_browser_router(self) -> None:
        """Verify BrowserRouter is imported."""
        assert "BrowserRouter" in self.content
        assert "react-router-dom" in self.content

    def test_imports_helmet_provider(self) -> None:
        """Verify HelmetProvider is imported."""
        assert "HelmetProvider" in self.content
        assert "react-helmet-async" in self.content

    def test_imports_app(self) -> None:
        """Verify App component is imported."""
        assert "import App" in self.content

    def test_imports_index_css(self) -> None:
        """Verify global CSS is imported."""
        assert "./index.css" in self.content

    def test_uses_strict_mode(self) -> None:
        """Verify React.StrictMode is used."""
        assert "StrictMode" in self.content

    def test_uses_create_root(self) -> None:
        """Verify createRoot API is used."""
        assert "createRoot" in self.content

    def test_gets_root_element(self) -> None:
        """Verify getElementById('root') is called."""
        assert "getElementById('root')" in self.content

    def test_has_error_handling_for_missing_root(self) -> None:
        """Verify error is thrown if root element is missing."""
        assert "throw new Error" in self.content or "throw Error" in self.content


class TestIndexCss:
    """Tests for frontend/src/index.css."""

    @pytest.fixture(autouse=True)
    def _load_css(self) -> None:
        """Load the index.css content."""
        self.path = FRONTEND_DIR / "src" / "index.css"
        assert self.path.exists(), f"{self.path} does not exist"
        self.content = self.path.read_text(encoding="utf-8")

    def test_has_root_selector(self) -> None:
        """Verify :root selector exists for custom properties."""
        assert ":root" in self.content

    def test_has_color_properties(self) -> None:
        """Verify color custom properties are defined."""
        assert "--color-primary" in self.content
        assert "--color-neutral" in self.content

    def test_has_spacing_properties(self) -> None:
        """Verify spacing custom properties are defined."""
        assert "--spacing-" in self.content

    def test_has_typography_properties(self) -> None:
        """Verify typography custom properties are defined."""
        assert "--font-family-sans" in self.content
        assert "--font-size-" in self.content
        assert "--font-weight-" in self.content
        assert "--line-height-" in self.content

    def test_has_shadow_properties(self) -> None:
        """Verify shadow custom properties are defined."""
        assert "--shadow-sm" in self.content
        assert "--shadow-md" in self.content
        assert "--shadow-lg" in self.content

    def test_has_border_radius_properties(self) -> None:
        """Verify border-radius custom properties are defined."""
        assert "--radius-sm" in self.content
        assert "--radius-md" in self.content
        assert "--radius-lg" in self.content

    def test_has_box_sizing_reset(self) -> None:
        """Verify box-sizing reset is present."""
        assert "box-sizing: border-box" in self.content

    def test_has_margin_reset(self) -> None:
        """Verify margin reset is present."""
        assert "margin: 0" in self.content

    def test_has_body_styling(self) -> None:
        """Verify body font/color styling."""
        assert "font-family" in self.content
        assert "background-color" in self.content

    def test_has_gradient_properties(self) -> None:
        """Verify gradient custom properties for modern aesthetic."""
        assert "gradient" in self.content.lower()
        assert "linear-gradient" in self.content

    def test_has_transition_properties(self) -> None:
        """Verify transition custom properties."""
        assert "--transition-" in self.content

    def test_has_reduced_motion_media_query(self) -> None:
        """Verify prefers-reduced-motion media query."""
        assert "prefers-reduced-motion" in self.content

    def test_has_semantic_colors(self) -> None:
        """Verify semantic color tokens (success, warning, danger)."""
        assert "--color-success" in self.content
        assert "--color-warning" in self.content
        assert "--color-danger" in self.content

    def test_has_focus_styles(self) -> None:
        """Verify focus-visible styles."""
        assert "focus-visible" in self.content

    def test_has_selection_styles(self) -> None:
        """Verify ::selection styles."""
        assert "::selection" in self.content

    def test_has_list_reset(self) -> None:
        """Verify list-style reset."""
        assert "list-style: none" in self.content

    def test_has_image_reset(self) -> None:
        """Verify img display block reset."""
        assert "display: block" in self.content
        assert "max-width: 100%" in self.content

    def test_minimum_custom_properties_count(self) -> None:
        """Verify at least 50 CSS custom properties are defined."""
        prop_count = self.content.count("--")
        assert prop_count >= 50, f"Expected at least 50 custom properties, found ~{prop_count}"


class TestAppTsx:
    """Tests for frontend/src/App.tsx."""

    @pytest.fixture(autouse=True)
    def _load_app(self) -> None:
        """Load the App.tsx content."""
        self.path = FRONTEND_DIR / "src" / "App.tsx"
        assert self.path.exists(), f"{self.path} does not exist"
        self.content = self.path.read_text(encoding="utf-8")

    def test_imports_react(self) -> None:
        """Verify React is imported."""
        assert "react" in self.content.lower()

    def test_imports_helmet(self) -> None:
        """Verify Helmet is imported from react-helmet-async."""
        assert "Helmet" in self.content
        assert "react-helmet-async" in self.content

    def test_has_default_export(self) -> None:
        """Verify App is exported as default."""
        assert "export default" in self.content

    def test_uses_routes(self) -> None:
        """Verify React Router Routes component is used."""
        assert "Routes" in self.content
        assert "Route" in self.content

    def test_sets_meta_tags(self) -> None:
        """Verify default meta tags are set."""
        assert "<Helmet>" in self.content or "<Helmet " in self.content
        assert "title" in self.content.lower()


class TestPackageJson:
    """Tests for frontend/package.json."""

    @pytest.fixture(autouse=True)
    def _load_pkg(self) -> None:
        """Load the package.json content."""
        import json

        self.path = FRONTEND_DIR / "package.json"
        assert self.path.exists(), f"{self.path} does not exist"
        self.content = self.path.read_text(encoding="utf-8")
        self.data = json.loads(self.content)

    def test_has_react_dependency(self) -> None:
        """Verify react is listed as dependency."""
        assert "react" in self.data.get("dependencies", {})

    def test_has_react_dom_dependency(self) -> None:
        """Verify react-dom is listed as dependency."""
        assert "react-dom" in self.data.get("dependencies", {})

    def test_has_react_router_dom_dependency(self) -> None:
        """Verify react-router-dom is listed as dependency."""
        assert "react-router-dom" in self.data.get("dependencies", {})

    def test_has_react_helmet_async_dependency(self) -> None:
        """Verify react-helmet-async is listed as dependency."""
        assert "react-helmet-async" in self.data.get("dependencies", {})

    def test_has_vite_dev_dependency(self) -> None:
        """Verify vite is listed as dev dependency."""
        assert "vite" in self.data.get("devDependencies", {})

    def test_has_typescript_dev_dependency(self) -> None:
        """Verify typescript is listed as dev dependency."""
        assert "typescript" in self.data.get("devDependencies", {})

    def test_has_dev_script(self) -> None:
        """Verify dev script is defined."""
        assert "dev" in self.data.get("scripts", {})

    def test_has_build_script(self) -> None:
        """Verify build script is defined."""
        assert "build" in self.data.get("scripts", {})
