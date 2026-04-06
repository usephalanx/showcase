"""FastAPI application entry-point for the Kanban backend.

Registers all routers, configures CORS for the frontend dev server,
and initialises the database on startup.
"""

from __future__ import annotations

import os
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import init_db
from routers.boards import router as boards_router
from routers.cards import router as cards_router
from routers.categories import router as categories_router
from routers.columns import router as columns_router
from routers.seo import router as seo_router

# ---------------------------------------------------------------------------
# CORS configuration
# ---------------------------------------------------------------------------

# Comma-separated list of allowed origins; defaults to typical Vite dev server
CORS_ORIGINS: list[str] = [
    origin.strip()
    for origin in os.environ.get(
        "CORS_ORIGINS",
        "http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000,http://127.0.0.1:3000",
    ).split(",")
    if origin.strip()
]


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

# ---------------------------------------------------------------------------
# Middleware
# ---------------------------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------

app.include_router(boards_router)
app.include_router(columns_router)
app.include_router(cards_router)
app.include_router(categories_router)
app.include_router(seo_router)


@app.get("/health", tags=["health"])
def health_check() -> dict[str, str]:
    """Return a simple health-check response."""
    return {"status": "ok"}
