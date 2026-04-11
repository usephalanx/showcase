"""FastAPI application entry point.

Creates the FastAPI app instance and defines the GET /hello endpoint.
"""

from __future__ import annotations

from fastapi import FastAPI

app = FastAPI(
    title="Hello World API",
    description="A minimal FastAPI application with a /hello endpoint.",
    version="1.0.0",
)


@app.get("/hello", tags=["hello"])
async def hello() -> dict:
    """Return a JSON greeting message.

    Returns:
        A dictionary with a single 'message' key.
    """
    return {"message": "Hello, World!"}
