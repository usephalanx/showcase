"""FastAPI application entry point for the Todo backend.

Configures the application instance, CORS middleware (allowing the Vite
dev-server origin), and a startup event that ensures database tables
exist before the first request is served.
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.database import init_db
from backend.routes import router

# ---------------------------------------------------------------------------
# Allowed CORS origins – the Vite dev-server runs on port 5173 by default.
# ---------------------------------------------------------------------------

ALLOWED_ORIGINS: list[str] = [
    "http://localhost:5173",
]


# ---------------------------------------------------------------------------
# Application lifespan
# ---------------------------------------------------------------------------


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    """Run one-time startup logic before the app begins serving requests.

    Currently this only ensures that all SQLAlchemy-managed tables exist
    in the backing SQLite database.
    """
    init_db()
    yield


# ---------------------------------------------------------------------------
# FastAPI application instance
# ---------------------------------------------------------------------------

app = FastAPI(
    title="Todo API",
    description="A RESTful Todo API backed by SQLite and SQLAlchemy.",
    version="1.0.0",
    lifespan=lifespan,
)

# ---------------------------------------------------------------------------
# Middleware
# ---------------------------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------

app.include_router(router)
