"""Tests verifying that the FastAPI application creates tables on startup.

Uses the ASGI lifespan protocol via httpx.AsyncClient / TestClient to
ensure ``Base.metadata.create_all`` is invoked during the startup event.
"""

from __future__ import annotations

from sqlalchemy import inspect, text

from app.database import Base, engine
from app.models import Todo  # noqa: F401 – register model


def test_tables_created_on_startup() -> None:
    """After importing and starting the app, the 'todos' table must exist."""
    # Importing the app triggers the lifespan when used with TestClient.
    from fastapi.testclient import TestClient

    from app.main import app

    with TestClient(app) as client:
        # The lifespan has now fired; verify the table exists.
        inspector = inspect(engine)
        assert "todos" in inspector.get_table_names()

        # Also verify the root endpoint still works.
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Welcome to the Todo API"}


def test_create_all_is_idempotent() -> None:
    """Calling create_all multiple times should not raise."""
    Base.metadata.create_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    inspector = inspect(engine)
    assert "todos" in inspector.get_table_names()
