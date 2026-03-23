"""FastAPI application entry-point.

Initialises the database on startup and mounts the API router.
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import init_db
from app.routers import projects


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

# CORS – allow the Vite dev-server and common local origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(projects.router)


@app.get("/health", tags=["health"])
async def health_check() -> dict[str, str]:
    """Return a simple health-check response."""
    return {"status": "ok"}
