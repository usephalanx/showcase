"""FastAPI application entry-point.

Configures CORS, registers routers, creates database tables on startup,
and seeds demo data.
"""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import CORS_ORIGINS
from app.database import Base, SessionLocal, engine
from app.routers.auth_router import router as auth_router
from app.seed import run_seed

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    """Application lifespan handler: create tables and seed on startup."""
    # Import models so Base.metadata knows about them
    import app.models  # noqa: F401

    logger.info("Creating database tables…")
    Base.metadata.create_all(bind=engine)

    # Seed demo data
    db = SessionLocal()
    try:
        run_seed(db)
    finally:
        db.close()

    yield


app = FastAPI(
    title="Kanban Board API",
    description="Backend API for the Phalanx Kanban board application.",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(auth_router)


@app.get("/health", tags=["health"])
def health_check() -> dict[str, str]:
    """Simple health-check endpoint."""
    return {"status": "ok"}
