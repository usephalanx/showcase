"""Tests for the Todo CRUD router."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.storage import storage


@pytest.fixture(autouse=True)
def _clear_storage() -> None:
    """Reset in-memory storage before each test."""
    storage.clear()


@pytest.fixture()
def client() -> TestClient:
    """Return a TestClient wired to the FastAPI application."""
    return TestClient(app)


# -- POST /todos -------------------------------------------------------------


def test_create_todo(client: TestClient) -> None:
    """POST /todos should create a todo and return 201."""
    response = client.post("/todos", json={"title": "Buy milk"})
    assert response.status_code == 201
    body = response.json()
    assert body["title"] == "Buy milk"
    assert body["description"] == ""
    assert body["completed"] is False
    assert "id" in body


def test_create_todo_with_description(client: TestClient) -> None:
    """POST /todos should accept an optional description."""
    response = client.post(
        "/todos",
        json={"title": "Read book", "description": "Chapter 3"},
    )
    assert response.status_code == 201
    assert response.json()["description"] == "Chapter 3"


def test_create_todo_missing_title_returns_422(client: TestClient) -> None:
    """POST /todos with no title should return 422."""
    response = client.post("/todos", json={})
    assert response.status_code == 422


def test_create_todo_empty_title_returns_422(client: TestClient) -> None:
    """POST /todos with an empty title should return 422."""
    response = client.post("/todos", json={"title": ""})
    assert response.status_code == 422


# -- GET /todos --------------------------------------------------------------


def test_list_todos_empty(client: TestClient) -> None:
    """GET /todos should return an empty list when no todos exist."""
    response = client.get("/todos")
    assert response.status_code == 200
    assert response.json() == []


def test_list_todos(client: TestClient) -> None:
    """GET /todos should return all created todos."""
    client.post("/todos", json={"title": "A"})
    client.post("/todos", json={"title": "B"})
    response = client.get("/todos")
    assert response.status_code == 200
    titles = {t["title"] for t in response.json()}
    assert titles == {"A", "B"}


# -- GET /todos/{id} ---------------------------------------------------------


def test_get_todo_by_id(client: TestClient) -> None:
    """GET /todos/{id} should return the matching todo."""
    create_resp = client.post("/todos", json={"title": "Laundry"})
    todo_id = create_resp.json()["id"]
    response = client.get(f"/todos/{todo_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Laundry"


def test_get_todo_not_found_returns_404(client: TestClient) -> None:
    """GET /todos/{id} should return 404 for a non-existent id."""
    response = client.get("/todos/9999")
    assert response.status_code == 404


# -- PUT /todos/{id} ---------------------------------------------------------


def test_update_todo(client: TestClient) -> None:
    """PUT /todos/{id} should update and return the todo."""
    create_resp = client.post("/todos", json={"title": "Old"})
    todo_id = create_resp.json()["id"]
    response = client.put(
        f"/todos/{todo_id}",
        json={"title": "New", "completed": True},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["title"] == "New"
    assert body["completed"] is True


def test_update_todo_partial(client: TestClient) -> None:
    """PUT /todos/{id} with partial payload should only update provided fields."""
    create_resp = client.post("/todos", json={"title": "Keep", "description": "Original"})
    todo_id = create_resp.json()["id"]
    response = client.put(f"/todos/{todo_id}", json={"completed": True})
    assert response.status_code == 200
    body = response.json()
    assert body["title"] == "Keep"
    assert body["description"] == "Original"
    assert body["completed"] is True


def test_update_todo_not_found_returns_404(client: TestClient) -> None:
    """PUT /todos/{id} should return 404 for a non-existent id."""
    response = client.put("/todos/9999", json={"title": "Nope"})
    assert response.status_code == 404


# -- DELETE /todos/{id} ------------------------------------------------------


def test_delete_todo(client: TestClient) -> None:
    """DELETE /todos/{id} should return 204 and remove the todo."""
    create_resp = client.post("/todos", json={"title": "Gone"})
    todo_id = create_resp.json()["id"]
    response = client.delete(f"/todos/{todo_id}")
    assert response.status_code == 204
    assert response.content == b""
    # Confirm it's actually gone
    get_resp = client.get(f"/todos/{todo_id}")
    assert get_resp.status_code == 404


def test_delete_todo_not_found_returns_404(client: TestClient) -> None:
    """DELETE /todos/{id} should return 404 for a non-existent id."""
    response = client.delete("/todos/9999")
    assert response.status_code == 404


# -- Health check ------------------------------------------------------------


def test_health_check(client: TestClient) -> None:
    """GET /health should return 200 with status ok."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
