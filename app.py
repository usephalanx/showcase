"""FastAPI Hello World application.

Provides a single GET /hello endpoint that returns a JSON greeting.
This module can also be used as a lightweight health-check target.

Runnable with: uvicorn app:app --reload
"""

from __future__ import annotations

from fastapi import FastAPI

app = FastAPI(
    title="Hello World API",
    description="A minimal Hello World endpoint.",
    version="1.0.0",
)


@app.get("/hello", tags=["hello"])
async def hello() -> dict:
    """Return a JSON greeting.

    Returns:
        A dictionary with a single 'message' key set to 'hello world'.
    """
    return {"message": "hello world"}
