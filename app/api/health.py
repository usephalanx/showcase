"""Health check endpoint router.

Provides a simple GET /health endpoint that returns the service status.
"""

from __future__ import annotations

from fastapi import APIRouter

router = APIRouter()


@router.get("/health", tags=["health"])
async def health() -> dict:
    """Return the current health status of the service."""
    return {"status": "ok"}
