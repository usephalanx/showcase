"""FastAPI application entry point.

Creates the FastAPI app, mounts the Todo CRUD router, and exposes
a root GET endpoint that returns a hello message.
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
    """Return a hello message at the API root."""
    return {"message": "hello"}
