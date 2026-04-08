"""Integration tests for the FastAPI application.

Verifies that the application starts correctly with seeded data and
that core endpoints function as expected.
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.seed import SAMPLE_TODOS
from app.storage import storage


@pytest.fixture(autouse=True)
def _reset_storage() -> None:
    """Clear storage before each test so tests are independent."""
    storage.clear()


@pytest.fixture()
def client() -> TestClient:
    """Return a TestClient wired to the FastAPI app.

    Using the context-manager form ensures the lifespan events fire,
    which seeds demo data into the store.
    """
    with TestClient(app) as c:
        yield c


class TestHealthCheck:
    """Tests for the /health endpoint."""

    def test_health_returns_ok(self, client: TestClient) -> None:
        """GET /health should return 200 with status ok."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}


class TestLifespanSeed:
    """Tests verifying that the lifespan event seeds data."""

    def test_todos_seeded_on_startup(self, client: TestClient) -> None:
        """GET /todos should return the seeded sample items."""
        response = client.get("/todos")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == len(SAMPLE_TODOS)

    def test_seeded_todos_have_correct_structure(self, client: TestClient) -> None:
        """Each seeded todo should have id, title, description, and completed."""
        response = client.get("/todos")
        for todo in response.json():
            assert "id" in todo
            assert "title" in todo
            assert "description" in todo
            assert "completed" in todo


class TestCrudEndpoints:
    """Smoke tests for the CRUD endpoints."""

    def test_create_todo(self, client: TestClient) -> None:
        """POST /todos should create a new item."""
        response = client.post("/todos", json={"title": "New task"})
        assert response.status_code == 201
        body = response.json()
        assert body["title"] == "New task"
        assert body["completed"] is False

    def test_get_todo_by_id(self, client: TestClient) -> None:
        """GET /todos/{id} should return the matching item."""
        # The lifespan seeds items with ids starting at 1
        response = client.get("/todos/1")
        assert response.status_code == 200
        assert response.json()["id"] == 1

    def test_get_todo_not_found(self, client: TestClient) -> None:
        """GET /todos/{id} for a missing id should return 404."""
        response = client.get("/todos/9999")
        assert response.status_code == 404

    def test_update_todo(self, client: TestClient) -> None:
        """PUT /todos/{id} should update the item."""
        response = client.put("/todos/1", json={"completed": True})
        assert response.status_code == 200
        assert response.json()["completed"] is True

    def test_update_todo_not_found(self, client: TestClient) -> None:
        """PUT /todos/{id} for a missing id should return 404."""
        response = client.put("/todos/9999", json={"completed": True})
        assert response.status_code == 404

    def test_delete_todo(self, client: TestClient) -> None:
        """DELETE /todos/{id} should return 204."""
        response = client.delete("/todos/1")
        assert response.status_code == 204

    def test_delete_todo_not_found(self, client: TestClient) -> None:
        """DELETE /todos/{id} for a missing id should return 404."""
        response = client.delete("/todos/9999")
        assert response.status_code == 404

    def test_create_todo_missing_title_returns_422(self, client: TestClient) -> None:
        """POST /todos without a title should return 422."""
        response = client.post("/todos", json={})
        assert response.status_code == 422
