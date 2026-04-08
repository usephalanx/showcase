"""FastAPI application entry point.

Initialises the FastAPI app with CORS middleware and includes
the Todo API router.  This module is the single source of the
``app`` instance used by uvicorn.
"""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import router

app = FastAPI(
    title="Todo API",
    description="A simple Todo REST API backed by SQLite (in-memory).",
    version="1.0.0",
)

# ---------------------------------------------------------------------------
# CORS Middleware – allow all origins during development.
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Include API routers
# ---------------------------------------------------------------------------
app.include_router(router)


@app.get("/", tags=["root"])
async def root() -> dict:
    """Return a welcome message at the API root."""
    return {"message": "Welcome to the Todo API"}
