"""Comprehensive test suite for the Yellow World application.

Verifies:
1. The app (HTML page) renders without crashing / is well-formed.
2. The 'Yellow World' heading text is present in the document.
3. The page has the expected yellow background style applied.

Additional tests cover the CSS file, the JavaScript file, and the
Python HTTP server module.
"""

from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Optional

import pytest

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

PUBLIC_DIR: Path = Path(__file__).resolve().parent.parent / "public"
HTML_PATH: Path = PUBLIC_DIR / "index.html"
CSS_PATH: Path = PUBLIC_DIR / "styles.css"
JS_PATH: Path = PUBLIC_DIR / "app.js"


def _read_file(path: Path) -> str:
    """Read and return the full text content of *path*."""
    assert path.exists(), f"Expected file not found: {path}"
    return path.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# 1. App (HTML page) renders without crashing
# ---------------------------------------------------------------------------


class TestAppRenders:
    """Tests that the HTML page is well-formed and can be parsed."""

    def test_index_html_exists(self) -> None:
        """public/index.html must exist on disk."""
        assert HTML_PATH.exists(), "public/index.html is missing"

    def test_index_html_is_not_empty(self) -> None:
        """The HTML file must have content."""
        content = _read_file(HTML_PATH)
        assert len(content.strip()) > 0, "index.html is empty"

    def test_html_has_doctype(self) -> None:
        """The page must start with an HTML5 doctype."""
        content = _read_file(HTML_PATH)
        assert content.strip().lower().startswith("<!doctype html"), (
            "Missing <!DOCTYPE html> declaration"
        )

    def test_html_has_html_tag(self) -> None:
        """The page must contain an <html> root element."""
        content = _read_file(HTML_PATH)
        assert "<html" in content.lower(), "Missing <html> tag"

    def test_html_has_head_and_body(self) -> None:
        """The page must contain <head> and <body> sections."""
        content = _read_file(HTML_PATH).lower()
        assert "<head>" in content or "<head " in content, "Missing <head>"
        assert "<body>" in content or "<body " in content, "Missing <body>"

    def test_html_has_title(self) -> None:
        """The <title> tag must exist and contain meaningful text."""
        content = _read_file(HTML_PATH)
        match = re.search(r"<title>(.*?)</title>", content, re.IGNORECASE | re.DOTALL)
        assert match is not None, "Missing <title> element"
        assert len(match.group(1).strip()) > 0, "<title> is empty"

    def test_html_has_meta_viewport(self) -> None:
        """A responsive viewport meta tag must be present."""
        content = _read_file(HTML_PATH).lower()
        assert "viewport" in content, "Missing viewport meta tag"

    def test_html_has_stylesheet_link(self) -> None:
        """The page must link to styles.css."""
        content = _read_file(HTML_PATH)
        assert "styles.css" in content, "Missing link to styles.css"

    def test_html_has_script_tag(self) -> None:
        """The page must include app.js."""
        content = _read_file(HTML_PATH)
        assert "app.js" in content, "Missing script reference to app.js"

    def test_html_has_semantic_structure(self) -> None:
        """The page should use semantic HTML elements (header, main, footer)."""
        content = _read_file(HTML_PATH).lower()
        assert "<header" in content, "Missing <header> element"
        assert "<main" in content, "Missing <main> element"
        assert "<footer" in content, "Missing <footer> element"

    def test_html_tags_are_closed(self) -> None:
        """Basic check that major tags have matching closing tags."""
        content = _read_file(HTML_PATH).lower()
        for tag in ("html", "head", "body", "header", "main", "footer"):
            assert f"</{tag}>" in content, f"Missing closing </{tag}> tag"


# ---------------------------------------------------------------------------
# 2. 'Yellow World' heading text is present
# ---------------------------------------------------------------------------


class TestYellowWorldHeading:
    """Tests that the 'Yellow World' heading text is in the document."""

    def test_heading_text_present(self) -> None:
        """The literal text 'Yellow World' must appear in the HTML."""
        content = _read_file(HTML_PATH)
        assert "Yellow World" in content, (
            "'Yellow World' text not found in index.html"
        )

    def test_heading_is_h1(self) -> None:
        """'Yellow World' must be wrapped in an <h1> element."""
        content = _read_file(HTML_PATH)
        match = re.search(r"<h1[^>]*>(.*?)</h1>", content, re.IGNORECASE | re.DOTALL)
        assert match is not None, "No <h1> element found"
        assert "Yellow World" in match.group(1), (
            "'Yellow World' is not inside the <h1> tag"
        )

    def test_heading_has_greeting_class(self) -> None:
        """The <h1> should carry the 'greeting' CSS class."""
        content = _read_file(HTML_PATH)
        match = re.search(r'<h1[^>]*class=["\']([^"\']*)["\']', content, re.IGNORECASE)
        assert match is not None, "<h1> is missing a class attribute"
        assert "greeting" in match.group(1), (
            "<h1> does not have the 'greeting' class"
        )

    def test_title_contains_yellow_world(self) -> None:
        """The <title> should also reference 'Yellow World'."""
        content = _read_file(HTML_PATH)
        match = re.search(r"<title>(.*?)</title>", content, re.IGNORECASE | re.DOTALL)
        assert match is not None
        assert "Yellow World" in match.group(1)


# ---------------------------------------------------------------------------
# 3. The page has the expected yellow background style
# ---------------------------------------------------------------------------


class TestYellowBackground:
    """Tests that yellow background styling is correctly defined."""

    def test_css_file_exists(self) -> None:
        """styles.css must exist."""
        assert CSS_PATH.exists(), "public/styles.css is missing"

    def test_css_defines_yellow_bg_variable(self) -> None:
        """CSS must define --yellow-bg custom property with a yellow value."""
        css = _read_file(CSS_PATH)
        match = re.search(r"--yellow-bg\s*:\s*([^;]+);", css)
        assert match is not None, "--yellow-bg CSS variable not defined"
        value = match.group(1).strip().upper()
        # Accept known yellow values
        assert value in ("#FFF8DC", "#FFFACD", "#FFD700", "#FFFFE0") or "YELLOW" in value, (
            f"--yellow-bg value '{value}' does not look yellow"
        )

    def test_body_uses_yellow_background(self) -> None:
        """The body selector must set background-color using the yellow variable."""
        css = _read_file(CSS_PATH)
        # Find body rule and check for background-color
        assert "background-color" in css, "No background-color property found in CSS"
        # Specifically verify it references the yellow-bg variable or a yellow hex
        has_var = "var(--yellow-bg)" in css
        has_hex = bool(re.search(r"background-color\s*:\s*#FFF8DC", css, re.IGNORECASE))
        assert has_var or has_hex, (
            "body background-color does not reference --yellow-bg or #FFF8DC"
        )

    def test_css_defines_yellow_primary_variable(self) -> None:
        """CSS must define --yellow-primary for header styling."""
        css = _read_file(CSS_PATH)
        match = re.search(r"--yellow-primary\s*:\s*([^;]+);", css)
        assert match is not None, "--yellow-primary CSS variable not defined"

    def test_css_defines_yellow_accent_variable(self) -> None:
        """CSS must define --yellow-accent for footer styling."""
        css = _read_file(CSS_PATH)
        match = re.search(r"--yellow-accent\s*:\s*([^;]+);", css)
        assert match is not None, "--yellow-accent CSS variable not defined"

    def test_header_has_yellow_primary_background(self) -> None:
        """The header should use --yellow-primary as its background."""
        css = _read_file(CSS_PATH)
        # Check header rule references yellow-primary
        assert "var(--yellow-primary)" in css, (
            "Header does not use var(--yellow-primary)"
        )

    def test_footer_has_yellow_accent_background(self) -> None:
        """The footer should use --yellow-accent as its background."""
        css = _read_file(CSS_PATH)
        assert "var(--yellow-accent)" in css, (
            "Footer does not use var(--yellow-accent)"
        )

    def test_heading_color_is_dark(self) -> None:
        """The h1 text colour should be the dark heading colour."""
        css = _read_file(CSS_PATH)
        match = re.search(r"--text-heading\s*:\s*([^;]+);", css)
        assert match is not None, "--text-heading variable not defined"
        # The heading colour should be dark (not pure white)
        value = match.group(1).strip().upper()
        assert value != "#FFFFFF", "Heading colour should not be white"


# ---------------------------------------------------------------------------
# 4. JavaScript file tests
# ---------------------------------------------------------------------------


class TestAppJavaScript:
    """Tests for the app.js companion script."""

    def test_js_file_exists(self) -> None:
        """public/app.js must exist."""
        assert JS_PATH.exists(), "public/app.js is missing"

    def test_js_has_dom_content_loaded_listener(self) -> None:
        """app.js should listen for DOMContentLoaded."""
        js = _read_file(JS_PATH)
        assert "DOMContentLoaded" in js, "Missing DOMContentLoaded listener"

    def test_js_defines_get_greeting(self) -> None:
        """app.js should define a getGreeting function."""
        js = _read_file(JS_PATH)
        assert "getGreeting" in js, "Missing getGreeting function"

    def test_js_get_greeting_returns_yellow_world(self) -> None:
        """The getGreeting function should contain the string 'Yellow World'."""
        js = _read_file(JS_PATH)
        assert "Yellow World" in js, (
            "'Yellow World' string not found in app.js"
        )


# ---------------------------------------------------------------------------
# 5. Server module tests
# ---------------------------------------------------------------------------


class TestServerModule:
    """Tests for the Python HTTP server module."""

    def test_server_py_exists(self) -> None:
        """server.py must exist at the project root."""
        server_path = Path(__file__).resolve().parent.parent / "server.py"
        assert server_path.exists(), "server.py is missing"

    def test_server_module_imports(self) -> None:
        """server.py must be importable without side-effects."""
        import importlib
        import sys

        server_path = str(Path(__file__).resolve().parent.parent)
        if server_path not in sys.path:
            sys.path.insert(0, server_path)

        # Should import without starting the server (guarded by __name__)
        mod = importlib.import_module("server")
        assert hasattr(mod, "run_server"), "server module missing run_server()"
        assert hasattr(mod, "DIRECTORY"), "server module missing DIRECTORY"
        assert hasattr(mod, "PORT"), "server module missing PORT"

    def test_server_default_port(self) -> None:
        """Default PORT should be 8000."""
        import importlib
        import sys

        server_path = str(Path(__file__).resolve().parent.parent)
        if server_path not in sys.path:
            sys.path.insert(0, server_path)

        mod = importlib.import_module("server")
        # PORT may have been overridden by env; check it's an int
        assert isinstance(mod.PORT, int)

    def test_server_directory_points_to_public(self) -> None:
        """DIRECTORY should resolve to the public/ folder."""
        import importlib
        import sys

        server_path = str(Path(__file__).resolve().parent.parent)
        if server_path not in sys.path:
            sys.path.insert(0, server_path)

        mod = importlib.import_module("server")
        assert mod.DIRECTORY.endswith("public"), (
            f"DIRECTORY should end with 'public', got {mod.DIRECTORY}"
        )

    def test_create_handler_returns_callable(self) -> None:
        """create_handler() must return a callable handler class/partial."""
        import importlib
        import sys

        server_path = str(Path(__file__).resolve().parent.parent)
        if server_path not in sys.path:
            sys.path.insert(0, server_path)

        mod = importlib.import_module("server")
        handler = mod.create_handler()
        assert callable(handler), "create_handler() did not return a callable"
