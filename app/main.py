"""FastAPI application entry-point.

Configures the application, registers routers, adds CORS middleware,
and initialises the database on startup.
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import init_db, seed_default_user
from app.routers import auth, projects, tasks


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    """Application lifespan handler — creates tables and seeds data on startup."""
    init_db()
    seed_default_user()
    yield


app = FastAPI(
    title="TaskBoard API",
    description="Project and task management REST API.",
    version="0.1.0",
    lifespan=lifespan,
)

# ---------------------------------------------------------------------------
# CORS middleware — allows frontend dev servers to access the API
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------
app.include_router(auth.router)
app.include_router(projects.router, prefix="/api")
app.include_router(tasks.router, prefix="/api")


@app.get("/health", tags=["health"])
async def health_check() -> dict:
    """Simple health-check endpoint."""
    return {"status": "ok"}
