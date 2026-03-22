"""Tests for the FastAPI Todo application.

Uses an in-memory SQLite database (monkeypatched via DATABASE_PATH) to
avoid polluting the real data store.
"""

from __future__ import annotations

import importlib
import os
import tempfile
from typing import Generator

import pytest
from fastapi.testclient import TestClient

import database
import main


@pytest.fixture(autouse=True)
def _use_temp_db(tmp_path: pytest.TempPathFactory) -> Generator[None, None, None]:
    """Redirect the database to a temporary file for every test."""
    db_file = str(tmp_path / "test_todos.db")
    original_path = database.DATABASE_PATH
    database.DATABASE_PATH = db_file
    database.init_db()
    yield
    database.DATABASE_PATH = original_path


@pytest.fixture()
def client() -> TestClient:
    """Return a TestClient that does NOT trigger the lifespan again."""
    return TestClient(main.app, raise_server_exceptions=True)


# ---------------------------------------------------------------------------
# GET /
# ---------------------------------------------------------------------------

class TestServeIndex:
    """Tests for the root HTML endpoint."""

    def test_returns_html(self, client: TestClient) -> None:
        """GET / should return 200 with HTML content."""
        resp = client.get("/")
        assert resp.status_code == 200
        assert "text/html" in resp.headers["content-type"]
        assert "<title>" in resp.text


# ---------------------------------------------------------------------------
# GET /api/todos
# ---------------------------------------------------------------------------

class TestListTodos:
    """Tests for listing todos."""

    def test_empty_list(self, client: TestClient) -> None:
        """An empty database should return an empty list."""
        resp = client.get("/api/todos")
        assert resp.status_code == 200
        assert resp.json() == []

    def test_returns_created_todos(self, client: TestClient) -> None:
        """After creating todos they should appear in the list."""
        client.post("/api/todos", json={"title": "First"})
        client.post("/api/todos", json={"title": "Second"})
        resp = client.get("/api/todos")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 2
        titles = {t["title"] for t in data}
        assert titles == {"First", "Second"}


# ---------------------------------------------------------------------------
# POST /api/todos
# ---------------------------------------------------------------------------

class TestCreateTodo:
    """Tests for creating a todo."""

    def test_create_returns_201(self, client: TestClient) -> None:
        """Creating a todo should return 201 with the new item."""
        resp = client.post("/api/todos", json={"title": "Buy milk"})
        assert resp.status_code == 201
        body = resp.json()
        assert body["title"] == "Buy milk"
        assert body["completed"] is False
        assert "id" in body
        assert "created_at" in body

    def test_create_missing_title_returns_422(self, client: TestClient) -> None:
        """A request without a title should be rejected."""
        resp = client.post("/api/todos", json={})
        assert resp.status_code == 422

    def test_create_empty_title_returns_422(self, client: TestClient) -> None:
        """A request with an empty title should be rejected."""
        resp = client.post("/api/todos", json={"title": ""})
        assert resp.status_code == 422


# ---------------------------------------------------------------------------
# PATCH /api/todos/{id}
# ---------------------------------------------------------------------------

class TestToggleTodo:
    """Tests for toggling the completed status."""

    def test_toggle_sets_completed(self, client: TestClient) -> None:
        """Toggling an incomplete todo should set completed=True."""
        create_resp = client.post("/api/todos", json={"title": "Toggle me"})
        todo_id = create_resp.json()["id"]

        resp = client.patch(f"/api/todos/{todo_id}")
        assert resp.status_code == 200
        assert resp.json()["completed"] is True

    def test_double_toggle_reverts(self, client: TestClient) -> None:
        """Toggling twice should revert to the original state."""
        create_resp = client.post("/api/todos", json={"title": "Flip"})
        todo_id = create_resp.json()["id"]

        client.patch(f"/api/todos/{todo_id}")
        resp = client.patch(f"/api/todos/{todo_id}")
        assert resp.status_code == 200
        assert resp.json()["completed"] is False

    def test_toggle_nonexistent_returns_404(self, client: TestClient) -> None:
        """Toggling a non-existent todo should return 404."""
        resp = client.patch("/api/todos/99999")
        assert resp.status_code == 404
        assert resp.json()["detail"] == "Todo not found"


# ---------------------------------------------------------------------------
# DELETE /api/todos/{id}
# ---------------------------------------------------------------------------

class TestDeleteTodo:
    """Tests for deleting a todo."""

    def test_delete_returns_success_message(self, client: TestClient) -> None:
        """Deleting an existing todo should return a success message."""
        create_resp = client.post("/api/todos", json={"title": "Delete me"})
        todo_id = create_resp.json()["id"]

        resp = client.delete(f"/api/todos/{todo_id}")
        assert resp.status_code == 200
        assert resp.json()["detail"] == "Todo deleted successfully"

    def test_deleted_todo_disappears_from_list(self, client: TestClient) -> None:
        """After deletion the todo should no longer appear in the list."""
        create_resp = client.post("/api/todos", json={"title": "Gone"})
        todo_id = create_resp.json()["id"]

        client.delete(f"/api/todos/{todo_id}")
        todos = client.get("/api/todos").json()
        assert all(t["id"] != todo_id for t in todos)

    def test_delete_nonexistent_returns_404(self, client: TestClient) -> None:
        """Deleting a non-existent todo should return 404."""
        resp = client.delete("/api/todos/99999")
        assert resp.status_code == 404
        assert resp.json()["detail"] == "Todo not found"


# ---------------------------------------------------------------------------
# Response model validation
# ---------------------------------------------------------------------------

class TestResponseModel:
    """Verify that the response body matches the TodoResponse schema."""

    def test_response_has_all_fields(self, client: TestClient) -> None:
        """Every required field must be present in a created todo."""
        resp = client.post("/api/todos", json={"title": "Schema check"})
        body = resp.json()
        assert isinstance(body["id"], int)
        assert isinstance(body["title"], str)
        assert isinstance(body["completed"], bool)
        assert isinstance(body["created_at"], str)
