"""Tests for the Todo CRUD API endpoints.

Uses the httpx async client with FastAPI's TestClient pattern to
exercise every endpoint and edge case.
"""

from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app
from app.storage import storage


def _reset_storage() -> None:
    """Clear the storage between tests to ensure isolation."""
    storage.clear()


class TestHealthCheck:
    """Tests for the GET /health endpoint."""

    def test_health_check(self) -> None:
        """GET /health should return 200 with status ok."""
        _reset_storage()
        client = TestClient(app)
        response = client.get("/health")

        assert response.status_code == 200
        assert response.json() == {"status": "ok"}


class TestCreateTodo:
    """Tests for the POST /todos endpoint."""

    def test_create_todo(self) -> None:
        """POST /todos should create a todo and return 201."""
        _reset_storage()
        client = TestClient(app)
        payload = {"title": "Test todo", "description": "A test item"}
        response = client.post("/todos", json=payload)

        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Test todo"
        assert data["description"] == "A test item"
        assert data["completed"] is False
        assert "id" in data

    def test_create_todo_minimal(self) -> None:
        """POST /todos with only title should default description to empty string."""
        _reset_storage()
        client = TestClient(app)
        payload = {"title": "Minimal todo"}
        response = client.post("/todos", json=payload)

        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Minimal todo"
        assert data["description"] == ""

    def test_create_todo_missing_title_returns_422(self) -> None:
        """POST /todos without title should return 422 Unprocessable Entity."""
        _reset_storage()
        client = TestClient(app)
        response = client.post("/todos", json={})

        assert response.status_code == 422

    def test_create_todo_empty_title_returns_422(self) -> None:
        """POST /todos with empty string title should return 422."""
        _reset_storage()
        client = TestClient(app)
        response = client.post("/todos", json={"title": ""})

        assert response.status_code == 422


class TestListTodos:
    """Tests for the GET /todos endpoint."""

    def test_list_todos_empty(self) -> None:
        """GET /todos on empty store should return an empty list."""
        _reset_storage()
        client = TestClient(app)
        response = client.get("/todos")

        assert response.status_code == 200
        assert response.json() == []

    def test_list_todos(self) -> None:
        """GET /todos should return all created todos."""
        _reset_storage()
        client = TestClient(app)
        client.post("/todos", json={"title": "First"})
        client.post("/todos", json={"title": "Second"})

        response = client.get("/todos")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2


class TestGetTodo:
    """Tests for the GET /todos/{id} endpoint."""

    def test_get_todo_by_id(self) -> None:
        """GET /todos/{id} should return the matching todo."""
        _reset_storage()
        client = TestClient(app)
        create_resp = client.post("/todos", json={"title": "Find me"})
        todo_id = create_resp.json()["id"]

        response = client.get(f"/todos/{todo_id}")
        assert response.status_code == 200
        assert response.json()["title"] == "Find me"

    def test_get_todo_not_found_returns_404(self) -> None:
        """GET /todos/{id} for a non-existent id should return 404."""
        _reset_storage()
        client = TestClient(app)
        response = client.get("/todos/9999")

        assert response.status_code == 404
        assert response.json()["detail"] == "Todo not found"


class TestUpdateTodo:
    """Tests for the PUT /todos/{id} endpoint."""

    def test_update_todo(self) -> None:
        """PUT /todos/{id} should update provided fields."""
        _reset_storage()
        client = TestClient(app)
        create_resp = client.post("/todos", json={"title": "Original"})
        todo_id = create_resp.json()["id"]

        response = client.put(
            f"/todos/{todo_id}",
            json={"title": "Updated", "completed": True},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated"
        assert data["completed"] is True

    def test_update_todo_partial(self) -> None:
        """PUT /todos/{id} with partial data should only change provided fields."""
        _reset_storage()
        client = TestClient(app)
        create_resp = client.post(
            "/todos",
            json={"title": "Original", "description": "Keep me"},
        )
        todo_id = create_resp.json()["id"]

        response = client.put(
            f"/todos/{todo_id}",
            json={"completed": True},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Original"
        assert data["description"] == "Keep me"
        assert data["completed"] is True

    def test_update_todo_not_found_returns_404(self) -> None:
        """PUT /todos/{id} for a non-existent id should return 404."""
        _reset_storage()
        client = TestClient(app)
        response = client.put("/todos/9999", json={"title": "Nope"})

        assert response.status_code == 404
        assert response.json()["detail"] == "Todo not found"


class TestDeleteTodo:
    """Tests for the DELETE /todos/{id} endpoint."""

    def test_delete_todo(self) -> None:
        """DELETE /todos/{id} should return 204 and remove the item."""
        _reset_storage()
        client = TestClient(app)
        create_resp = client.post("/todos", json={"title": "Delete me"})
        todo_id = create_resp.json()["id"]

        response = client.delete(f"/todos/{todo_id}")
        assert response.status_code == 204

        # Confirm it's gone
        get_resp = client.get(f"/todos/{todo_id}")
        assert get_resp.status_code == 404

    def test_delete_todo_not_found_returns_404(self) -> None:
        """DELETE /todos/{id} for a non-existent id should return 404."""
        _reset_storage()
        client = TestClient(app)
        response = client.delete("/todos/9999")

        assert response.status_code == 404
        assert response.json()["detail"] == "Todo not found"
