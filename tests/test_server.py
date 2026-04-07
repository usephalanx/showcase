"""Automated tests for server.py and index.html.

Starts the HTTP server in a background thread, verifies that it serves
the expected content, and tears it down after the test suite completes.
"""

from __future__ import annotations

import functools
import http.server
import os
import socketserver
import threading
import time
import unittest
import urllib.error
import urllib.request
from typing import Optional


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _find_project_root() -> str:
    """Return the absolute path to the project root directory.

    Walks upward from this file's directory until it finds ``index.html``
    and ``server.py`` side-by-side.
    """
    current = os.path.dirname(os.path.abspath(__file__))
    # Go up one level (from tests/ to project root)
    root = os.path.dirname(current)
    if os.path.isfile(os.path.join(root, "index.html")) and os.path.isfile(
        os.path.join(root, "server.py")
    ):
        return root
    # Fallback: current working directory
    return os.getcwd()


class _ServerThread:
    """Context manager that runs an HTTP server in a daemon thread."""

    def __init__(self, port: int, directory: str) -> None:
        """Initialise with the desired port and directory to serve."""
        self.port = port
        self.directory = directory
        self.httpd: Optional[socketserver.TCPServer] = None
        self.thread: Optional[threading.Thread] = None

    def __enter__(self) -> "_ServerThread":
        """Start the server in a background daemon thread."""
        handler = functools.partial(
            http.server.SimpleHTTPRequestHandler,
            directory=self.directory,
        )
        socketserver.TCPServer.allow_reuse_address = True
        self.httpd = socketserver.TCPServer(("127.0.0.1", self.port), handler)
        self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        self.thread.start()
        # Give the server a moment to bind
        time.sleep(0.3)
        return self

    def __exit__(self, *exc_info: object) -> None:
        """Shut down the server and wait for the thread to finish."""
        if self.httpd is not None:
            self.httpd.shutdown()
        if self.thread is not None:
            self.thread.join(timeout=5)


# ---------------------------------------------------------------------------
# Test cases
# ---------------------------------------------------------------------------

# Pick a port unlikely to collide with a running dev server
TEST_PORT: int = 18_765
PROJECT_ROOT: str = _find_project_root()


class TestServerServing(unittest.TestCase):
    """Verify that the HTTP server correctly serves project files."""

    server: _ServerThread

    @classmethod
    def setUpClass(cls) -> None:
        """Start the server once for all tests in this class."""
        cls.server = _ServerThread(port=TEST_PORT, directory=PROJECT_ROOT)
        cls.server.__enter__()

    @classmethod
    def tearDownClass(cls) -> None:
        """Shut down the server after all tests complete."""
        cls.server.__exit__(None, None, None)

    # -- Tests --------------------------------------------------------------

    def _get(self, path: str = "/") -> http.client.HTTPResponse:
        """Perform a GET request against the test server."""
        url = f"http://127.0.0.1:{TEST_PORT}{path}"
        return urllib.request.urlopen(url, timeout=5)

    def test_root_returns_200(self) -> None:
        """GET / should return HTTP 200."""
        response = self._get("/")
        self.assertEqual(response.status, 200)

    def test_root_serves_html(self) -> None:
        """GET / should return content containing 'Hello World'."""
        response = self._get("/")
        body = response.read().decode("utf-8")
        self.assertIn("Hello World", body)

    def test_root_content_type_is_html(self) -> None:
        """GET / should have a text/html Content-Type."""
        response = self._get("/")
        content_type = response.headers.get("Content-Type", "")
        self.assertIn("text/html", content_type)

    def test_index_html_direct(self) -> None:
        """GET /index.html should return HTTP 200 with Hello World."""
        response = self._get("/index.html")
        self.assertEqual(response.status, 200)
        body = response.read().decode("utf-8")
        self.assertIn("Hello World", body)

    def test_nonexistent_path_returns_404(self) -> None:
        """GET /nonexistent should return HTTP 404."""
        url = f"http://127.0.0.1:{TEST_PORT}/nonexistent_page.html"
        with self.assertRaises(urllib.error.HTTPError) as ctx:
            urllib.request.urlopen(url, timeout=5)
        self.assertEqual(ctx.exception.code, 404)


class TestIndexHtmlContent(unittest.TestCase):
    """Validate the static index.html file on disk."""

    html: str

    @classmethod
    def setUpClass(cls) -> None:
        """Read index.html into memory once."""
        path = os.path.join(PROJECT_ROOT, "index.html")
        with open(path, encoding="utf-8") as fh:
            cls.html = fh.read()

    def test_has_doctype(self) -> None:
        """index.html should start with a DOCTYPE declaration."""
        self.assertTrue(self.html.strip().startswith("<!DOCTYPE html>"))

    def test_has_title(self) -> None:
        """index.html should contain a <title> tag with 'Hello World'."""
        self.assertIn("<title>Hello World</title>", self.html)

    def test_has_h1(self) -> None:
        """index.html should contain an <h1> with 'Hello World'."""
        self.assertIn("<h1>Hello World</h1>", self.html)

    def test_has_viewport_meta(self) -> None:
        """index.html should contain a viewport meta tag."""
        self.assertIn('name="viewport"', self.html)

    def test_white_background(self) -> None:
        """index.html should set background-color to white."""
        self.assertIn("background-color: #ffffff", self.html)

    def test_centered_layout(self) -> None:
        """index.html should use flexbox centering."""
        self.assertIn("display: flex", self.html)
        self.assertIn("justify-content: center", self.html)
        self.assertIn("align-items: center", self.html)


class TestRunServerImport(unittest.TestCase):
    """Verify that server.py can be imported and exposes run_server."""

    def test_run_server_is_callable(self) -> None:
        """run_server should be importable and callable."""
        import importlib
        import sys

        # Ensure the project root is on the path
        if PROJECT_ROOT not in sys.path:
            sys.path.insert(0, PROJECT_ROOT)

        mod = importlib.import_module("server")
        self.assertTrue(callable(getattr(mod, "run_server", None)))

    def test_run_server_default_args(self) -> None:
        """run_server should accept port and directory keyword arguments."""
        import importlib
        import inspect
        import sys

        if PROJECT_ROOT not in sys.path:
            sys.path.insert(0, PROJECT_ROOT)

        mod = importlib.import_module("server")
        sig = inspect.signature(mod.run_server)
        params = list(sig.parameters.keys())
        self.assertIn("port", params)
        self.assertIn("directory", params)

        # Check defaults
        self.assertEqual(sig.parameters["port"].default, 8000)
        self.assertEqual(sig.parameters["directory"].default, ".")


if __name__ == "__main__":
    unittest.main()
