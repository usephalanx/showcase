"""Integration tests for the Todo API endpoints.

Uses :class:`httpx.AsyncClient` via ``pytest`` to exercise the full
request/response cycle through the FastAPI application.

Each test function gets a clean storage instance to ensure isolation.
"""

from __future__ import annotations

from typing import Generator

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.storage import storage


@pytest.fixture(autouse=True)
def _clean_storage() -> Generator[None, None, None]:
    """Clear the in-memory store before and after every test."""
    storage.clear()
    yield
    storage.clear()


# -------------------------------------------------------------------
# Helpers
# -------------------------------------------------------------------

_client = TestClient(app, raise_server_exceptions=False)


def _create_todo(
    title: str = "Test todo",
    description: str = "A test description",
) -> dict:
    """Helper to POST a new todo and return the JSON response body."""
    response = _client.post(
        "/todos",
        json={"title": title, "description": description},
    )
    assert response.status_code == 201
    return response.json()


# -------------------------------------------------------------------
# POST /todos
# -------------------------------------------------------------------


def test_create_todo() -> None:
    """POST /todos should create a todo and return it with status 201."""
    body = {"title": "Buy milk", "description": "2% milk from the store"}
    response = _client.post("/todos", json=body)

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Buy milk"
    assert data["description"] == "2% milk from the store"
    assert data["completed"] is False
    assert isinstance(data["id"], int)


def test_create_todo_minimal() -> None:
    """POST /todos with only title should default description to empty string."""
    response = _client.post("/todos", json={"title": "Minimal"})

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Minimal"
    assert data["description"] == ""
    assert data["completed"] is False


def test_create_todo_missing_title_returns_422() -> None:
    """POST /todos without a title should return 422."""
    response = _client.post("/todos", json={"description": "no title"})
    assert response.status_code == 422


def test_create_todo_empty_title_returns_422() -> None:
    """POST /todos with an empty title string should return 422."""
    response = _client.post("/todos", json={"title": ""})
    assert response.status_code == 422


# -------------------------------------------------------------------
# GET /todos
# -------------------------------------------------------------------


def test_list_todos_empty() -> None:
    """GET /todos on an empty store should return an empty list."""
    response = _client.get("/todos")
    assert response.status_code == 200
    assert response.json() == []


def test_list_todos() -> None:
    """GET /todos should return all created items."""
    _create_todo(title="First")
    _create_todo(title="Second")

    response = _client.get("/todos")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    titles = {item["title"] for item in data}
    assert titles == {"First", "Second"}


# -------------------------------------------------------------------
# GET /todos/{id}
# -------------------------------------------------------------------


def test_get_todo_by_id() -> None:
    """GET /todos/{id} should return the correct item."""
    created = _create_todo(title="Specific")
    todo_id = created["id"]

    response = _client.get(f"/todos/{todo_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == todo_id
    assert data["title"] == "Specific"


def test_get_todo_not_found_returns_404() -> None:
    """GET /todos/{id} with a non-existent id should return 404."""
    response = _client.get("/todos/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Todo not found"


# -------------------------------------------------------------------
# PUT /todos/{id}
# -------------------------------------------------------------------


def test_update_todo() -> None:
    """PUT /todos/{id} should update the specified fields."""
    created = _create_todo(title="Old title")
    todo_id = created["id"]

    response = _client.put(
        f"/todos/{todo_id}",
        json={"title": "New title", "completed": True},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New title"
    assert data["completed"] is True
    # Description should remain unchanged
    assert data["description"] == created["description"]


def test_update_todo_partial() -> None:
    """PUT /todos/{id} with only one field should leave others unchanged."""
    created = _create_todo(title="Original", description="Keep me")
    todo_id = created["id"]

    response = _client.put(
        f"/todos/{todo_id}",
        json={"completed": True},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Original"
    assert data["description"] == "Keep me"
    assert data["completed"] is True


def test_update_todo_not_found_returns_404() -> None:
    """PUT /todos/{id} with a non-existent id should return 404."""
    response = _client.put("/todos/99999", json={"title": "Nope"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Todo not found"


# -------------------------------------------------------------------
# DELETE /todos/{id}
# -------------------------------------------------------------------


def test_delete_todo() -> None:
    """DELETE /todos/{id} should return 204 and remove the item."""
    created = _create_todo(title="Delete me")
    todo_id = created["id"]

    response = _client.delete(f"/todos/{todo_id}")
    assert response.status_code == 204
    assert response.content == b""

    # Confirm it is gone
    get_response = _client.get(f"/todos/{todo_id}")
    assert get_response.status_code == 404


def test_delete_todo_not_found_returns_404() -> None:
    """DELETE /todos/{id} with a non-existent id should return 404."""
    response = _client.delete("/todos/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Todo not found"


# -------------------------------------------------------------------
# GET /health
# -------------------------------------------------------------------


def test_health_check() -> None:
    """GET /health should return 200 with status ok."""
    response = _client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
