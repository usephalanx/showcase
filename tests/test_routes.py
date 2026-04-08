"""Tests for the Todo API route endpoints.

Covers all CRUD operations exposed via ``app/routes.py``:

- ``GET /todos`` – list with pagination
- ``GET /todos/{todo_id}`` – get by id, including 404
- ``POST /todos`` – create, status 201
- ``PUT /todos/{todo_id}`` – update, including 404
- ``DELETE /todos/{todo_id}`` – delete 204, including 404

Uses an independent in-memory SQLite database for full isolation.
"""

from __future__ import annotations

from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.database import Base, get_db
from app.main import app

# ---------------------------------------------------------------------------
# Test database setup
# ---------------------------------------------------------------------------
SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
TestingSessionLocal: sessionmaker[Session] = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def override_get_db() -> Generator[Session, None, None]:
    """Yield a test database session."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def _setup_database() -> Generator[None, None, None]:
    """Create all tables before each test and drop them after."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


client = TestClient(app)


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------
def _create_todo(
    title: str = "Test Todo",
    description: str | None = None,
) -> dict:
    """Create a todo via POST and return the JSON response body."""
    payload: dict = {"title": title}
    if description is not None:
        payload["description"] = description
    response = client.post("/todos", json=payload)
    assert response.status_code == 201
    return response.json()


# ---------------------------------------------------------------------------
# POST /todos
# ---------------------------------------------------------------------------
class TestCreateTodo:
    """Tests for the POST /todos endpoint."""

    def test_create_todo_minimal(self) -> None:
        """Create a todo with only a title."""
        response = client.post("/todos", json={"title": "Buy milk"})
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Buy milk"
        assert data["description"] is None
        assert data["completed"] is False
        assert "id" in data
        assert "created_at" in data

    def test_create_todo_with_description(self) -> None:
        """Create a todo with title and description."""
        response = client.post(
            "/todos",
            json={"title": "Groceries", "description": "Eggs, bread, cheese"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Groceries"
        assert data["description"] == "Eggs, bread, cheese"

    def test_create_todo_empty_title_rejected(self) -> None:
        """An empty title string must be rejected (422)."""
        response = client.post("/todos", json={"title": ""})
        assert response.status_code == 422

    def test_create_todo_missing_title_rejected(self) -> None:
        """A request body without a title must be rejected (422)."""
        response = client.post("/todos", json={})
        assert response.status_code == 422


# ---------------------------------------------------------------------------
# GET /todos
# ---------------------------------------------------------------------------
class TestListTodos:
    """Tests for the GET /todos endpoint."""

    def test_list_empty(self) -> None:
        """An empty database returns an empty list."""
        response = client.get("/todos")
        assert response.status_code == 200
        assert response.json() == []

    def test_list_multiple(self) -> None:
        """Multiple todos are returned."""
        _create_todo("First")
        _create_todo("Second")
        response = client.get("/todos")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

    def test_list_with_skip(self) -> None:
        """The skip query parameter offsets results."""
        _create_todo("A")
        _create_todo("B")
        _create_todo("C")
        response = client.get("/todos", params={"skip": 2})
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1

    def test_list_with_limit(self) -> None:
        """The limit query parameter caps results."""
        _create_todo("A")
        _create_todo("B")
        _create_todo("C")
        response = client.get("/todos", params={"limit": 2})
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

    def test_list_with_skip_and_limit(self) -> None:
        """Both skip and limit work together."""
        for i in range(5):
            _create_todo(f"Item {i}")
        response = client.get("/todos", params={"skip": 1, "limit": 2})
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2


# ---------------------------------------------------------------------------
# GET /todos/{todo_id}
# ---------------------------------------------------------------------------
class TestGetTodo:
    """Tests for the GET /todos/{todo_id} endpoint."""

    def test_get_existing(self) -> None:
        """Retrieve a todo by its ID."""
        created = _create_todo("Read book")
        todo_id = created["id"]
        response = client.get(f"/todos/{todo_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == todo_id
        assert data["title"] == "Read book"

    def test_get_not_found(self) -> None:
        """A non-existent ID returns 404 with proper detail."""
        response = client.get("/todos/99999")
        assert response.status_code == 404
        assert response.json()["detail"] == "Todo not found"


# ---------------------------------------------------------------------------
# PUT /todos/{todo_id}
# ---------------------------------------------------------------------------
class TestUpdateTodo:
    """Tests for the PUT /todos/{todo_id} endpoint."""

    def test_update_title(self) -> None:
        """Update only the title of an existing todo."""
        created = _create_todo("Old title")
        todo_id = created["id"]
        response = client.put(
            f"/todos/{todo_id}",
            json={"title": "New title"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "New title"
        # Other fields remain unchanged
        assert data["completed"] is False

    def test_update_completed(self) -> None:
        """Mark a todo as completed."""
        created = _create_todo("Task")
        todo_id = created["id"]
        response = client.put(
            f"/todos/{todo_id}",
            json={"completed": True},
        )
        assert response.status_code == 200
        assert response.json()["completed"] is True

    def test_update_description(self) -> None:
        """Update the description of a todo."""
        created = _create_todo("Task", description="old desc")
        todo_id = created["id"]
        response = client.put(
            f"/todos/{todo_id}",
            json={"description": "new desc"},
        )
        assert response.status_code == 200
        assert response.json()["description"] == "new desc"

    def test_update_multiple_fields(self) -> None:
        """Update multiple fields in a single request."""
        created = _create_todo("Original")
        todo_id = created["id"]
        response = client.put(
            f"/todos/{todo_id}",
            json={"title": "Updated", "completed": True, "description": "Done"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated"
        assert data["completed"] is True
        assert data["description"] == "Done"

    def test_update_not_found(self) -> None:
        """Updating a non-existent todo returns 404."""
        response = client.put(
            "/todos/99999",
            json={"title": "Nope"},
        )
        assert response.status_code == 404
        assert response.json()["detail"] == "Todo not found"

    def test_update_empty_title_rejected(self) -> None:
        """An empty title string in an update must be rejected (422)."""
        created = _create_todo("Valid")
        todo_id = created["id"]
        response = client.put(
            f"/todos/{todo_id}",
            json={"title": ""},
        )
        assert response.status_code == 422


# ---------------------------------------------------------------------------
# DELETE /todos/{todo_id}
# ---------------------------------------------------------------------------
class TestDeleteTodo:
    """Tests for the DELETE /todos/{todo_id} endpoint."""

    def test_delete_existing(self) -> None:
        """Deleting an existing todo returns 204 with no body."""
        created = _create_todo("To be deleted")
        todo_id = created["id"]
        response = client.delete(f"/todos/{todo_id}")
        assert response.status_code == 204
        assert response.content == b""

        # Verify it is gone
        get_response = client.get(f"/todos/{todo_id}")
        assert get_response.status_code == 404

    def test_delete_not_found(self) -> None:
        """Deleting a non-existent todo returns 404."""
        response = client.delete("/todos/99999")
        assert response.status_code == 404
        assert response.json()["detail"] == "Todo not found"

    def test_delete_idempotent(self) -> None:
        """Deleting the same todo twice returns 404 on the second call."""
        created = _create_todo("Delete me")
        todo_id = created["id"]
        first = client.delete(f"/todos/{todo_id}")
        assert first.status_code == 204
        second = client.delete(f"/todos/{todo_id}")
        assert second.status_code == 404


# ---------------------------------------------------------------------------
# Integration / round-trip tests
# ---------------------------------------------------------------------------
class TestRoundTrip:
    """End-to-end tests exercising multiple endpoints in sequence."""

    def test_create_read_update_delete(self) -> None:
        """Full lifecycle: create → read → update → read → delete → 404."""
        # Create
        created = _create_todo("Lifecycle test", description="Step 1")
        todo_id = created["id"]
        assert created["completed"] is False

        # Read
        read_resp = client.get(f"/todos/{todo_id}")
        assert read_resp.status_code == 200
        assert read_resp.json()["title"] == "Lifecycle test"

        # Update
        update_resp = client.put(
            f"/todos/{todo_id}",
            json={"completed": True, "description": "Done"},
        )
        assert update_resp.status_code == 200
        assert update_resp.json()["completed"] is True
        assert update_resp.json()["description"] == "Done"
        # Title should not have changed
        assert update_resp.json()["title"] == "Lifecycle test"

        # Read again to confirm persistence
        read_resp2 = client.get(f"/todos/{todo_id}")
        assert read_resp2.json()["completed"] is True

        # Delete
        del_resp = client.delete(f"/todos/{todo_id}")
        assert del_resp.status_code == 204

        # Verify deletion
        final_resp = client.get(f"/todos/{todo_id}")
        assert final_resp.status_code == 404
