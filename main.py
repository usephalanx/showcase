"""FastAPI application entry point.

Creates the FastAPI app and mounts the Todo CRUD router.
Also re-exports the /health endpoint from app.main.
"""

from __future__ import annotations

from fastapi import FastAPI

from routes import router

app = FastAPI(
    title="Todo API",
    description="A simple Todo REST API with in-memory storage.",
    version="1.0.0",
)

app.include_router(router)


@app.get("/", tags=["root"])
async def root() -> dict:
    """Return a welcome message at the API root."""
    return {"message": "Welcome to the Todo API"}


@app.get("/health", tags=["health"])
async def health() -> dict:
    """Return a simple health-check response.

    Returns:
        A JSON object with a single key ``status`` set to ``"ok"``.
    """
    return {"status": "ok"}
