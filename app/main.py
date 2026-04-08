"""FastAPI application entry point.

Initialises the FastAPI application with CORS middleware and includes
the todo router.  On startup, a small set of sample todos is seeded
into the in-memory store for demo purposes.

Run with::

    uvicorn app.main:app --reload
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.todos import router as todos_router
from app.seed import seed_todos
from app.storage import storage


# ---------------------------------------------------------------------------
# Lifespan – seeds demo data on startup
# ---------------------------------------------------------------------------


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    """Application lifespan handler.

    Seeds a few sample todo items into the in-memory store so the API
    has data available immediately for demonstration.
    """
    seed_todos(storage)
    yield


app = FastAPI(
    title="Todo API",
    description="A simple Todo REST API with in-memory storage.",
    version="1.0.0",
    lifespan=lifespan,
)

# ---------------------------------------------------------------------------
# CORS middleware – allow all origins for local development
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------
app.include_router(todos_router)


@app.get("/health", tags=["health"])
async def health_check() -> dict[str, str]:
    """Return a simple health-check response."""
    return {"status": "ok"}
