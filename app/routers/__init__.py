"""API routers package.

Re-exports the top-level ``router`` so that ``app.main`` can simply do::

    from app.routers import router

When concrete endpoint modules (e.g. ``todos.py``) are added they
should be included into the ``router`` defined here.
"""

from __future__ import annotations

from fastapi import APIRouter

router = APIRouter()

# Future routers will be included here, e.g.:
# from app.routers.todos import router as todos_router
# router.include_router(todos_router)
