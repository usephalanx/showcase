"""FastAPI application entry point.

Creates the FastAPI app instance and defines the /hello endpoint.
"""

from __future__ import annotations

from fastapi import FastAPI

app = FastAPI(
    title="Hello World API",
    description="A simple Hello World FastAPI application.",
    version="1.0.0",
)


@app.get("/hello", tags=["hello"])
async def hello() -> dict:
    """Return a Hello, World! greeting message."""
    return {"message": "Hello, World!"}
