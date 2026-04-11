"""Tests for frontend CSS styling files.

Verifies that all required CSS and component files exist with the
expected styling rules for a centered, modern look.
"""

from __future__ import annotations

import os
from pathlib import Path

# Resolve the project root (parent of tests/)
PROJECT_ROOT = Path(__file__).resolve().parent.parent


def _read_file(relative_path: str) -> str:
    """Read a project file and return its content as a string."""
    full_path = PROJECT_ROOT / relative_path
    assert full_path.exists(), f"File not found: {relative_path}"
    return full_path.read_text(encoding="utf-8")


class TestIndexCSS:
    """Tests for the global index.css file."""

    def test_file_exists(self) -> None:
        """index.css must exist in src/."""
        path = PROJECT_ROOT / "src" / "index.css"
        assert path.exists()

    def test_white_background(self) -> None:
        """Global styles should set a white background."""
        content = _read_file("src/index.css")
        assert "#ffffff" in content or "#fff" in content or "white" in content

    def test_box_sizing_reset(self) -> None:
        """Global styles should include box-sizing: border-box reset."""
        content = _read_file("src/index.css")
        assert "box-sizing" in content

    def test_margin_reset(self) -> None:
        """Global styles should reset margins."""
        content = _read_file("src/index.css")
        assert "margin: 0" in content or "margin:0" in content


class TestAppModuleCSS:
    """Tests for the App-level CSS module."""

    def test_file_exists(self) -> None:
        """App.module.css must exist in src/."""
        path = PROJECT_ROOT / "src" / "App.module.css"
        assert path.exists()

    def test_flexbox_centering(self) -> None:
        """App container should use flexbox for centering."""
        content = _read_file("src/App.module.css")
        assert "display: flex" in content or "display:flex" in content
        assert "justify-content: center" in content or "justify-content:center" in content
        assert "align-items: center" in content or "align-items:center" in content

    def test_min_height_viewport(self) -> None:
        """App container should span at least full viewport height."""
        content = _read_file("src/App.module.css")
        assert "min-height: 100vh" in content or "min-height:100vh" in content

    def test_white_background(self) -> None:
        """App container should have a white background."""
        content = _read_file("src/App.module.css")
        assert "#ffffff" in content or "#fff" in content or "white" in content


class TestAppCSS:
    """Tests for the legacy App.css file."""

    def test_file_exists(self) -> None:
        """App.css must exist in src/."""
        path = PROJECT_ROOT / "src" / "App.css"
        assert path.exists()


class TestHelloWorldModuleCSS:
    """Tests for the HelloWorld component's CSS module."""

    def test_file_exists(self) -> None:
        """HelloWorld.module.css must exist in src/components/."""
        path = PROJECT_ROOT / "src" / "components" / "HelloWorld.module.css"
        assert path.exists()

    def test_text_alignment(self) -> None:
        """Heading should be centered."""
        content = _read_file("src/components/HelloWorld.module.css")
        assert "text-align: center" in content or "text-align:center" in content

    def test_font_size(self) -> None:
        """Heading should have a substantial font size."""
        content = _read_file("src/components/HelloWorld.module.css")
        assert "font-size" in content

    def test_font_weight(self) -> None:
        """Heading should be bold."""
        content = _read_file("src/components/HelloWorld.module.css")
        assert "font-weight" in content

    def test_color(self) -> None:
        """Heading should have a defined color."""
        content = _read_file("src/components/HelloWorld.module.css")
        assert "color" in content


class TestComponentFiles:
    """Tests that required component source files exist."""

    def test_app_tsx_exists(self) -> None:
        """App.tsx must exist."""
        assert (PROJECT_ROOT / "src" / "App.tsx").exists()

    def test_helloworld_tsx_exists(self) -> None:
        """HelloWorld.tsx must exist."""
        assert (PROJECT_ROOT / "src" / "components" / "HelloWorld.tsx").exists()

    def test_main_tsx_exists(self) -> None:
        """main.tsx must exist."""
        assert (PROJECT_ROOT / "src" / "main.tsx").exists()

    def test_index_html_exists(self) -> None:
        """index.html must exist at project root."""
        assert (PROJECT_ROOT / "index.html").exists()


class TestAppTSXContent:
    """Tests for App.tsx component content."""

    def test_imports_css_module(self) -> None:
        """App.tsx should import its CSS module."""
        content = _read_file("src/App.tsx")
        assert "App.module.css" in content

    def test_imports_helloworld(self) -> None:
        """App.tsx should import the HelloWorld component."""
        content = _read_file("src/App.tsx")
        assert "HelloWorld" in content

    def test_uses_container_class(self) -> None:
        """App.tsx should use the container class from the CSS module."""
        content = _read_file("src/App.tsx")
        assert "styles.container" in content


class TestHelloWorldTSXContent:
    """Tests for HelloWorld.tsx component content."""

    def test_imports_css_module(self) -> None:
        """HelloWorld.tsx should import its CSS module."""
        content = _read_file("src/components/HelloWorld.tsx")
        assert "HelloWorld.module.css" in content

    def test_renders_h1(self) -> None:
        """HelloWorld.tsx should render an h1 element."""
        content = _read_file("src/components/HelloWorld.tsx")
        assert "<h1" in content

    def test_hello_world_text(self) -> None:
        """HelloWorld.tsx should contain 'Hello World' text."""
        content = _read_file("src/components/HelloWorld.tsx")
        assert "Hello World" in content

    def test_uses_heading_class(self) -> None:
        """HelloWorld.tsx should use the heading class from CSS module."""
        content = _read_file("src/components/HelloWorld.tsx")
        assert "styles.heading" in content
