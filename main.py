"""FastAPI application entry point.

Creates the FastAPI app, mounts the Todo CRUD router, and exposes
a lightweight health-check endpoint for operational monitoring.
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
    """Return a simple health status for liveness checks.

    Returns:
        A dictionary with a single key ``status`` set to ``"ok"``.
    """
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000)
