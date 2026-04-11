"""API routes for the FastAPI application.

Defines an APIRouter with the following endpoints:
- GET /health — returns service health status
- GET /hello  — returns a greeting message
"""

from __future__ import annotations

from fastapi import APIRouter

router = APIRouter()


@router.get("/health", tags=["health"])
async def health() -> dict:
    """Return the current health status of the service."""
    return {"status": "ok"}


@router.get("/hello", tags=["hello"])
async def hello() -> dict:
    """Return a greeting message."""
    return {"message": "Hello, world!"}
