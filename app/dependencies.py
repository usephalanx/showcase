"""Shared FastAPI dependencies.

Re-exports the database session dependency for convenience and provides
a central location for future cross-cutting dependencies (e.g. current
user extraction).
"""

from __future__ import annotations

from app.core.database import get_db

__all__ = ["get_db"]
