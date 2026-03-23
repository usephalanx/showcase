"""FastAPI application entry-point.

Configures the application, registers routers, and initialises the
database on startup.
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI

from app.core.database import init_db
from app.routers import projects, tasks


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    """Application lifespan handler — creates tables on startup."""
    init_db()
    yield


app = FastAPI(
    title="TaskBoard API",
    description="Project and task management REST API.",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(projects.router, prefix="/api")
app.include_router(tasks.router, prefix="/api")


@app.get("/health", tags=["health"])
async def health_check() -> dict:
    """Simple health-check endpoint."""
    return {"status": "ok"}
