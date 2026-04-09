"""FastAPI application entry point.

Provides an Echo API with a health check endpoint and an echo endpoint
that returns any JSON body it receives.
"""

from __future__ import annotations

from typing import Any, Dict

from fastapi import FastAPI

app = FastAPI(
    title="Echo API",
    description="A minimal API that echoes JSON payloads and reports health.",
    version="1.0.0",
)


@app.get("/", tags=["health"])
async def health() -> Dict[str, str]:
    """Return a simple health-check response."""
    return {"status": "ok"}


@app.post("/echo", tags=["echo"])
async def echo(body: Dict[str, Any]) -> Dict[str, Any]:
    """Accept an arbitrary JSON object and return it unchanged.

    Args:
        body: Any valid JSON object (dict).

    Returns:
        The exact same JSON object that was received.
    """
    return body
