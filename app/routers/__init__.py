"""API routers package.

Re-exports the top-level ``router`` so that ``app.main`` can simply do::

    from app.routers import router

All concrete endpoint modules are included into the ``router`` defined
here.
"""

from __future__ import annotations

from fastapi import APIRouter

from app.routes import router as todos_router

router = APIRouter()
router.include_router(todos_router)
