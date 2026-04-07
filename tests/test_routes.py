"""Tests for the Todo CRUD API endpoints.

Covers all five endpoints with happy-path and error scenarios,
including 404 handling and correct HTTP status codes.
"""

from __future__ import annotations

from fastapi import status
from fastapi.testclient import TestClient

from app.main import app
from app.storage import storage

client = TestClient(app)


def _reset_storage() -> None:
    """Clear the in-memory store and reset the ID counter."""
    storage._todos.clear()
    storage._next_id = 1


# -- GET /todos -------------------------------------------------------------


def test_list_todos_empty() -> None:
    """GET /todos returns an empty list when no todos exist."""
    _reset_storage()
    response = client.get("/todos")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


def test_list_todos_returns_all() -> None:
    """GET /todos returns all created todos."""
    _reset_storage()
    client.post("/todos", json={"title": "First"})
    client.post("/todos", json={"title": "Second"})

    response = client.get("/todos")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 2
    titles = {item["title"] for item in data}
    assert titles == {"First", "Second"}


# -- GET /todos/{todo_id} ---------------------------------------------------


def test_get_todo_existing() -> None:
    """GET /todos/{id} returns the correct todo."""
    _reset_storage()
    create_resp = client.post("/todos", json={"title": "Test"})
    todo_id = create_resp.json()["id"]

    response = client.get(f"/todos/{todo_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["title"] == "Test"
    assert response.json()["id"] == todo_id


def test_get_todo_not_found() -> None:
    """GET /todos/{id} returns 404 for a non-existent id."""
    _reset_storage()
    response = client.get("/todos/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Todo not found"


# -- POST /todos ------------------------------------------------------------


def test_create_todo_minimal() -> None:
    """POST /todos with only a title returns 201 and correct defaults."""
    _reset_storage()
    response = client.post("/todos", json={"title": "Buy milk"})
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["title"] == "Buy milk"
    assert data["description"] is None
    assert data["completed"] is False
    assert "id" in data


def test_create_todo_with_description() -> None:
    """POST /todos with title and description returns both."""
    _reset_storage()
    response = client.post(
        "/todos",
        json={"title": "Read book", "description": "Chapter 3"},
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["title"] == "Read book"
    assert data["description"] == "Chapter 3"


def test_create_todo_empty_title_rejected() -> None:
    """POST /todos with an empty title returns 422 validation error."""
    _reset_storage()
    response = client.post("/todos", json={"title": ""})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_todo_missing_title_rejected() -> None:
    """POST /todos without a title field returns 422 validation error."""
    _reset_storage()
    response = client.post("/todos", json={})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_todo_ids_auto_increment() -> None:
    """Successive POST /todos calls produce incrementing IDs."""
    _reset_storage()
    resp1 = client.post("/todos", json={"title": "A"})
    resp2 = client.post("/todos", json={"title": "B"})
    assert resp1.json()["id"] < resp2.json()["id"]


# -- PUT /todos/{todo_id} ---------------------------------------------------


def test_update_todo_title() -> None:
    """PUT /todos/{id} updates the title and preserves other fields."""
    _reset_storage()
    create_resp = client.post(
        "/todos",
        json={"title": "Old title", "description": "Keep me"},
    )
    todo_id = create_resp.json()["id"]

    response = client.put(
        f"/todos/{todo_id}",
        json={"title": "New title"},
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["title"] == "New title"
    assert data["description"] == "Keep me"
    assert data["completed"] is False


def test_update_todo_completed() -> None:
    """PUT /todos/{id} can toggle the completed flag."""
    _reset_storage()
    create_resp = client.post("/todos", json={"title": "Task"})
    todo_id = create_resp.json()["id"]

    response = client.put(
        f"/todos/{todo_id}",
        json={"completed": True},
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["completed"] is True


def test_update_todo_not_found() -> None:
    """PUT /todos/{id} returns 404 for a non-existent id."""
    _reset_storage()
    response = client.put("/todos/999", json={"title": "Nope"})
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Todo not found"


def test_update_todo_partial_preserves_unset_fields() -> None:
    """PUT /todos/{id} with only description leaves title and completed intact."""
    _reset_storage()
    create_resp = client.post("/todos", json={"title": "Keep"})
    todo_id = create_resp.json()["id"]

    response = client.put(
        f"/todos/{todo_id}",
        json={"description": "Added desc"},
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["title"] == "Keep"
    assert data["description"] == "Added desc"
    assert data["completed"] is False


# -- DELETE /todos/{todo_id} ------------------------------------------------


def test_delete_todo_existing() -> None:
    """DELETE /todos/{id} returns 204 and removes the item."""
    _reset_storage()
    create_resp = client.post("/todos", json={"title": "Delete me"})
    todo_id = create_resp.json()["id"]

    response = client.delete(f"/todos/{todo_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.content == b""

    # Confirm it's gone
    get_resp = client.get(f"/todos/{todo_id}")
    assert get_resp.status_code == status.HTTP_404_NOT_FOUND


def test_delete_todo_not_found() -> None:
    """DELETE /todos/{id} returns 404 for a non-existent id."""
    _reset_storage()
    response = client.delete("/todos/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Todo not found"


def test_delete_todo_twice_returns_404_second_time() -> None:
    """Deleting the same todo twice returns 204 then 404."""
    _reset_storage()
    create_resp = client.post("/todos", json={"title": "Once"})
    todo_id = create_resp.json()["id"]

    first = client.delete(f"/todos/{todo_id}")
    assert first.status_code == status.HTTP_204_NO_CONTENT

    second = client.delete(f"/todos/{todo_id}")
    assert second.status_code == status.HTTP_404_NOT_FOUND
