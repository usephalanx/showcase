"""Tests for FastAPI route handlers (routes.py) via the main app.

Covers: CRUD endpoints (POST, GET, PUT, DELETE /todos), error handling
(404 for missing items), and full integration flows.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Dict

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from main import app
from routes import store


@pytest.fixture(autouse=True)
def _reset_store() -> None:
    """Reset the in-memory store before each test."""
    store.reset()


@pytest.fixture()
def client() -> TestClient:
    """Return a TestClient for the FastAPI application."""
    return TestClient(app)


def _create_todo(
    client: TestClient,
    title: str = "Test Todo",
    description: str | None = None,
    completed: bool = False,
) -> Dict[str, Any]:
    """Helper to create a todo and return the response JSON."""
    payload: Dict[str, Any] = {"title": title}
    if description is not None:
        payload["description"] = description
    if completed:
        payload["completed"] = completed
    response = client.post("/todos", json=payload)
    assert response.status_code == 201
    return response.json()


class TestRootEndpoint:
    """Tests for the root endpoint."""

    def test_root_returns_welcome_message(self, client: TestClient) -> None:
        """GET / returns a welcome message."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data


class TestCreateTodo:
    """Tests for POST /todos."""

    def test_create_todo_success(self, client: TestClient) -> None:
        """Creating a todo returns 201 with the new item."""
        response = client.post("/todos", json={"title": "New todo"})
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "New todo"
        assert data["completed"] is False
        assert "id" in data
        assert "created_at" in data

    def test_create_todo_with_description(self, client: TestClient) -> None:
        """Creating a todo with a description includes it in response."""
        data = _create_todo(client, title="Task", description="Details")
        assert data["description"] == "Details"

    def test_create_todo_with_completed_true(self, client: TestClient) -> None:
        """Creating a todo with completed=true sets it accordingly."""
        data = _create_todo(client, title="Done", completed=True)
        assert data["completed"] is True

    def test_create_todo_empty_title_rejected(self, client: TestClient) -> None:
        """An empty title returns 422."""
        response = client.post("/todos", json={"title": ""})
        assert response.status_code == 422

    def test_create_todo_missing_title_rejected(self, client: TestClient) -> None:
        """A missing title returns 422."""
        response = client.post("/todos", json={})
        assert response.status_code == 422


class TestListTodos:
    """Tests for GET /todos."""

    def test_list_empty(self, client: TestClient) -> None:
        """An empty store returns an empty list."""
        response = client.get("/todos")
        assert response.status_code == 200
        assert response.json() == []

    def test_list_returns_created_items(self, client: TestClient) -> None:
        """Created items appear in the list."""
        _create_todo(client, title="A")
        _create_todo(client, title="B")
        response = client.get("/todos")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

    def test_list_returns_list_of_dicts(self, client: TestClient) -> None:
        """Each item is a dict with expected keys."""
        _create_todo(client, title="Task")
        response = client.get("/todos")
        data = response.json()
        assert isinstance(data, list)
        item = data[0]
        assert "id" in item
        assert "title" in item
        assert "completed" in item


class TestGetTodo:
    """Tests for GET /todos/{todo_id}."""

    def test_get_existing_todo(self, client: TestClient) -> None:
        """Fetching an existing todo returns it."""
        created = _create_todo(client, title="Fetch me")
        response = client.get(f"/todos/{created['id']}")
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Fetch me"

    def test_get_nonexistent_todo(self, client: TestClient) -> None:
        """Fetching a non-existent todo returns 404."""
        response = client.get("/todos/99999")
        assert response.status_code == 404
        assert response.json()["detail"] == "Todo not found"


class TestUpdateTodo:
    """Tests for PUT /todos/{todo_id}."""

    def test_update_title(self, client: TestClient) -> None:
        """Updating a todo's title changes it."""
        created = _create_todo(client, title="Old")
        response = client.put(
            f"/todos/{created['id']}", json={"title": "New"}
        )
        assert response.status_code == 200
        assert response.json()["title"] == "New"

    def test_update_completed(self, client: TestClient) -> None:
        """Toggling completed status works."""
        created = _create_todo(client, title="Toggle")
        response = client.put(
            f"/todos/{created['id']}", json={"completed": True}
        )
        assert response.status_code == 200
        assert response.json()["completed"] is True

    def test_update_preserves_unchanged_fields(self, client: TestClient) -> None:
        """Fields not in the update payload remain unchanged."""
        created = _create_todo(client, title="Keep", description="Stay")
        response = client.put(
            f"/todos/{created['id']}", json={"completed": True}
        )
        data = response.json()
        assert data["title"] == "Keep"
        assert data["description"] == "Stay"

    def test_update_nonexistent_todo(self, client: TestClient) -> None:
        """Updating a non-existent todo returns 404."""
        response = client.put("/todos/99999", json={"title": "Nope"})
        assert response.status_code == 404


class TestDeleteTodo:
    """Tests for DELETE /todos/{todo_id}."""

    def test_delete_existing_todo(self, client: TestClient) -> None:
        """Deleting an existing todo returns 200."""
        created = _create_todo(client, title="Delete me")
        response = client.delete(f"/todos/{created['id']}")
        assert response.status_code == 200
        assert "deleted" in response.json()["detail"].lower()

    def test_delete_removes_todo(self, client: TestClient) -> None:
        """After deletion the todo is no longer accessible."""
        created = _create_todo(client, title="Gone")
        client.delete(f"/todos/{created['id']}")
        response = client.get(f"/todos/{created['id']}")
        assert response.status_code == 404

    def test_delete_nonexistent_todo(self, client: TestClient) -> None:
        """Deleting a non-existent todo returns 404."""
        response = client.delete("/todos/99999")
        assert response.status_code == 404

    def test_delete_does_not_affect_other_todos(self, client: TestClient) -> None:
        """Deleting one todo leaves others intact."""
        t1 = _create_todo(client, title="Stay")
        t2 = _create_todo(client, title="Go")
        client.delete(f"/todos/{t2['id']}")
        response = client.get("/todos")
        data = response.json()
        assert len(data) == 1
        assert data[0]["id"] == t1["id"]


class TestIntegrationFlow:
    """Full integration tests exercising multiple operations in sequence."""

    def test_full_crud_lifecycle(self, client: TestClient) -> None:
        """Create, read, update, delete a todo in a single flow."""
        # Create
        created = _create_todo(client, title="Lifecycle")
        todo_id = created["id"]
        assert created["completed"] is False

        # Read
        read_resp = client.get(f"/todos/{todo_id}")
        assert read_resp.status_code == 200
        assert read_resp.json()["title"] == "Lifecycle"

        # Update
        update_resp = client.put(
            f"/todos/{todo_id}", json={"completed": True}
        )
        assert update_resp.status_code == 200
        assert update_resp.json()["completed"] is True

        # Verify update persisted
        verify_resp = client.get(f"/todos/{todo_id}")
        assert verify_resp.json()["completed"] is True

        # Delete
        del_resp = client.delete(f"/todos/{todo_id}")
        assert del_resp.status_code == 200

        # Verify gone
        gone_resp = client.get(f"/todos/{todo_id}")
        assert gone_resp.status_code == 404

    def test_multiple_todos_isolation(self, client: TestClient) -> None:
        """Operations on one todo do not affect others."""
        t1 = _create_todo(client, title="Alpha")
        t2 = _create_todo(client, title="Beta")
        t3 = _create_todo(client, title="Gamma")

        # Update t2 only
        client.put(f"/todos/{t2['id']}", json={"completed": True})

        # Delete t3 only
        client.delete(f"/todos/{t3['id']}")

        # Verify t1 unchanged
        r1 = client.get(f"/todos/{t1['id']}")
        assert r1.status_code == 200
        assert r1.json()["completed"] is False
        assert r1.json()["title"] == "Alpha"

        # Verify t2 updated
        r2 = client.get(f"/todos/{t2['id']}")
        assert r2.status_code == 200
        assert r2.json()["completed"] is True

        # Verify t3 gone
        r3 = client.get(f"/todos/{t3['id']}")
        assert r3.status_code == 404

        # List should have exactly 2 items
        all_resp = client.get("/todos")
        assert len(all_resp.json()) == 2

    def test_create_many_and_list(self, client: TestClient) -> None:
        """Creating many todos and listing returns them all."""
        for i in range(20):
            _create_todo(client, title=f"Todo {i}")
        response = client.get("/todos")
        assert response.status_code == 200
        assert len(response.json()) == 20
