"""FastAPI application entry point for the Kanban backend.

Configures the ASGI application, includes routers, and sets up
startup events for database initialisation.
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI

from database import init_db
from routers.cards import router as cards_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Application lifespan handler.

    Creates database tables on startup.

    Args:
        app: The FastAPI application instance.

    Yields:
        Control back to the application.
    """
    init_db()
    yield


app = FastAPI(
    title="Kanban API",
    description="RESTful API for the Kanban board application.",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(cards_router)


@app.get("/health", tags=["health"])
def health_check() -> dict[str, str]:
    """Return a simple health check response.

    Returns:
        A dictionary with status 'ok'.
    """
    return {"status": "ok"}
