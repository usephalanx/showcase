"""Minimal HTTP server for the Yellow World static site.

Serves files from the ``public/`` directory using Python's built-in
``http.server`` module.  The port defaults to **8000** and can be
overridden with the ``PORT`` environment variable.
"""

from __future__ import annotations

import os
import sys
from functools import partial
from http.server import HTTPServer, SimpleHTTPRequestHandler

DIRECTORY: str = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public")
PORT: int = int(os.environ.get("PORT", "8000"))


def create_handler() -> type:
    """Return a request-handler class bound to the public directory."""
    return partial(SimpleHTTPRequestHandler, directory=DIRECTORY)


def run_server(port: int = PORT) -> None:
    """Start the HTTP server on the given port.

    Args:
        port: TCP port to listen on.  Defaults to the module-level PORT.
    """
    handler = create_handler()
    server = HTTPServer(("0.0.0.0", port), handler)
    print(f"Serving Yellow World at http://localhost:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down.")
        server.server_close()
        sys.exit(0)


if __name__ == "__main__":
    run_server()
