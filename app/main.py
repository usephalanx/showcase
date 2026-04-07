"""FastAPI application entry point.

Creates the FastAPI app instance and registers the todo CRUD router.
"""

from __future__ import annotations

from fastapi import FastAPI

from app.routes import router

app = FastAPI(
    title="Todo API",
    description="A simple Todo REST API with in-memory storage.",
    version="1.0.0",
)

app.include_router(router)
