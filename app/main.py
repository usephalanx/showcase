"""FastAPI application entry point.

Creates the FastAPI app instance and defines the /hello, /health, and / endpoints.
"""

from __future__ import annotations

from fastapi import FastAPI

app = FastAPI(
    title="Hello World API",
    description="A simple Hello World FastAPI application.",
    version="1.0.0",
)


@app.get("/", tags=["root"])
async def root() -> dict:
    """Return a welcome message at the API root."""
    return {"message": "Hello World"}


@app.get("/health", tags=["health"])
async def health() -> dict:
    """Return the health status of the application."""
    return {"status": "ok"}


@app.get("/hello", tags=["hello"])
async def hello() -> dict:
    """Return a Hello, World! greeting message."""
    return {"message": "Hello, World!"}
