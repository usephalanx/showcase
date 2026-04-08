"""FastAPI application entry point.

Creates the FastAPI app and mounts the Todo CRUD router.
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
    return {"message": "Todo API is running"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
