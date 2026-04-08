"""Unit and integration tests for the Todo FastAPI application.

Uses FastAPI's TestClient to exercise all CRUD endpoints and verify
correct status codes, response bodies, and 404 handling.  The
in-memory store is reset before every test via a pytest fixture.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

# Ensure the project root is on sys.path so that 'main', 'routes',
# 'storage', and 'models' can be imported.
_PROJECT_ROOT = str(Path(__file__).resolve().parent.parent)
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from main import app  # noqa: E402
from routes import store  # noqa: E402


@pytest.fixture(autouse=True)
def _reset_store() -> None:
    """Reset the in-memory todo store before each test."""
    store.reset()


client = TestClient(app)


# ------------------------------------------------------------------
# Helper
# ------------------------------------------------------------------

def _create_todo(
    title: str = "Test todo",
    description: str | None = None,
    completed: bool = False,
) -> dict:
    """Post a new todo and return the parsed JSON response."""
    payload: dict = {"title": title}
    if description is not None:
        payload["description"] = description
    if completed:
        payload["completed"] = completed
    response = client.post("/todos", json=payload)
    return response.json()


# ------------------------------------------------------------------
# POST /todos
# ------------------------------------------------------------------


def test_create_todo_minimal() -> None:
    """Creating a todo with only a title should succeed with 201."""
    response = client.post("/todos", json={"title": "Buy milk"})
    assert response.status_code == 201
    body = response.json()
    assert body["title"] == "Buy milk"
    assert body["completed"] is False
    assert body["description"] is None
    assert "id" in body
    assert "created_at" in body


def test_create_todo_with_description() -> None:
    """Creating a todo with a title and description should succeed."""
    response = client.post(
        "/todos",
        json={"title": "Read book", "description": "Chapter 5"},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["title"] == "Read book"
    assert body["description"] == "Chapter 5"
    assert body["completed"] is False


def test_create_todo_with_completed_flag() -> None:
    """Creating a todo that is already completed should honour the flag."""
    response = client.post(
        "/todos",
        json={"title": "Done task", "completed": True},
    )
    assert response.status_code == 201
    assert response.json()["completed"] is True


def test_create_todo_empty_title_rejected() -> None:
    """An empty title should be rejected (422 validation error)."""
    response = client.post("/todos", json={"title": ""})
    assert response.status_code == 422


# ------------------------------------------------------------------
# GET /todos
# ------------------------------------------------------------------


def test_list_todos_empty() -> None:
    """Listing todos when the store is empty should return an empty list."""
    response = client.get("/todos")
    assert response.status_code == 200
    assert response.json() == []


def test_list_todos_multiple() -> None:
    """Listing todos should return all created items."""
    _create_todo(title="First")
    _create_todo(title="Second")
    response = client.get("/todos")
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 2
    titles = {t["title"] for t in body}
    assert titles == {"First", "Second"}


# ------------------------------------------------------------------
# GET /todos/{id}
# ------------------------------------------------------------------


def test_get_single_todo() -> None:
    """Retrieving a todo by ID should return the correct item."""
    created = _create_todo(title="Specific todo", description="details")
    todo_id = created["id"]
    response = client.get(f"/todos/{todo_id}")
    assert response.status_code == 200
    body = response.json()
    assert body["id"] == todo_id
    assert body["title"] == "Specific todo"
    assert body["description"] == "details"


def test_get_todo_not_found() -> None:
    """Requesting a non-existent todo should return 404."""
    response = client.get("/todos/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Todo not found"


# ------------------------------------------------------------------
# PUT /todos/{id}
# ------------------------------------------------------------------


def test_update_todo_title() -> None:
    """Updating only the title should leave other fields unchanged."""
    created = _create_todo(title="Old title")
    todo_id = created["id"]
    response = client.put(f"/todos/{todo_id}", json={"title": "New title"})
    assert response.status_code == 200
    body = response.json()
    assert body["title"] == "New title"
    assert body["completed"] is False  # unchanged


def test_update_todo_completed() -> None:
    """Updating the completed flag should be reflected in the response."""
    created = _create_todo(title="Task")
    todo_id = created["id"]
    response = client.put(f"/todos/{todo_id}", json={"completed": True})
    assert response.status_code == 200
    assert response.json()["completed"] is True


def test_update_todo_description() -> None:
    """Updating the description should work."""
    created = _create_todo(title="Task")
    todo_id = created["id"]
    response = client.put(
        f"/todos/{todo_id}", json={"description": "new desc"}
    )
    assert response.status_code == 200
    assert response.json()["description"] == "new desc"


def test_update_todo_not_found() -> None:
    """Updating a non-existent todo should return 404."""
    response = client.put("/todos/9999", json={"title": "Nope"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Todo not found"


# ------------------------------------------------------------------
# DELETE /todos/{id}
# ------------------------------------------------------------------


def test_delete_todo() -> None:
    """Deleting an existing todo should succeed and remove it."""
    created = _create_todo(title="To be deleted")
    todo_id = created["id"]

    response = client.delete(f"/todos/{todo_id}")
    assert response.status_code == 200
    assert response.json()["detail"] == "Todo deleted successfully"

    # Confirm it's gone
    get_response = client.get(f"/todos/{todo_id}")
    assert get_response.status_code == 404


def test_delete_todo_not_found() -> None:
    """Deleting a non-existent todo should return 404."""
    response = client.delete("/todos/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Todo not found"


# ------------------------------------------------------------------
# Store isolation
# ------------------------------------------------------------------


def test_store_reset_between_tests() -> None:
    """Verify the store is empty at the start of each test (fixture works)."""
    response = client.get("/todos")
    assert response.status_code == 200
    assert response.json() == []
