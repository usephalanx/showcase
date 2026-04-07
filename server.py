"""Lightweight Python HTTP server that serves static files from the current directory.

Uses only the Python standard library.  Designed to be run directly or
imported and started programmatically via :func:`run_server`.
"""

from __future__ import annotations

import functools
import http.server
import socketserver
from typing import Optional


def run_server(port: int = 8000, directory: str = ".") -> None:
    """Start an HTTP server serving *directory* on *port*.

    The server binds to ``0.0.0.0`` so it is reachable from outside a
    Docker container.

    Args:
        port: TCP port to listen on.  Defaults to ``8000``.
        directory: Filesystem directory to serve.  Defaults to ``"."``.
    """
    handler = functools.partial(
        http.server.SimpleHTTPRequestHandler,
        directory=directory,
    )

    # Allow quick restart without waiting for TIME_WAIT to expire
    socketserver.TCPServer.allow_reuse_address = True

    with socketserver.TCPServer(("0.0.0.0", port), handler) as httpd:
        print(f"Serving on http://0.0.0.0:{port}")
        httpd.serve_forever()


if __name__ == "__main__":
    run_server()
