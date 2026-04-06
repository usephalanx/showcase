"""FastAPI application entry point for the Kanban backend.

Registers all routers and configures the application with CORS,
database initialization, and health-check endpoints.
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncIterator, Dict

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import init_db
from routers import boards, columns


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Application lifespan handler: initialise DB on startup."""
    init_db()
    yield


app = FastAPI(
    title="Kanban Board API",
    description="RESTful API for managing Kanban boards, columns, and cards.",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS – allow all origins during development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(boards.router)
app.include_router(columns.router)


@app.get("/health", tags=["health"])
def health_check() -> Dict[str, str]:
    """Return a simple health-check response."""
    return {"status": "ok"}
