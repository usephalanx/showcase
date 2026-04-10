"""FastAPI application entry point.

Creates the FastAPI app instance and defines the /health endpoint.
"""

from __future__ import annotations

from fastapi import FastAPI

app = FastAPI(
    title="Todo API",
    description="A simple Todo REST API with in-memory storage.",
    version="1.0.0",
)


@app.get("/health", tags=["health"])
async def health() -> dict:
    """Return a simple health-check response.

    Returns:
        A JSON object with a single key ``status`` set to ``"ok"``.
    """
    return {"status": "ok"}
