"""FastAPI application entry point.

Initialises the FastAPI app with CORS middleware and includes
the Todo API router.  This module is the single source of the
``app`` instance used by uvicorn.

On startup the SQLAlchemy ``Base.metadata.create_all`` call ensures
that all ORM tables exist in the (in-memory) SQLite database.
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.models import Todo  # noqa: F401 – ensure model is registered on Base
from app.routers import router


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    """Application lifespan handler – create DB tables on startup."""
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Todo API",
    description="A simple Todo REST API backed by SQLite (in-memory).",
    version="1.0.0",
    lifespan=lifespan,
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
