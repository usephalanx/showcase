"""FastAPI application entry-point for the Kanban backend.

Registers all routers and initialises the database on startup.
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI

from database import init_db
from routers.categories import router as categories_router
from routers.seo import router as seo_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Application lifespan: initialise DB tables on startup."""
    init_db()
    yield


app = FastAPI(
    title="Kanban Board API",
    description="RESTful API for managing Kanban boards, columns, cards, and categories.",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(categories_router)
app.include_router(seo_router)


@app.get("/health", tags=["health"])
def health_check() -> dict[str, str]:
    """Return a simple health-check response."""
    return {"status": "ok"}
