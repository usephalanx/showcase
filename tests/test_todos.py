"""Tests for the Todo CRUD API endpoints.

Uses FastAPI's TestClient against the main app instance.
Each test resets the in-memory store to ensure isolation.
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from main import app
from routes import store


@pytest.fixture(autouse=True)
def _reset_store() -> None:
    """Reset the in-memory store before every test."""
    store.reset()


@pytest.fixture()
def client() -> TestClient:
    """Return a TestClient bound to the FastAPI app."""
    return TestClient(app)


# ---- POST /todos -----------------------------------------------------------


def test_create_todo(client: TestClient) -> None:
    """POST /todos should create and return a new todo with status 201."""
    response = client.post("/todos", json={"title": "Buy milk"})
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Buy milk"
    assert data["description"] is None
    assert data["completed"] is False
    assert "created_at" in data


def test_create_todo_with_description(client: TestClient) -> None:
    """POST /todos with description should persist it."""
    response = client.post(
        "/todos", json={"title": "Read book", "description": "Chapter 3"}
    )
    assert response.status_code == 201
    assert response.json()["description"] == "Chapter 3"


def test_create_todo_with_completed(client: TestClient) -> None:
    """POST /todos with completed=True should persist it."""
    response = client.post(
        "/todos", json={"title": "Done task", "completed": True}
    )
    assert response.status_code == 201
    assert response.json()["completed"] is True


def test_create_todo_missing_title(client: TestClient) -> None:
    """POST /todos without title should return 422."""
    response = client.post("/todos", json={})
    assert response.status_code == 422


def test_create_todo_empty_title(client: TestClient) -> None:
    """POST /todos with empty title should return 422."""
    response = client.post("/todos", json={"title": ""})
    assert response.status_code == 422


# ---- GET /todos ------------------------------------------------------------


def test_list_todos_empty(client: TestClient) -> None:
    """GET /todos on an empty store should return an empty list."""
    response = client.get("/todos")
    assert response.status_code == 200
    assert response.json() == []


def test_list_todos(client: TestClient) -> None:
    """GET /todos should return all created todos."""
    client.post("/todos", json={"title": "First"})
    client.post("/todos", json={"title": "Second"})
    response = client.get("/todos")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "First"
    assert data[1]["title"] == "Second"


# ---- GET /todos/{id} -------------------------------------------------------


def test_get_todo(client: TestClient) -> None:
    """GET /todos/{id} should return the correct todo."""
    create_resp = client.post("/todos", json={"title": "Test"})
    todo_id = create_resp.json()["id"]
    response = client.get(f"/todos/{todo_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Test"


def test_get_todo_not_found(client: TestClient) -> None:
    """GET /todos/{id} for a non-existent id should return 404."""
    response = client.get("/todos/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Todo not found"


# ---- PUT /todos/{id} -------------------------------------------------------


def test_update_todo_title(client: TestClient) -> None:
    """PUT /todos/{id} should update the title."""
    create_resp = client.post("/todos", json={"title": "Old"})
    todo_id = create_resp.json()["id"]
    response = client.put(f"/todos/{todo_id}", json={"title": "New"})
    assert response.status_code == 200
    assert response.json()["title"] == "New"


def test_update_todo_completed(client: TestClient) -> None:
    """PUT /todos/{id} should update the completed status."""
    create_resp = client.post("/todos", json={"title": "Task"})
    todo_id = create_resp.json()["id"]
    response = client.put(f"/todos/{todo_id}", json={"completed": True})
    assert response.status_code == 200
    assert response.json()["completed"] is True


def test_update_todo_description(client: TestClient) -> None:
    """PUT /todos/{id} should update the description."""
    create_resp = client.post("/todos", json={"title": "Task"})
    todo_id = create_resp.json()["id"]
    response = client.put(
        f"/todos/{todo_id}", json={"description": "Details"}
    )
    assert response.status_code == 200
    assert response.json()["description"] == "Details"


def test_update_todo_not_found(client: TestClient) -> None:
    """PUT /todos/{id} for a non-existent id should return 404."""
    response = client.put("/todos/999", json={"title": "Nope"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Todo not found"


# ---- DELETE /todos/{id} ----------------------------------------------------


def test_delete_todo(client: TestClient) -> None:
    """DELETE /todos/{id} should remove the todo and return success."""
    create_resp = client.post("/todos", json={"title": "Bye"})
    todo_id = create_resp.json()["id"]
    response = client.delete(f"/todos/{todo_id}")
    assert response.status_code == 200
    assert response.json()["detail"] == "Todo deleted successfully"

    # Confirm it is gone
    get_resp = client.get(f"/todos/{todo_id}")
    assert get_resp.status_code == 404


def test_delete_todo_not_found(client: TestClient) -> None:
    """DELETE /todos/{id} for a non-existent id should return 404."""
    response = client.delete("/todos/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Todo not found"


# ---- ID auto-increment -----------------------------------------------------


def test_auto_increment_ids(client: TestClient) -> None:
    """Consecutive creates should yield incrementing IDs."""
    r1 = client.post("/todos", json={"title": "A"})
    r2 = client.post("/todos", json={"title": "B"})
    assert r1.json()["id"] == 1
    assert r2.json()["id"] == 2
