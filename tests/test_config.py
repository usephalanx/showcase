"""Validation tests for frontend configuration files.

These tests verify that the project configuration files are correctly
structured and contain the expected design tokens and settings.
"""

import json
import os
from pathlib import Path

import pytest

ROOT_DIR = Path(__file__).resolve().parent.parent


def _read_file(relative_path: str) -> str:
    """Read a file relative to the project root and return its content."""
    file_path = ROOT_DIR / relative_path
    assert file_path.exists(), f"File not found: {relative_path}"
    return file_path.read_text(encoding="utf-8")


class TestPackageJson:
    """Tests for package.json structure and dependencies."""

    @pytest.fixture()
    def pkg(self) -> dict:
        """Parse and return package.json as a dictionary."""
        content = _read_file("package.json")
        return json.loads(content)

    def test_project_name(self, pkg: dict) -> None:
        """Project should be named 'maddie-realestate'."""
        assert pkg["name"] == "maddie-realestate"

    def test_has_react_dependency(self, pkg: dict) -> None:
        """React should be listed in dependencies."""
        assert "react" in pkg["dependencies"]
        assert "react-dom" in pkg["dependencies"]

    def test_has_dev_dependencies(self, pkg: dict) -> None:
        """Key dev dependencies should be present."""
        dev_deps = pkg["devDependencies"]
        assert "vite" in dev_deps
        assert "tailwindcss" in dev_deps
        assert "postcss" in dev_deps
        assert "autoprefixer" in dev_deps
        assert "@vitejs/plugin-react" in dev_deps
        assert "typescript" in dev_deps

    def test_has_scripts(self, pkg: dict) -> None:
        """Essential npm scripts should be defined."""
        scripts = pkg["scripts"]
        assert "dev" in scripts
        assert "build" in scripts
        assert "preview" in scripts

    def test_private_flag(self, pkg: dict) -> None:
        """Package should be marked as private."""
        assert pkg["private"] is True


class TestIndexHtml:
    """Tests for index.html content and meta tags."""

    @pytest.fixture()
    def html(self) -> str:
        """Read and return index.html content."""
        return _read_file("index.html")

    def test_has_google_fonts_preconnect(self, html: str) -> None:
        """Should have preconnect links for Google Fonts."""
        assert "fonts.googleapis.com" in html
        assert "fonts.gstatic.com" in html

    def test_has_playfair_display_font(self, html: str) -> None:
        """Should load Playfair Display from Google Fonts."""
        assert "Playfair+Display" in html or "Playfair Display" in html

    def test_has_inter_font(self, html: str) -> None:
        """Should load Inter from Google Fonts."""
        assert "Inter" in html

    def test_has_smooth_scroll(self, html: str) -> None:
        """Should have smooth scroll behavior on html element."""
        assert "scroll-behavior" in html
        assert "smooth" in html

    def test_has_viewport_meta(self, html: str) -> None:
        """Should have viewport meta tag."""
        assert 'name="viewport"' in html

    def test_has_description_meta(self, html: str) -> None:
        """Should have a description meta tag."""
        assert 'name="description"' in html

    def test_has_root_div(self, html: str) -> None:
        """Should have a root mount point div."""
        assert 'id="root"' in html

    def test_has_main_tsx_script(self, html: str) -> None:
        """Should reference main.tsx as the entry module."""
        assert "src/main.tsx" in html


class TestTailwindConfig:
    """Tests for tailwind.config.js design tokens."""

    @pytest.fixture()
    def config(self) -> str:
        """Read and return tailwind.config.js content."""
        return _read_file("tailwind.config.js")

    def test_has_cream_color(self, config: str) -> None:
        """Should define cream color token."""
        assert "#FDF8F0" in config

    def test_has_gold_color(self, config: str) -> None:
        """Should define gold color token."""
        assert "#C9A84C" in config

    def test_has_warm_white_color(self, config: str) -> None:
        """Should define warm-white color token."""
        assert "#FAF7F2" in config

    def test_has_slate_color(self, config: str) -> None:
        """Should define slate color with value #334155."""
        assert "#334155" in config

    def test_has_playfair_font_family(self, config: str) -> None:
        """Should configure Playfair Display font family."""
        assert "playfair" in config
        assert "Playfair Display" in config

    def test_has_inter_font_family(self, config: str) -> None:
        """Should configure Inter font family."""
        assert "inter" in config.lower()
        assert "Inter" in config

    def test_has_content_paths(self, config: str) -> None:
        """Should configure content paths for Tailwind purge."""
        assert "./index.html" in config
        assert "./src/**/*.{js,ts,jsx,tsx}" in config

    def test_has_animations(self, config: str) -> None:
        """Should define custom animations."""
        assert "fade-in" in config
        assert "slide-up" in config

    def test_has_custom_spacing(self, config: str) -> None:
        """Should extend spacing with custom values."""
        assert "4.5rem" in config


class TestPostcssConfig:
    """Tests for postcss.config.js plugins."""

    @pytest.fixture()
    def config(self) -> str:
        """Read and return postcss.config.js content."""
        return _read_file("postcss.config.js")

    def test_has_tailwindcss_plugin(self, config: str) -> None:
        """Should include tailwindcss plugin."""
        assert "tailwindcss" in config

    def test_has_autoprefixer_plugin(self, config: str) -> None:
        """Should include autoprefixer plugin."""
        assert "autoprefixer" in config


class TestViteConfig:
    """Tests for vite.config.js settings."""

    @pytest.fixture()
    def config(self) -> str:
        """Read and return vite.config.js content."""
        return _read_file("vite.config.js")

    def test_has_react_plugin(self, config: str) -> None:
        """Should use the React Vite plugin."""
        assert "@vitejs/plugin-react" in config
        assert "react()" in config

    def test_has_path_alias(self, config: str) -> None:
        """Should define '@' path alias pointing to './src'."""
        assert "'@'" in config or '"@"' in config
        assert "./src" in config

    def test_has_port_3000(self, config: str) -> None:
        """Should configure dev server on port 3000."""
        assert "3000" in config


class TestTypeScriptConfig:
    """Tests for tsconfig.json settings."""

    @pytest.fixture()
    def tsconfig(self) -> dict:
        """Parse and return tsconfig.json as a dictionary."""
        content = _read_file("tsconfig.json")
        return json.loads(content)

    def test_has_react_jsx(self, tsconfig: dict) -> None:
        """Should use react-jsx for JSX transform."""
        assert tsconfig["compilerOptions"]["jsx"] == "react-jsx"

    def test_has_strict_mode(self, tsconfig: dict) -> None:
        """Should enable strict mode."""
        assert tsconfig["compilerOptions"]["strict"] is True

    def test_has_path_alias(self, tsconfig: dict) -> None:
        """Should define '@/*' path alias."""
        paths = tsconfig["compilerOptions"]["paths"]
        assert "@/*" in paths
        assert "./src/*" in paths["@/*"]

    def test_includes_src(self, tsconfig: dict) -> None:
        """Should include the src directory."""
        assert "src" in tsconfig["include"]


class TestSourceFiles:
    """Tests to verify essential source files exist and have correct content."""

    def test_index_css_has_tailwind_directives(self) -> None:
        """src/index.css should include Tailwind directives."""
        css = _read_file("src/index.css")
        assert "@tailwind base" in css
        assert "@tailwind components" in css
        assert "@tailwind utilities" in css

    def test_index_css_has_base_typography(self) -> None:
        """src/index.css should set base font families."""
        css = _read_file("src/index.css")
        assert "font-inter" in css
        assert "font-playfair" in css

    def test_main_tsx_exists(self) -> None:
        """src/main.tsx should exist."""
        assert (ROOT_DIR / "src" / "main.tsx").exists()

    def test_app_tsx_exists(self) -> None:
        """src/App.tsx should exist."""
        assert (ROOT_DIR / "src" / "App.tsx").exists()

    def test_vite_env_dts_exists(self) -> None:
        """src/vite-env.d.ts should exist."""
        assert (ROOT_DIR / "src" / "vite-env.d.ts").exists()

    def test_types_index_exists(self) -> None:
        """src/types/index.ts should exist."""
        assert (ROOT_DIR / "src" / "types" / "index.ts").exists()

    def test_scroll_utility_exists(self) -> None:
        """src/utils/scrollTo.ts should exist."""
        assert (ROOT_DIR / "src" / "utils" / "scrollTo.ts").exists()

    def test_smooth_scroll_hook_exists(self) -> None:
        """src/hooks/useSmoothScroll.ts should exist."""
        assert (ROOT_DIR / "src" / "hooks" / "useSmoothScroll.ts").exists()

    def test_app_has_all_sections(self) -> None:
        """App.tsx should contain all major section IDs."""
        app = _read_file("src/App.tsx")
        for section_id in ["hero", "about", "sales", "contact"]:
            assert f'id="{section_id}"' in app, f"Missing section: {section_id}"
