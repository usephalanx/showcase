"""Comprehensive tests for the Todo CRUD API routes.

Uses the FastAPI TestClient (backed by httpx) to exercise every endpoint,
including happy paths and error cases (404s, validation errors).
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
    """Return a TestClient bound to the FastAPI application."""
    return TestClient(app)


# ── Root endpoint ─────────────────────────────────────────────────────────


class TestRoot:
    """Tests for GET /."""

    def test_root_returns_welcome_message(self, client: TestClient) -> None:
        """GET / should return the welcome JSON."""
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Todo API is running"}


# ── POST /todos ───────────────────────────────────────────────────────────


class TestCreateTodo:
    """Tests for POST /todos."""

    def test_create_todo_minimal(self, client: TestClient) -> None:
        """Create a todo with only a title."""
        response = client.post("/todos", json={"title": "Buy milk"})
        assert response.status_code == 201
        body = response.json()
        assert body["id"] == 1
        assert body["title"] == "Buy milk"
        assert body["description"] is None
        assert body["completed"] is False
        assert "created_at" in body

    def test_create_todo_with_all_fields(self, client: TestClient) -> None:
        """Create a todo supplying every field."""
        payload = {
            "title": "Learn FastAPI",
            "description": "Work through the tutorial",
            "completed": True,
        }
        response = client.post("/todos", json=payload)
        assert response.status_code == 201
        body = response.json()
        assert body["title"] == "Learn FastAPI"
        assert body["description"] == "Work through the tutorial"
        assert body["completed"] is True

    def test_create_todo_auto_increments_id(self, client: TestClient) -> None:
        """IDs should increase monotonically."""
        r1 = client.post("/todos", json={"title": "First"})
        r2 = client.post("/todos", json={"title": "Second"})
        assert r1.json()["id"] == 1
        assert r2.json()["id"] == 2

    def test_create_todo_empty_title_returns_422(self, client: TestClient) -> None:
        """An empty title should be rejected by Pydantic validation."""
        response = client.post("/todos", json={"title": ""})
        assert response.status_code == 422

    def test_create_todo_missing_title_returns_422(self, client: TestClient) -> None:
        """A missing title should be rejected."""
        response = client.post("/todos", json={})
        assert response.status_code == 422


# ── GET /todos ────────────────────────────────────────────────────────────


class TestListTodos:
    """Tests for GET /todos."""

    def test_list_empty(self, client: TestClient) -> None:
        """An empty store should return an empty list."""
        response = client.get("/todos")
        assert response.status_code == 200
        assert response.json() == []

    def test_list_multiple(self, client: TestClient) -> None:
        """All created todos should appear in the list."""
        client.post("/todos", json={"title": "A"})
        client.post("/todos", json={"title": "B"})
        client.post("/todos", json={"title": "C"})

        response = client.get("/todos")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        titles = {t["title"] for t in data}
        assert titles == {"A", "B", "C"}


# ── GET /todos/{todo_id} ──────────────────────────────────────────────────


class TestGetTodo:
    """Tests for GET /todos/{todo_id}."""

    def test_get_existing(self, client: TestClient) -> None:
        """Retrieve a todo that exists."""
        create_resp = client.post("/todos", json={"title": "Test"})
        todo_id = create_resp.json()["id"]

        response = client.get(f"/todos/{todo_id}")
        assert response.status_code == 200
        assert response.json()["id"] == todo_id
        assert response.json()["title"] == "Test"

    def test_get_nonexistent_returns_404(self, client: TestClient) -> None:
        """A missing todo should yield 404."""
        response = client.get("/todos/9999")
        assert response.status_code == 404
        assert response.json()["detail"] == "Todo not found"


# ── PUT /todos/{todo_id} ──────────────────────────────────────────────────


class TestUpdateTodo:
    """Tests for PUT /todos/{todo_id}."""

    def test_update_title(self, client: TestClient) -> None:
        """Updating only the title should leave other fields unchanged."""
        create_resp = client.post("/todos", json={"title": "Old"})
        todo_id = create_resp.json()["id"]

        response = client.put(f"/todos/{todo_id}", json={"title": "New"})
        assert response.status_code == 200
        body = response.json()
        assert body["title"] == "New"
        assert body["completed"] is False  # unchanged

    def test_update_completed(self, client: TestClient) -> None:
        """Toggle the completed flag."""
        create_resp = client.post("/todos", json={"title": "Do it"})
        todo_id = create_resp.json()["id"]

        response = client.put(f"/todos/{todo_id}", json={"completed": True})
        assert response.status_code == 200
        assert response.json()["completed"] is True

    def test_update_description(self, client: TestClient) -> None:
        """Set the description on an existing todo."""
        create_resp = client.post("/todos", json={"title": "Stuff"})
        todo_id = create_resp.json()["id"]

        response = client.put(
            f"/todos/{todo_id}", json={"description": "More details"}
        )
        assert response.status_code == 200
        assert response.json()["description"] == "More details"

    def test_update_multiple_fields(self, client: TestClient) -> None:
        """Update several fields at once."""
        create_resp = client.post("/todos", json={"title": "Original"})
        todo_id = create_resp.json()["id"]

        payload = {"title": "Updated", "description": "Desc", "completed": True}
        response = client.put(f"/todos/{todo_id}", json=payload)
        assert response.status_code == 200
        body = response.json()
        assert body["title"] == "Updated"
        assert body["description"] == "Desc"
        assert body["completed"] is True

    def test_update_nonexistent_returns_404(self, client: TestClient) -> None:
        """Updating a missing todo should yield 404."""
        response = client.put("/todos/9999", json={"title": "Nope"})
        assert response.status_code == 404
        assert response.json()["detail"] == "Todo not found"

    def test_update_no_fields_keeps_original(self, client: TestClient) -> None:
        """Sending an empty update body should leave the todo unchanged."""
        create_resp = client.post(
            "/todos",
            json={"title": "Keep", "description": "Same", "completed": False},
        )
        todo_id = create_resp.json()["id"]

        response = client.put(f"/todos/{todo_id}", json={})
        assert response.status_code == 200
        body = response.json()
        assert body["title"] == "Keep"
        assert body["description"] == "Same"
        assert body["completed"] is False


# ── DELETE /todos/{todo_id} ───────────────────────────────────────────────


class TestDeleteTodo:
    """Tests for DELETE /todos/{todo_id}."""

    def test_delete_existing(self, client: TestClient) -> None:
        """Deleting an existing todo should return 204 with no body."""
        create_resp = client.post("/todos", json={"title": "Remove me"})
        todo_id = create_resp.json()["id"]

        response = client.delete(f"/todos/{todo_id}")
        assert response.status_code == 204
        assert response.content == b""

        # Confirm it's actually gone
        get_resp = client.get(f"/todos/{todo_id}")
        assert get_resp.status_code == 404

    def test_delete_nonexistent_returns_404(self, client: TestClient) -> None:
        """Deleting a missing todo should yield 404."""
        response = client.delete("/todos/9999")
        assert response.status_code == 404
        assert response.json()["detail"] == "Todo not found"

    def test_delete_removes_from_list(self, client: TestClient) -> None:
        """After deletion, the todo should no longer appear in the list."""
        client.post("/todos", json={"title": "Stay"})
        create_resp = client.post("/todos", json={"title": "Go away"})
        todo_id = create_resp.json()["id"]

        client.delete(f"/todos/{todo_id}")

        list_resp = client.get("/todos")
        ids = [t["id"] for t in list_resp.json()]
        assert todo_id not in ids
        assert len(list_resp.json()) == 1


# ── Integration / edge-case tests ─────────────────────────────────────────


class TestIntegration:
    """End-to-end integration and edge-case tests."""

    def test_full_lifecycle(self, client: TestClient) -> None:
        """Create → read → update → read → delete → confirm gone."""
        # Create
        r = client.post("/todos", json={"title": "Lifecycle"})
        assert r.status_code == 201
        todo_id = r.json()["id"]

        # Read
        r = client.get(f"/todos/{todo_id}")
        assert r.status_code == 200
        assert r.json()["title"] == "Lifecycle"

        # Update
        r = client.put(f"/todos/{todo_id}", json={"completed": True})
        assert r.status_code == 200
        assert r.json()["completed"] is True

        # Read again to confirm persistence
        r = client.get(f"/todos/{todo_id}")
        assert r.json()["completed"] is True

        # Delete
        r = client.delete(f"/todos/{todo_id}")
        assert r.status_code == 204

        # Confirm gone
        r = client.get(f"/todos/{todo_id}")
        assert r.status_code == 404

    def test_create_after_delete_uses_next_id(self, client: TestClient) -> None:
        """IDs should never be reused — counter continues after deletion."""
        r1 = client.post("/todos", json={"title": "First"})
        first_id = r1.json()["id"]

        client.delete(f"/todos/{first_id}")

        r2 = client.post("/todos", json={"title": "Second"})
        assert r2.json()["id"] == first_id + 1

    def test_double_delete_returns_404(self, client: TestClient) -> None:
        """Deleting the same todo twice should yield 404 on the second call."""
        r = client.post("/todos", json={"title": "Twice"})
        todo_id = r.json()["id"]

        first_delete = client.delete(f"/todos/{todo_id}")
        assert first_delete.status_code == 204

        second_delete = client.delete(f"/todos/{todo_id}")
        assert second_delete.status_code == 404
