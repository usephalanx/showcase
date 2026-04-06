"""API route definitions for the Todo application.

This module defines the :data:`router` that is included by the main
application.  Endpoint implementations will be added in a subsequent
task.
"""

from __future__ import annotations

from fastapi import APIRouter

router = APIRouter()


@router.get("/health", tags=["health"])
async def health_check() -> dict[str, str]:
    """Return a simple health-check response.

    Returns:
        A JSON object with a ``status`` key set to ``ok``.
    """
    return {"status": "ok"}
