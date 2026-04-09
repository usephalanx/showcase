"""FastAPI application entry point.

Creates the FastAPI app and mounts the Todo CRUD router.
Provides a /health endpoint for liveness checks.
"""

from __future__ import annotations

import uvicorn
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
async def health_check() -> dict:
    """Return a simple health-check response indicating the service is alive."""
    return {"message": "hi"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
