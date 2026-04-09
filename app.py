"""FastAPI application entry point with a hello world endpoint.

Creates the FastAPI app, mounts the Todo CRUD router, and exposes
a simple GET /hello endpoint that returns a greeting.
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


@app.get("/hello", tags=["hello"])
async def hello() -> dict:
    """Return a simple hello world greeting."""
    return {"message": "hello world"}


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000)
