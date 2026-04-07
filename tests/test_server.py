"""Automated tests for the Hello World static server.

Tests verify that:
- The server starts and responds on the configured port.
- The response contains the expected HTML content.
- The background colour is set to #ffffff.
- The page title is 'Hello World'.
- The visible text 'Hello World' is present.
"""

from __future__ import annotations

import os
import socket
import threading
import time
import unittest
import urllib.request
from functools import partial
from http.server import HTTPServer, SimpleHTTPRequestHandler
from typing import Optional


def _find_free_port() -> int:
    """Return an available TCP port on localhost."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        return s.getsockname()[1]


class TestHelloWorldServer(unittest.TestCase):
    """Integration tests that spin up the static file server and issue HTTP requests."""

    server: Optional[HTTPServer] = None
    thread: Optional[threading.Thread] = None
    port: int = 0

    @classmethod
    def setUpClass(cls) -> None:
        """Start an HTTP server in a background thread before any tests run."""
        cls.port = _find_free_port()

        # Serve from the project root where index.html lives
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        handler = partial(SimpleHTTPRequestHandler, directory=project_root)

        cls.server = HTTPServer(("127.0.0.1", cls.port), handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

        # Give the server a moment to start accepting connections
        time.sleep(0.3)

    @classmethod
    def tearDownClass(cls) -> None:
        """Shut down the HTTP server after all tests complete."""
        if cls.server is not None:
            cls.server.shutdown()

    def _get(self, path: str = "/") -> str:
        """Perform an HTTP GET and return the decoded response body.

        Args:
            path: URL path to request.  Defaults to ``"/"``.

        Returns:
            The response body as a UTF-8 string.
        """
        url = f"http://127.0.0.1:{self.port}{path}"
        with urllib.request.urlopen(url, timeout=5) as resp:
            return resp.read().decode("utf-8")

    # ------------------------------------------------------------------
    # Tests
    # ------------------------------------------------------------------

    def test_server_responds_with_200(self) -> None:
        """The server should respond with HTTP 200 for the root path."""
        url = f"http://127.0.0.1:{self.port}/"
        with urllib.request.urlopen(url, timeout=5) as resp:
            self.assertEqual(resp.status, 200)

    def test_response_contains_hello_world_heading(self) -> None:
        """The page body must contain an <h1> with 'Hello World'."""
        body = self._get("/")
        self.assertIn("<h1>Hello World</h1>", body)

    def test_page_title_is_hello_world(self) -> None:
        """The <title> element must be 'Hello World'."""
        body = self._get("/")
        self.assertIn("<title>Hello World</title>", body)

    def test_background_color_is_white(self) -> None:
        """The CSS must set background-color to #ffffff."""
        body = self._get("/")
        self.assertIn("background-color: #ffffff", body)

    def test_html5_doctype(self) -> None:
        """The page must start with an HTML5 doctype declaration."""
        body = self._get("/")
        self.assertTrue(body.strip().startswith("<!DOCTYPE html>"))

    def test_flexbox_centering(self) -> None:
        """The CSS must use flexbox for centering content."""
        body = self._get("/")
        self.assertIn("display: flex", body)
        self.assertIn("justify-content: center", body)
        self.assertIn("align-items: center", body)

    def test_viewport_meta_tag(self) -> None:
        """The page should include a viewport meta tag for responsiveness."""
        body = self._get("/")
        self.assertIn('name="viewport"', body)

    def test_content_type_is_html(self) -> None:
        """The Content-Type header should indicate HTML."""
        url = f"http://127.0.0.1:{self.port}/"
        with urllib.request.urlopen(url, timeout=5) as resp:
            content_type = resp.headers.get("Content-Type", "")
            self.assertIn("text/html", content_type)


class TestIndexHtmlFile(unittest.TestCase):
    """Unit tests that verify index.html exists and has correct structure."""

    def setUp(self) -> None:
        """Load index.html content from the project root."""
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.index_path = os.path.join(project_root, "index.html")

    def test_index_html_exists(self) -> None:
        """index.html must exist in the project root."""
        self.assertTrue(
            os.path.isfile(self.index_path),
            f"index.html not found at {self.index_path}",
        )

    def test_index_html_is_not_empty(self) -> None:
        """index.html must not be an empty file."""
        size = os.path.getsize(self.index_path)
        self.assertGreater(size, 0, "index.html is empty")

    def test_index_html_contains_lang_attribute(self) -> None:
        """The <html> tag should have a lang attribute."""
        with open(self.index_path, encoding="utf-8") as f:
            content = f.read()
        self.assertIn('lang="en"', content)


class TestServerModule(unittest.TestCase):
    """Unit tests for the server.py module."""

    def test_server_module_importable(self) -> None:
        """server.py must be importable without starting a server."""
        import importlib
        import sys

        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if project_root not in sys.path:
            sys.path.insert(0, project_root)

        # Importing should not block because serve_forever is behind __main__ guard
        module = importlib.import_module("server")
        self.assertTrue(hasattr(module, "run_server"))

    def test_run_server_is_callable(self) -> None:
        """run_server must be a callable function."""
        import importlib
        import sys

        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if project_root not in sys.path:
            sys.path.insert(0, project_root)

        module = importlib.import_module("server")
        self.assertTrue(callable(module.run_server))


if __name__ == "__main__":
    unittest.main()
