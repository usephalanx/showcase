"""Shared pytest fixtures for the Todo app test suite.

Provides fixtures for a clean TodoStore, a fresh database, and
a FastAPI TestClient.
"""

from __future__ import annotations

import os
import sqlite3
import sys
from pathlib import Path
from typing import Generator

import pytest

# Ensure project root is on sys.path so imports resolve.
_PROJECT_ROOT = str(Path(__file__).resolve().parent.parent)
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from storage import TodoStore  # noqa: E402


@pytest.fixture()
def todo_store() -> TodoStore:
    """Return a fresh, empty TodoStore instance for each test."""
    store = TodoStore()
    return store


@pytest.fixture()
def populated_store() -> TodoStore:
    """Return a TodoStore pre-populated with three sample todos."""
    store = TodoStore()
    store.add(title="Buy groceries", description="Milk, eggs, bread")
    store.add(title="Write tests", description="Cover all endpoints", completed=True)
    store.add(title="Deploy app", description=None, completed=False)
    return store


@pytest.fixture()
def _tmp_database(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Create a temporary SQLite database file and patch database.DATABASE_PATH.

    This ensures each test using the database layer gets a completely
    isolated, temporary database.
    """
    # We need to import database lazily so patching works.
    import database  # noqa: E402

    db_path = tmp_path / "test_todos.db"
    monkeypatch.setattr(database, "DATABASE_PATH", str(db_path))
    database.init_db()
    return db_path


@pytest.fixture()
def db_connection(_tmp_database: Path) -> Generator[sqlite3.Connection, None, None]:
    """Yield a connection to the temporary test database."""
    import database  # noqa: E402

    conn = database.get_db_connection()
    yield conn
    conn.close()
