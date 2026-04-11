"""FastAPI application entry point.

Creates the FastAPI app and mounts the Todo CRUD router.
Provides /health and / root endpoints.
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
    return {"message": "Hello World"}


@app.get("/health", tags=["health"])
async def health() -> dict:
    """Return the health status of the application."""
    return {"status": "ok"}
