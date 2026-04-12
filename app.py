"""FastAPI application with a GET /hello endpoint.

Returns a JSON payload containing a greeting message and the current
UTC timestamp in ISO 8601 format.
"""

from __future__ import annotations

import datetime

from fastapi import FastAPI
from pydantic import BaseModel


class HelloResponse(BaseModel):
    """Response model for the /hello endpoint."""

    message: str
    timestamp: str


app = FastAPI(title="Hello World API", version="1.0.0")


@app.get("/", tags=["root"])
async def root() -> dict:
    """Health-check endpoint returning a simple status object."""
    return {"status": "ok"}


@app.get("/hello", response_model=HelloResponse, tags=["hello"])
async def hello() -> HelloResponse:
    """Return a greeting with the current UTC timestamp."""
    return HelloResponse(
        message="hello world",
        timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    )
