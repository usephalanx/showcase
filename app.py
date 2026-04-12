"""FastAPI application with a single GET /hello endpoint.

Returns a JSON object containing a greeting message and the current
UTC timestamp in ISO-8601 format.
"""

from __future__ import annotations

import datetime

from fastapi import FastAPI

app = FastAPI(title="Hello World API")


@app.get("/hello")
async def hello() -> dict:
    """Return a hello world message with the current UTC timestamp."""
    return {
        "message": "hello world",
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
