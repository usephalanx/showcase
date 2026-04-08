"""Integration tests for the Todo API endpoints."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from main import app
from routes import store


@pytest.fixture(autouse=True)
def _reset_store() -> None:
    """Reset the shared store before each test for isolation."""
    store.reset()


client = TestClient(app)


# ---------------------------------------------------------------------------
# Root
# ---------------------------------------------------------------------------


class TestRoot:
    """Tests for the root endpoint."""

    def test_root_returns_message(self) -> None:
        """GET / should return the welcome message."""
        resp = client.get("/")
        assert resp.status_code == 200
        assert resp.json() == {"message": "Todo API is running"}


# ---------------------------------------------------------------------------
# POST /todos
# ---------------------------------------------------------------------------


class TestCreateTodo:
    """Tests for creating a todo."""

    def test_create_minimal(self) -> None:
        """POST with only a title should succeed with defaults."""
        resp = client.post("/todos", json={"title": "Buy milk"})
        assert resp.status_code == 201
        data = resp.json()
        assert data["title"] == "Buy milk"
        assert data["description"] is None
        assert data["completed"] is False
        assert "id" in data
        assert "created_at" in data

    def test_create_full(self) -> None:
        """POST with all fields should apply them."""
        resp = client.post(
            "/todos",
            json={
                "title": "Deploy",
                "description": "Push to prod",
                "completed": True,
            },
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["title"] == "Deploy"
        assert data["description"] == "Push to prod"
        assert data["completed"] is True

    def test_create_empty_title_rejected(self) -> None:
        """POST with an empty title should return 422."""
        resp = client.post("/todos", json={"title": ""})
        assert resp.status_code == 422

    def test_create_missing_title_rejected(self) -> None:
        """POST without a title should return 422."""
        resp = client.post("/todos", json={})
        assert resp.status_code == 422


# ---------------------------------------------------------------------------
# GET /todos
# ---------------------------------------------------------------------------


class TestListTodos:
    """Tests for listing todos."""

    def test_empty_list(self) -> None:
        """GET /todos on an empty store should return []."""
        resp = client.get("/todos")
        assert resp.status_code == 200
        assert resp.json() == []

    def test_list_multiple(self) -> None:
        """GET /todos should return all created todos."""
        client.post("/todos", json={"title": "A"})
        client.post("/todos", json={"title": "B"})
        resp = client.get("/todos")
        assert resp.status_code == 200
        assert len(resp.json()) == 2


# ---------------------------------------------------------------------------
# GET /todos/{todo_id}
# ---------------------------------------------------------------------------


class TestGetTodo:
    """Tests for retrieving a single todo."""

    def test_get_existing(self) -> None:
        """GET /todos/{id} for a valid id should return the todo."""
        create_resp = client.post("/todos", json={"title": "Find me"})
        todo_id = create_resp.json()["id"]
        resp = client.get(f"/todos/{todo_id}")
        assert resp.status_code == 200
        assert resp.json()["title"] == "Find me"

    def test_get_nonexistent(self) -> None:
        """GET /todos/{id} for an unknown id should return 404."""
        resp = client.get("/todos/999")
        assert resp.status_code == 404
        assert resp.json()["detail"] == "Todo not found"


# ---------------------------------------------------------------------------
# PUT /todos/{todo_id}
# ---------------------------------------------------------------------------


class TestUpdateTodo:
    """Tests for updating a todo."""

    def test_update_title(self) -> None:
        """PUT should update only the supplied field."""
        create_resp = client.post("/todos", json={"title": "Old"})
        todo_id = create_resp.json()["id"]
        resp = client.put(f"/todos/{todo_id}", json={"title": "New"})
        assert resp.status_code == 200
        assert resp.json()["title"] == "New"

    def test_update_completed(self) -> None:
        """PUT should toggle completed status."""
        create_resp = client.post("/todos", json={"title": "Toggle"})
        todo_id = create_resp.json()["id"]
        resp = client.put(f"/todos/{todo_id}", json={"completed": True})
        assert resp.status_code == 200
        assert resp.json()["completed"] is True

    def test_update_nonexistent(self) -> None:
        """PUT on an unknown id should return 404."""
        resp = client.put("/todos/999", json={"title": "Nope"})
        assert resp.status_code == 404


# ---------------------------------------------------------------------------
# DELETE /todos/{todo_id}
# ---------------------------------------------------------------------------


class TestDeleteTodo:
    """Tests for deleting a todo."""

    def test_delete_existing(self) -> None:
        """DELETE on a valid id should succeed."""
        create_resp = client.post("/todos", json={"title": "Delete me"})
        todo_id = create_resp.json()["id"]
        resp = client.delete(f"/todos/{todo_id}")
        assert resp.status_code == 200
        assert resp.json()["detail"] == "Todo deleted successfully"
        # Confirm it's gone
        get_resp = client.get(f"/todos/{todo_id}")
        assert get_resp.status_code == 404

    def test_delete_nonexistent(self) -> None:
        """DELETE on an unknown id should return 404."""
        resp = client.delete("/todos/999")
        assert resp.status_code == 404
