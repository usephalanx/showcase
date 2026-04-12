"""FastAPI application with a single GET /hello endpoint.

Returns a JSON object containing a greeting message and the current
UTC timestamp in ISO-8601 format.
"""

from __future__ import annotations

import datetime

from fastapi import FastAPI
from pydantic import BaseModel


class HelloResponse(BaseModel):
    """Response model for the /hello endpoint."""

    message: str
    timestamp: str


app = FastAPI(title="Hello World API")


@app.get("/hello", response_model=HelloResponse)
async def hello() -> HelloResponse:
    """Return a hello world message with the current UTC timestamp."""
    now = datetime.datetime.now(datetime.timezone.utc)
    return HelloResponse(
        message="hello world",
        timestamp=now.isoformat(),
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
