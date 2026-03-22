"""Tests for the FastAPI application endpoints defined in main.py."""

from __future__ import annotations

import os
import tempfile
from typing import Generator

import pytest
from fastapi.testclient import TestClient

import database


@pytest.fixture(autouse=True)
def _use_temp_db(tmp_path: object) -> Generator[None, None, None]:
    """Redirect the database to a temporary file for each test."""
    fd, db_path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    original_path = database.DATABASE_PATH
    database.DATABASE_PATH = db_path
    database.init_db()
    yield
    database.DATABASE_PATH = original_path
    try:
        os.unlink(db_path)
    except OSError:
        pass


@pytest.fixture()
def client() -> Generator[TestClient, None, None]:
    """Provide a TestClient wired to the FastAPI app."""
    from main import app

    with TestClient(app) as c:
        yield c


# ---------------------------------------------------------------------------
# GET /
# ---------------------------------------------------------------------------


class TestServeFrontend:
    """Tests for the GET / endpoint."""

    def test_returns_html(self, client: TestClient) -> None:
        """GET / should return 200 with HTML content."""
        response = client.get("/")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
        assert "<html" in response.text.lower()


# ---------------------------------------------------------------------------
# GET /api/todos
# ---------------------------------------------------------------------------


class TestListTodos:
    """Tests for the GET /api/todos endpoint."""

    def test_empty_list(self, client: TestClient) -> None:
        """When no todos exist, an empty list should be returned."""
        response = client.get("/api/todos")
        assert response.status_code == 200
        assert response.json() == []

    def test_returns_created_todos(self, client: TestClient) -> None:
        """After creating todos, they should appear in the list."""
        client.post("/api/todos", json={"title": "First"})
        client.post("/api/todos", json={"title": "Second"})
        response = client.get("/api/todos")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        titles = {item["title"] for item in data}
        assert titles == {"First", "Second"}


# ---------------------------------------------------------------------------
# POST /api/todos
# ---------------------------------------------------------------------------


class TestCreateTodo:
    """Tests for the POST /api/todos endpoint."""

    def test_create_success(self, client: TestClient) -> None:
        """A valid title should create a todo and return 201."""
        response = client.post("/api/todos", json={"title": "New todo"})
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "New todo"
        assert data["completed"] is False
        assert "id" in data
        assert "created_at" in data

    def test_create_empty_title_rejected(self, client: TestClient) -> None:
        """An empty title should return 422."""
        response = client.post("/api/todos", json={"title": ""})
        assert response.status_code == 422

    def test_create_missing_title_rejected(self, client: TestClient) -> None:
        """Omitting the title field should return 422."""
        response = client.post("/api/todos", json={})
        assert response.status_code == 422

    def test_create_returns_response_model(self, client: TestClient) -> None:
        """The response should match the TodoResponse schema."""
        response = client.post("/api/todos", json={"title": "Check schema"})
        data = response.json()
        assert isinstance(data["id"], int)
        assert isinstance(data["title"], str)
        assert isinstance(data["completed"], bool)
        assert isinstance(data["created_at"], str)


# ---------------------------------------------------------------------------
# PATCH /api/todos/{id}
# ---------------------------------------------------------------------------


class TestUpdateTodo:
    """Tests for the PATCH /api/todos/{id} endpoint."""

    def test_update_completed_true(self, client: TestClient) -> None:
        """Setting completed to True should update the todo."""
        create_resp = client.post("/api/todos", json={"title": "Update me"})
        todo_id = create_resp.json()["id"]

        response = client.patch(
            f"/api/todos/{todo_id}", json={"completed": True}
        )
        assert response.status_code == 200
        assert response.json()["completed"] is True

    def test_update_completed_false(self, client: TestClient) -> None:
        """Setting completed to False should update the todo."""
        create_resp = client.post("/api/todos", json={"title": "Toggle me"})
        todo_id = create_resp.json()["id"]

        # First set to True
        client.patch(f"/api/todos/{todo_id}", json={"completed": True})
        # Then back to False
        response = client.patch(
            f"/api/todos/{todo_id}", json={"completed": False}
        )
        assert response.status_code == 200
        assert response.json()["completed"] is False

    def test_update_nonexistent_returns_404(self, client: TestClient) -> None:
        """Updating a non-existent todo should return 404."""
        response = client.patch(
            "/api/todos/99999", json={"completed": True}
        )
        assert response.status_code == 404
        assert response.json()["detail"] == "Todo not found"

    def test_update_missing_body_returns_422(self, client: TestClient) -> None:
        """Omitting the request body should return 422."""
        create_resp = client.post("/api/todos", json={"title": "No body"})
        todo_id = create_resp.json()["id"]
        response = client.patch(f"/api/todos/{todo_id}")
        assert response.status_code == 422


# ---------------------------------------------------------------------------
# DELETE /api/todos/{id}
# ---------------------------------------------------------------------------


class TestDeleteTodo:
    """Tests for the DELETE /api/todos/{id} endpoint."""

    def test_delete_success(self, client: TestClient) -> None:
        """Deleting an existing todo should return 200 with a message."""
        create_resp = client.post("/api/todos", json={"title": "Delete me"})
        todo_id = create_resp.json()["id"]

        response = client.delete(f"/api/todos/{todo_id}")
        assert response.status_code == 200
        assert response.json()["detail"] == "Todo deleted successfully"

    def test_delete_removes_from_list(self, client: TestClient) -> None:
        """After deletion, the todo should no longer appear in the list."""
        create_resp = client.post("/api/todos", json={"title": "Ephemeral"})
        todo_id = create_resp.json()["id"]

        client.delete(f"/api/todos/{todo_id}")

        list_resp = client.get("/api/todos")
        ids = [item["id"] for item in list_resp.json()]
        assert todo_id not in ids

    def test_delete_nonexistent_returns_404(self, client: TestClient) -> None:
        """Deleting a non-existent todo should return 404."""
        response = client.delete("/api/todos/99999")
        assert response.status_code == 404
        assert response.json()["detail"] == "Todo not found"

    def test_double_delete_returns_404(self, client: TestClient) -> None:
        """Deleting the same todo twice should return 404 on the second call."""
        create_resp = client.post("/api/todos", json={"title": "Once only"})
        todo_id = create_resp.json()["id"]

        first = client.delete(f"/api/todos/{todo_id}")
        assert first.status_code == 200

        second = client.delete(f"/api/todos/{todo_id}")
        assert second.status_code == 404
