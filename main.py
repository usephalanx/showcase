"""Convenience entry point for running the Todo API.

Usage::

    python main.py

Starts Uvicorn on 127.0.0.1:8000 with auto-reload enabled.
"""

from __future__ import annotations

import uvicorn


def main() -> None:
    """Launch the Uvicorn server pointing at the FastAPI application."""
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )


if __name__ == "__main__":
    main()
