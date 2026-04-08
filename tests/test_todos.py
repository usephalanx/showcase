"""CRUD tests for the /todos endpoints."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.storage import storage

client = TestClient(app)


@pytest.fixture(autouse=True)
def _reset_storage() -> None:
    """Clear the in-memory store before every test."""
    storage.clear()


# -- Create ------------------------------------------------------------------


def test_create_todo() -> None:
    """POST /todos should create a todo and return 201."""
    response = client.post(
        "/todos", json={"title": "Buy milk", "description": "2% preferred"}
    )
    assert response.status_code == 201
    body = response.json()
    assert body["title"] == "Buy milk"
    assert body["description"] == "2% preferred"
    assert body["completed"] is False
    assert "id" in body


def test_create_todo_missing_title_returns_422() -> None:
    """POST /todos without a title should return 422."""
    response = client.post("/todos", json={"description": "no title"})
    assert response.status_code == 422


# -- List --------------------------------------------------------------------


def test_list_todos() -> None:
    """GET /todos should return all created todos."""
    client.post("/todos", json={"title": "A"})
    client.post("/todos", json={"title": "B"})
    response = client.get("/todos")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_list_todos_empty() -> None:
    """GET /todos on an empty store should return an empty list."""
    response = client.get("/todos")
    assert response.status_code == 200
    assert response.json() == []


# -- Get by ID ---------------------------------------------------------------


def test_get_todo_by_id() -> None:
    """GET /todos/{id} should return the matching todo."""
    create_resp = client.post("/todos", json={"title": "Read"})
    todo_id = create_resp.json()["id"]
    response = client.get(f"/todos/{todo_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Read"


def test_get_todo_not_found_returns_404() -> None:
    """GET /todos/{id} for a non-existent id should return 404."""
    response = client.get("/todos/999")
    assert response.status_code == 404


# -- Update ------------------------------------------------------------------


def test_update_todo() -> None:
    """PUT /todos/{id} should update fields and return the todo."""
    create_resp = client.post("/todos", json={"title": "Old"})
    todo_id = create_resp.json()["id"]
    response = client.put(
        f"/todos/{todo_id}", json={"title": "New", "completed": True}
    )
    assert response.status_code == 200
    body = response.json()
    assert body["title"] == "New"
    assert body["completed"] is True


def test_update_todo_not_found_returns_404() -> None:
    """PUT /todos/{id} for a non-existent id should return 404."""
    response = client.put("/todos/999", json={"title": "X"})
    assert response.status_code == 404


# -- Delete ------------------------------------------------------------------


def test_delete_todo() -> None:
    """DELETE /todos/{id} should return 204 and remove the todo."""
    create_resp = client.post("/todos", json={"title": "Bye"})
    todo_id = create_resp.json()["id"]
    response = client.delete(f"/todos/{todo_id}")
    assert response.status_code == 204
    assert client.get(f"/todos/{todo_id}").status_code == 404


def test_delete_todo_not_found_returns_404() -> None:
    """DELETE /todos/{id} for a non-existent id should return 404."""
    response = client.delete("/todos/999")
    assert response.status_code == 404
