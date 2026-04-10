"""FastAPI application entry point.

Initialises the FastAPI app and defines the GET /hello endpoint.
"""

from __future__ import annotations

from fastapi import FastAPI

app = FastAPI(
    title="Hello API",
    description="A minimal API server with a /hello endpoint.",
    version="0.1.0",
)


@app.get("/hello", tags=["hello"])
async def hello() -> dict:
    """Return a simple JSON greeting."""
    return {"message": "hello"}
