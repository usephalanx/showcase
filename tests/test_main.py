"""Unit and integration tests for the Todo API.

Uses FastAPI's TestClient to exercise all CRUD endpoints and verify
404 behaviour for missing resources.  The in-memory store is reset
before each test via the ``reset_store`` fixture.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Ensure the project root (where main.py lives) is importable.
_PROJECT_ROOT = str(Path(__file__).resolve().parent.parent)
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

import pytest
from fastapi.testclient import TestClient

from main import app
from routes import store


@pytest.fixture(autouse=True)
def reset_store() -> None:
    """Reset the in-memory TodoStore before every test."""
    store._todos.clear()
    store._counter = 0


@pytest.fixture()
def client() -> TestClient:
    """Return a TestClient bound to the FastAPI application."""
    return TestClient(app)


# ------------------------------------------------------------------
# POST /todos
# ------------------------------------------------------------------


def test_create_todo_minimal(client: TestClient) -> None:
    """POST /todos with only a title should return 201 and the new todo."""
    response = client.post("/todos", json={"title": "Buy milk"})
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Buy milk"
    assert data["description"] is None
    assert data["completed"] is False
    assert "created_at" in data


def test_create_todo_with_description(client: TestClient) -> None:
    """POST /todos with title and description should persist both."""
    response = client.post(
        "/todos",
        json={"title": "Read book", "description": "Chapter 3"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Read book"
    assert data["description"] == "Chapter 3"
    assert data["completed"] is False


def test_create_todo_with_completed_flag(client: TestClient) -> None:
    """POST /todos with completed=true should honour the flag."""
    response = client.post(
        "/todos",
        json={"title": "Already done", "completed": True},
    )
    assert response.status_code == 201
    assert response.json()["completed"] is True


def test_create_todo_empty_title_rejected(client: TestClient) -> None:
    """POST /todos with an empty title should be rejected (422)."""
    response = client.post("/todos", json={"title": ""})
    assert response.status_code == 422


# ------------------------------------------------------------------
# GET /todos
# ------------------------------------------------------------------


def test_list_todos_empty(client: TestClient) -> None:
    """GET /todos on an empty store should return an empty list."""
    response = client.get("/todos")
    assert response.status_code == 200
    assert response.json() == []


def test_list_todos_multiple(client: TestClient) -> None:
    """GET /todos should return all created items."""
    client.post("/todos", json={"title": "First"})
    client.post("/todos", json={"title": "Second"})
    response = client.get("/todos")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    titles = {item["title"] for item in data}
    assert titles == {"First", "Second"}


# ------------------------------------------------------------------
# GET /todos/{id}
# ------------------------------------------------------------------


def test_get_single_todo(client: TestClient) -> None:
    """GET /todos/{id} should return the matching todo."""
    create_resp = client.post("/todos", json={"title": "Unique"})
    todo_id = create_resp.json()["id"]
    response = client.get(f"/todos/{todo_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Unique"


def test_get_todo_not_found(client: TestClient) -> None:
    """GET /todos/{id} for a non-existent ID should return 404."""
    response = client.get("/todos/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Todo not found"


# ------------------------------------------------------------------
# PUT /todos/{id}
# ------------------------------------------------------------------


def test_update_todo_title(client: TestClient) -> None:
    """PUT /todos/{id} should update only the supplied fields."""
    create_resp = client.post("/todos", json={"title": "Old title"})
    todo_id = create_resp.json()["id"]
    response = client.put(
        f"/todos/{todo_id}",
        json={"title": "New title"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New title"
    # Other fields unchanged
    assert data["completed"] is False


def test_update_todo_completed(client: TestClient) -> None:
    """PUT /todos/{id} can toggle the completed flag."""
    create_resp = client.post("/todos", json={"title": "Task"})
    todo_id = create_resp.json()["id"]
    response = client.put(
        f"/todos/{todo_id}",
        json={"completed": True},
    )
    assert response.status_code == 200
    assert response.json()["completed"] is True


def test_update_todo_description(client: TestClient) -> None:
    """PUT /todos/{id} can set a description."""
    create_resp = client.post("/todos", json={"title": "Task"})
    todo_id = create_resp.json()["id"]
    response = client.put(
        f"/todos/{todo_id}",
        json={"description": "Details here"},
    )
    assert response.status_code == 200
    assert response.json()["description"] == "Details here"


def test_update_todo_not_found(client: TestClient) -> None:
    """PUT /todos/{id} for a non-existent ID should return 404."""
    response = client.put("/todos/999", json={"title": "Nope"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Todo not found"


# ------------------------------------------------------------------
# DELETE /todos/{id}
# ------------------------------------------------------------------


def test_delete_todo(client: TestClient) -> None:
    """DELETE /todos/{id} should remove the todo and return success."""
    create_resp = client.post("/todos", json={"title": "To remove"})
    todo_id = create_resp.json()["id"]
    response = client.delete(f"/todos/{todo_id}")
    assert response.status_code == 200
    assert response.json()["detail"] == "Todo deleted successfully"

    # Confirm it's gone
    get_resp = client.get(f"/todos/{todo_id}")
    assert get_resp.status_code == 404


def test_delete_todo_not_found(client: TestClient) -> None:
    """DELETE /todos/{id} for a non-existent ID should return 404."""
    response = client.delete("/todos/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Todo not found"


# ------------------------------------------------------------------
# Store isolation
# ------------------------------------------------------------------


def test_store_is_reset_between_tests(client: TestClient) -> None:
    """Verify the autouse fixture resets the store (IDs restart at 1)."""
    response = client.post("/todos", json={"title": "Fresh"})
    assert response.status_code == 201
    assert response.json()["id"] == 1
