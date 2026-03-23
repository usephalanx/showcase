"""FastAPI application entry-point.

Initialises the database on startup and mounts the API routers.
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI

from app.database import init_db
from app.routers.auth import router as auth_router


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    """Run startup tasks (DB init) and yield control to the application."""
    init_db()
    yield


app = FastAPI(
    title="Project Management API",
    description="A project and task management REST API backed by SQLite.",
    version="0.1.0",
    lifespan=lifespan,
)

# Mount routers
app.include_router(auth_router)


@app.get("/health", tags=["health"])
async def health_check() -> dict[str, str]:
    """Return a simple health-check response."""
    return {"status": "ok"}
