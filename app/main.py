"""FastAPI application with a single GET / endpoint.

Returns {"message": "hello"} and includes a standard uvicorn entrypoint
for direct execution.
"""

from __future__ import annotations

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel


class HelloResponse(BaseModel):
    """Response model for the hello endpoint."""

    message: str


app = FastAPI(
    title="Hello API",
    description="A minimal API that returns a hello message.",
    version="1.0.0",
)


@app.get("/", response_model=HelloResponse, tags=["hello"])
async def root() -> HelloResponse:
    """Return a hello message."""
    return HelloResponse(message="hello")


if __name__ == "__main__":  # pragma: no cover
    uvicorn.run(app, host="0.0.0.0", port=8000)
