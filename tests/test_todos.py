"""Tests for the Todo CRUD endpoints.

Ensures that create, list, get, update, and delete operations on
/todos work correctly.
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from main import app
from routes import store

client: TestClient = TestClient(app)


@pytest.fixture(autouse=True)
def _reset_store() -> None:
    """Reset the in-memory store before each test for isolation."""
    store.reset()


# ---- CREATE ----------------------------------------------------------------


def test_create_todo_returns_201() -> None:
    """POST /todos with a valid title must return 201."""
    response = client.post("/todos", json={"title": "Buy milk"})
    assert response.status_code == 201


def test_create_todo_returns_item() -> None:
    """POST /todos must return the created todo with an id."""
    response = client.post("/todos", json={"title": "Buy milk"})
    data = response.json()
    assert data["title"] == "Buy milk"
    assert data["completed"] is False
    assert "id" in data


def test_create_todo_empty_title_returns_422() -> None:
    """POST /todos with an empty title must return 422."""
    response = client.post("/todos", json={"title": ""})
    assert response.status_code == 422


# ---- LIST ------------------------------------------------------------------


def test_list_todos_empty() -> None:
    """GET /todos on an empty store must return an empty list."""
    response = client.get("/todos")
    assert response.status_code == 200
    assert response.json() == []


def test_list_todos_after_create() -> None:
    """GET /todos after creating items must return them all."""
    client.post("/todos", json={"title": "First"})
    client.post("/todos", json={"title": "Second"})
    response = client.get("/todos")
    assert response.status_code == 200
    assert len(response.json()) == 2


# ---- GET -------------------------------------------------------------------


def test_get_todo_by_id() -> None:
    """GET /todos/{id} must return the correct todo."""
    create_resp = client.post("/todos", json={"title": "Test"})
    todo_id = create_resp.json()["id"]
    response = client.get(f"/todos/{todo_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Test"


def test_get_todo_not_found() -> None:
    """GET /todos/{id} for a non-existent id must return 404."""
    response = client.get("/todos/9999")
    assert response.status_code == 404


# ---- UPDATE ----------------------------------------------------------------


def test_update_todo_completed() -> None:
    """PUT /todos/{id} must update the completed field."""
    create_resp = client.post("/todos", json={"title": "Do laundry"})
    todo_id = create_resp.json()["id"]
    response = client.put(f"/todos/{todo_id}", json={"completed": True})
    assert response.status_code == 200
    assert response.json()["completed"] is True


def test_update_todo_not_found() -> None:
    """PUT /todos/{id} for a non-existent id must return 404."""
    response = client.put("/todos/9999", json={"completed": True})
    assert response.status_code == 404


# ---- DELETE ----------------------------------------------------------------


def test_delete_todo() -> None:
    """DELETE /todos/{id} must remove the item and return 200."""
    create_resp = client.post("/todos", json={"title": "Temp"})
    todo_id = create_resp.json()["id"]
    response = client.delete(f"/todos/{todo_id}")
    assert response.status_code == 200
    # Confirm it's gone
    get_resp = client.get(f"/todos/{todo_id}")
    assert get_resp.status_code == 404


def test_delete_todo_not_found() -> None:
    """DELETE /todos/{id} for a non-existent id must return 404."""
    response = client.delete("/todos/9999")
    assert response.status_code == 404
