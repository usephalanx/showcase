"""FastAPI application entry point.

Creates the FastAPI app instance and includes the API router
from app.api.routes, which defines the /health and /hello endpoints.
"""

from __future__ import annotations

from fastapi import FastAPI

from app.api.routes import router

app = FastAPI(
    title="FastAPI App",
    description="A simple FastAPI application with health and hello endpoints.",
    version="1.0.0",
)

app.include_router(router)
