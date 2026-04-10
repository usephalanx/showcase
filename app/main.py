"""FastAPI application entry point.

Creates the FastAPI app instance and includes the hello and health routers.
"""

from __future__ import annotations

from fastapi import FastAPI

from app.api.hello import router as hello_router
from app.api.health import router as health_router

app = FastAPI(
    title="Todo API",
    description="A simple Todo REST API with in-memory storage.",
    version="1.0.0",
)

app.include_router(hello_router)
app.include_router(health_router)
