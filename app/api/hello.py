"""Hello endpoint router.

Provides a simple GET /hello endpoint that returns a greeting message.
"""

from __future__ import annotations

from fastapi import APIRouter

router = APIRouter()


@router.get("/hello", tags=["hello"])
async def hello() -> dict:
    """Return a hello world greeting message."""
    return {"message": "hello world"}
