"""FastAPI application entry point.

Creates the FastAPI app instance and includes the hello and health routers.
"""

from __future__ import annotations

from fastapi import FastAPI

from app.api.hello import router as hello_router
from app.api.health import router as health_router

app = FastAPI(
    title="Hello & Health API",
    description="A minimal FastAPI app with /hello and /health endpoints.",
    version="1.0.0",
)

app.include_router(hello_router)
app.include_router(health_router)
