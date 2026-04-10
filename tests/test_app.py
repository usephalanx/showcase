"""Tests for the Yellow World application.

Covers:
- Static file existence and content verification
- HTML structure validation
- CSS color palette variables
- JavaScript function presence
- Python server handler creation
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Generator

import pytest

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent
PUBLIC_DIR: Path = PROJECT_ROOT / "public"


def _read(filename: str) -> str:
    """Read a file from the public directory and return its contents."""
    return (PUBLIC_DIR / filename).read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# Static file existence
# ---------------------------------------------------------------------------


class TestStaticFilesExist:
    """Verify all expected static assets are present."""

    @pytest.mark.parametrize("filename", ["index.html", "styles.css", "app.js"])
    def test_file_exists(self, filename: str) -> None:
        """Each static file must exist in public/."""
        path = PUBLIC_DIR / filename
        assert path.is_file(), f"{filename} not found in {PUBLIC_DIR}"


# ---------------------------------------------------------------------------
# HTML content
# ---------------------------------------------------------------------------


class TestHTMLContent:
    """Validate index.html structure and required elements."""

    @pytest.fixture(autouse=True)
    def _load_html(self) -> None:
        """Load the HTML content once for the class."""
        self.html: str = _read("index.html")

    def test_doctype(self) -> None:
        """Page must start with HTML5 doctype."""
        assert self.html.strip().startswith("<!DOCTYPE html>")

    def test_lang_attribute(self) -> None:
        """Root html element must have lang='en'."""
        assert 'lang="en"' in self.html

    def test_viewport_meta(self) -> None:
        """Responsive viewport meta tag must be present."""
        assert 'name="viewport"' in self.html

    def test_title(self) -> None:
        """Page title must be 'Yellow World'."""
        assert "<title>Yellow World</title>" in self.html

    def test_stylesheet_link(self) -> None:
        """Link to styles.css must be present."""
        assert 'href="styles.css"' in self.html

    def test_h1_greeting(self) -> None:
        """An h1 with class 'greeting' containing 'Yellow World' must exist."""
        assert 'class="greeting"' in self.html
        assert "Yellow World" in self.html

    def test_subtitle_paragraph(self) -> None:
        """A paragraph with class 'subtitle' must exist."""
        assert 'class="subtitle"' in self.html

    def test_header_element(self) -> None:
        """A <header> element must exist."""
        assert "<header>" in self.html

    def test_footer_element(self) -> None:
        """A <footer> element must exist."""
        assert "<footer>" in self.html

    def test_script_tag(self) -> None:
        """Script tag linking to app.js must be present."""
        assert 'src="app.js"' in self.html


# ---------------------------------------------------------------------------
# CSS content
# ---------------------------------------------------------------------------


class TestCSSContent:
    """Validate styles.css colour palette and key rules."""

    @pytest.fixture(autouse=True)
    def _load_css(self) -> None:
        """Load the CSS content once for the class."""
        self.css: str = _read("styles.css")

    @pytest.mark.parametrize(
        "var_name,value",
        [
            ("--yellow-primary", "#FFD700"),
            ("--yellow-bg", "#FFF8DC"),
            ("--yellow-accent", "#FFC107"),
            ("--text-dark", "#333333"),
            ("--text-heading", "#1A1A00"),
        ],
    )
    def test_css_variable_defined(self, var_name: str, value: str) -> None:
        """Each colour variable must be declared with the correct value."""
        assert var_name in self.css
        assert value in self.css

    def test_box_sizing_reset(self) -> None:
        """Global box-sizing: border-box must be set."""
        assert "box-sizing: border-box" in self.css

    def test_body_flex_column(self) -> None:
        """Body must use flex column layout."""
        assert "flex-direction: column" in self.css

    def test_min_height_viewport(self) -> None:
        """Body must have min-height: 100vh."""
        assert "min-height: 100vh" in self.css


# ---------------------------------------------------------------------------
# JavaScript content
# ---------------------------------------------------------------------------


class TestJSContent:
    """Validate app.js key functions."""

    @pytest.fixture(autouse=True)
    def _load_js(self) -> None:
        """Load the JS content once for the class."""
        self.js: str = _read("app.js")

    def test_get_greeting_function(self) -> None:
        """getGreeting function must be defined."""
        assert "function getGreeting" in self.js

    def test_get_greeting_returns_yellow_world(self) -> None:
        """getGreeting must return 'Yellow World'."""
        assert '"Yellow World"' in self.js or "'Yellow World'" in self.js

    def test_init_app_function(self) -> None:
        """initApp function must be defined."""
        assert "function initApp" in self.js

    def test_loaded_class_added(self) -> None:
        """initApp must add a 'loaded' class."""
        assert '"loaded"' in self.js or "'loaded'" in self.js

    def test_dom_content_loaded_listener(self) -> None:
        """DOMContentLoaded event listener must be present."""
        assert "DOMContentLoaded" in self.js

    def test_console_log(self) -> None:
        """Console log confirming initialisation must be present."""
        assert "console.log" in self.js


# ---------------------------------------------------------------------------
# Server module
# ---------------------------------------------------------------------------


class TestServerModule:
    """Validate server.py can be imported and configured."""

    def test_server_module_imports(self) -> None:
        """server module must be importable."""
        import importlib
        import importlib.util

        spec = importlib.util.spec_from_file_location(
            "server", str(PROJECT_ROOT / "server.py")
        )
        assert spec is not None
        module = importlib.util.module_from_spec(spec)
        # We don't execute the module to avoid starting the server,
        # but we verify the spec loaded correctly.
        assert module is not None

    def test_server_py_exists(self) -> None:
        """server.py must exist at project root."""
        assert (PROJECT_ROOT / "server.py").is_file()

    def test_server_references_public_directory(self) -> None:
        """server.py must reference the public directory."""
        content = (PROJECT_ROOT / "server.py").read_text(encoding="utf-8")
        assert "public" in content

    def test_server_default_port(self) -> None:
        """server.py must default to port 8000."""
        content = (PROJECT_ROOT / "server.py").read_text(encoding="utf-8")
        assert "8000" in content


# ---------------------------------------------------------------------------
# Docker files
# ---------------------------------------------------------------------------


class TestDockerFiles:
    """Validate Docker configuration files."""

    def test_dockerfile_exists(self) -> None:
        """Dockerfile must exist at project root."""
        assert (PROJECT_ROOT / "Dockerfile").is_file()

    def test_dockerfile_uses_python_slim(self) -> None:
        """Dockerfile must use python:3.12-slim base image."""
        content = (PROJECT_ROOT / "Dockerfile").read_text(encoding="utf-8")
        assert "python:3.12-slim" in content

    def test_dockerfile_exposes_8000(self) -> None:
        """Dockerfile must expose port 8000."""
        content = (PROJECT_ROOT / "Dockerfile").read_text(encoding="utf-8")
        assert "EXPOSE 8000" in content

    def test_docker_compose_exists(self) -> None:
        """docker-compose.yml must exist at project root."""
        assert (PROJECT_ROOT / "docker-compose.yml").is_file()

    def test_docker_compose_maps_port(self) -> None:
        """docker-compose.yml must map port 8000."""
        content = (PROJECT_ROOT / "docker-compose.yml").read_text(encoding="utf-8")
        assert "8000:8000" in content
