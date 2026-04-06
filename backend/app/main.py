"""FastAPI application entry-point.

Tables are auto-created on startup via the lifespan context manager so
there is no need for a separate Alembic migration step during
initial development.
"""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import init_db


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    """Application lifespan: initialise the database on startup."""
    # Import models so Base.metadata is fully populated before create_all.
    import app.models  # noqa: F401

    init_db()
    yield


app = FastAPI(
    title="Todo Task API",
    description="A task management REST API backed by SQLite.",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/health", tags=["meta"])
async def health_check() -> dict[str, str]:
    """Simple health-check endpoint."""
    return {"status": "ok"}
