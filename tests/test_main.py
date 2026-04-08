"""Tests for the main FastAPI application entry point.

Covers:
- The root endpoint returns the expected welcome message.
- The todo router is correctly mounted (basic smoke tests).
- CRUD lifecycle through the API.
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


# ------------------------------------------------------------------
# Root endpoint
# ------------------------------------------------------------------


class TestRootEndpoint:
    """Tests for GET /."""

    def test_root_returns_200(self, client: TestClient) -> None:
        """GET / should return 200."""
        response = client.get("/")
        assert response.status_code == 200

    def test_root_message(self, client: TestClient) -> None:
        """GET / should return the expected JSON message."""
        response = client.get("/")
        assert response.json() == {"message": "Todo API is running"}


# ------------------------------------------------------------------
# Create todo
# ------------------------------------------------------------------


class TestCreateTodo:
    """Tests for POST /todos."""

    def test_create_returns_201(self, client: TestClient) -> None:
        """POST /todos should return 201 on success."""
        response = client.post("/todos", json={"title": "Buy milk"})
        assert response.status_code == 201

    def test_create_returns_todo(self, client: TestClient) -> None:
        """POST /todos should return the created todo with an id."""
        response = client.post(
            "/todos", json={"title": "Walk the dog", "description": "In the park"}
        )
        data = response.json()
        assert data["id"] == 1
        assert data["title"] == "Walk the dog"
        assert data["description"] == "In the park"
        assert data["completed"] is False
        assert "created_at" in data

    def test_create_without_title_returns_422(self, client: TestClient) -> None:
        """POST /todos with missing title should return 422."""
        response = client.post("/todos", json={})
        assert response.status_code == 422

    def test_create_with_empty_title_returns_422(self, client: TestClient) -> None:
        """POST /todos with an empty title string should return 422."""
        response = client.post("/todos", json={"title": ""})
        assert response.status_code == 422


# ------------------------------------------------------------------
# List todos
# ------------------------------------------------------------------


class TestListTodos:
    """Tests for GET /todos."""

    def test_list_empty(self, client: TestClient) -> None:
        """GET /todos should return an empty list when no todos exist."""
        response = client.get("/todos")
        assert response.status_code == 200
        assert response.json() == []

    def test_list_after_create(self, client: TestClient) -> None:
        """GET /todos should include todos that were previously created."""
        client.post("/todos", json={"title": "First"})
        client.post("/todos", json={"title": "Second"})
        response = client.get("/todos")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["title"] == "First"
        assert data[1]["title"] == "Second"


# ------------------------------------------------------------------
# Get single todo
# ------------------------------------------------------------------


class TestGetTodo:
    """Tests for GET /todos/{todo_id}."""

    def test_get_existing(self, client: TestClient) -> None:
        """GET /todos/{id} should return the todo when it exists."""
        client.post("/todos", json={"title": "Test"})
        response = client.get("/todos/1")
        assert response.status_code == 200
        assert response.json()["title"] == "Test"

    def test_get_not_found(self, client: TestClient) -> None:
        """GET /todos/{id} should return 404 for a non-existent id."""
        response = client.get("/todos/999")
        assert response.status_code == 404
        assert response.json()["detail"] == "Todo not found"


# ------------------------------------------------------------------
# Update todo
# ------------------------------------------------------------------


class TestUpdateTodo:
    """Tests for PUT /todos/{todo_id}."""

    def test_update_title(self, client: TestClient) -> None:
        """PUT /todos/{id} should update the title."""
        client.post("/todos", json={"title": "Old title"})
        response = client.put("/todos/1", json={"title": "New title"})
        assert response.status_code == 200
        assert response.json()["title"] == "New title"

    def test_update_completed(self, client: TestClient) -> None:
        """PUT /todos/{id} should update the completed flag."""
        client.post("/todos", json={"title": "Task"})
        response = client.put("/todos/1", json={"completed": True})
        assert response.status_code == 200
        assert response.json()["completed"] is True

    def test_update_description(self, client: TestClient) -> None:
        """PUT /todos/{id} should update the description."""
        client.post("/todos", json={"title": "Task"})
        response = client.put("/todos/1", json={"description": "Details"})
        assert response.status_code == 200
        assert response.json()["description"] == "Details"

    def test_update_not_found(self, client: TestClient) -> None:
        """PUT /todos/{id} should return 404 for a non-existent id."""
        response = client.put("/todos/999", json={"title": "Nope"})
        assert response.status_code == 404


# ------------------------------------------------------------------
# Delete todo
# ------------------------------------------------------------------


class TestDeleteTodo:
    """Tests for DELETE /todos/{todo_id}."""

    def test_delete_existing(self, client: TestClient) -> None:
        """DELETE /todos/{id} should return 204 when the todo exists."""
        client.post("/todos", json={"title": "To remove"})
        response = client.delete("/todos/1")
        assert response.status_code == 204

    def test_delete_removes_todo(self, client: TestClient) -> None:
        """After DELETE, GET should return 404 for the same id."""
        client.post("/todos", json={"title": "To remove"})
        client.delete("/todos/1")
        response = client.get("/todos/1")
        assert response.status_code == 404

    def test_delete_not_found(self, client: TestClient) -> None:
        """DELETE /todos/{id} should return 404 for a non-existent id."""
        response = client.delete("/todos/999")
        assert response.status_code == 404


# ------------------------------------------------------------------
# Full lifecycle
# ------------------------------------------------------------------


class TestLifecycle:
    """End-to-end CRUD lifecycle test."""

    def test_full_crud_cycle(self, client: TestClient) -> None:
        """Create, read, update, and delete a todo through the API."""
        # Create
        create_resp = client.post(
            "/todos", json={"title": "Lifecycle", "description": "Full test"}
        )
        assert create_resp.status_code == 201
        todo_id = create_resp.json()["id"]

        # Read
        get_resp = client.get(f"/todos/{todo_id}")
        assert get_resp.status_code == 200
        assert get_resp.json()["title"] == "Lifecycle"

        # Update
        put_resp = client.put(
            f"/todos/{todo_id}", json={"completed": True, "title": "Done"}
        )
        assert put_resp.status_code == 200
        assert put_resp.json()["completed"] is True
        assert put_resp.json()["title"] == "Done"

        # Delete
        del_resp = client.delete(f"/todos/{todo_id}")
        assert del_resp.status_code == 204

        # Verify gone
        gone_resp = client.get(f"/todos/{todo_id}")
        assert gone_resp.status_code == 404
