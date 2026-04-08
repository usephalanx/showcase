"""FastAPI application entry point.

Initialises the FastAPI application with CORS middleware and includes
the todo router.  Run with::

    uvicorn app.main:app --reload
"""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.todos import router as todos_router

app = FastAPI(
    title="Todo API",
    description="A simple Todo REST API with in-memory storage.",
    version="1.0.0",
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
