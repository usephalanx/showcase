"""Unit and integration tests for the Todo API.

Covers all five CRUD endpoints:
- POST   /todos          — create a new todo
- GET    /todos          — list all todos
- GET    /todos/{id}     — retrieve a single todo
- PUT    /todos/{id}     — update an existing todo
- DELETE /todos/{id}     — delete a todo

Also verifies 404 responses for GET, PUT, and DELETE on non-existent IDs.
The in-memory store is reset between every test via a pytest fixture.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Dict

import pytest
from fastapi.testclient import TestClient

# Ensure the project root is on sys.path so that imports resolve correctly.
_PROJECT_ROOT = str(Path(__file__).resolve().parent.parent)
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from main import app  # noqa: E402
from routes import store  # noqa: E402


@pytest.fixture(autouse=True)
def _reset_store() -> None:
    """Reset the in-memory todo store before every test.

    This guarantees each test starts with a clean, empty store and
    predictable auto-increment IDs.
    """
    store.reset()


@pytest.fixture()
def client() -> TestClient:
    """Return a FastAPI TestClient wired to the application."""
    return TestClient(app)


# ------------------------------------------------------------------
# Helper
# ------------------------------------------------------------------

def _create_todo(
    client: TestClient,
    title: str = "Test todo",
    description: str | None = None,
    completed: bool = False,
) -> Dict[str, Any]:
    """Convenience helper that creates a todo and returns the JSON body."""
    payload: Dict[str, Any] = {"title": title, "completed": completed}
    if description is not None:
        payload["description"] = description
    response = client.post("/todos", json=payload)
    assert response.status_code == 201
    return response.json()


# ------------------------------------------------------------------
# POST /todos
# ------------------------------------------------------------------

class TestCreateTodo:
    """Tests for the POST /todos endpoint."""

    def test_create_todo_minimal(self, client: TestClient) -> None:
        """Creating a todo with only a title should succeed."""
        response = client.post("/todos", json={"title": "Buy milk"})
        assert response.status_code == 201
        body = response.json()
        assert body["id"] == 1
        assert body["title"] == "Buy milk"
        assert body["description"] is None
        assert body["completed"] is False
        assert "created_at" in body

    def test_create_todo_with_description(self, client: TestClient) -> None:
        """Creating a todo with a description should persist it."""
        response = client.post(
            "/todos",
            json={"title": "Read book", "description": "Chapter 5"},
        )
        assert response.status_code == 201
        body = response.json()
        assert body["title"] == "Read book"
        assert body["description"] == "Chapter 5"

    def test_create_todo_with_completed_true(self, client: TestClient) -> None:
        """Creating a todo that is already completed should be allowed."""
        response = client.post(
            "/todos",
            json={"title": "Done task", "completed": True},
        )
        assert response.status_code == 201
        assert response.json()["completed"] is True

    def test_create_todo_auto_increment_ids(self, client: TestClient) -> None:
        """Successive creates should yield incrementing IDs."""
        first = _create_todo(client, title="First")
        second = _create_todo(client, title="Second")
        third = _create_todo(client, title="Third")
        assert first["id"] == 1
        assert second["id"] == 2
        assert third["id"] == 3

    def test_create_todo_missing_title(self, client: TestClient) -> None:
        """Omitting the required 'title' field should return 422."""
        response = client.post("/todos", json={})
        assert response.status_code == 422

    def test_create_todo_empty_title(self, client: TestClient) -> None:
        """An empty title string should be rejected (min_length=1)."""
        response = client.post("/todos", json={"title": ""})
        assert response.status_code == 422


# ------------------------------------------------------------------
# GET /todos
# ------------------------------------------------------------------

class TestListTodos:
    """Tests for the GET /todos endpoint."""

    def test_list_todos_empty(self, client: TestClient) -> None:
        """When no todos exist, the list should be empty."""
        response = client.get("/todos")
        assert response.status_code == 200
        assert response.json() == []

    def test_list_todos_multiple(self, client: TestClient) -> None:
        """All created todos should appear in the listing."""
        _create_todo(client, title="Alpha")
        _create_todo(client, title="Beta")
        _create_todo(client, title="Gamma")

        response = client.get("/todos")
        assert response.status_code == 200
        todos = response.json()
        assert len(todos) == 3
        titles = {t["title"] for t in todos}
        assert titles == {"Alpha", "Beta", "Gamma"}

    def test_list_todos_returns_correct_fields(self, client: TestClient) -> None:
        """Each item in the list should contain all expected fields."""
        _create_todo(client, title="Check fields", description="desc")
        response = client.get("/todos")
        todo = response.json()[0]
        assert "id" in todo
        assert "title" in todo
        assert "description" in todo
        assert "completed" in todo
        assert "created_at" in todo


# ------------------------------------------------------------------
# GET /todos/{todo_id}
# ------------------------------------------------------------------

class TestGetTodo:
    """Tests for the GET /todos/{todo_id} endpoint."""

    def test_get_existing_todo(self, client: TestClient) -> None:
        """Fetching an existing todo should return its data."""
        created = _create_todo(client, title="Existing")
        response = client.get(f"/todos/{created['id']}")
        assert response.status_code == 200
        body = response.json()
        assert body["id"] == created["id"]
        assert body["title"] == "Existing"

    def test_get_todo_not_found(self, client: TestClient) -> None:
        """Fetching a non-existent todo should return 404."""
        response = client.get("/todos/999")
        assert response.status_code == 404
        assert response.json()["detail"] == "Todo not found"

    def test_get_todo_not_found_zero(self, client: TestClient) -> None:
        """ID 0 never exists (counter starts at 1) — should return 404."""
        response = client.get("/todos/0")
        assert response.status_code == 404

    def test_get_todo_with_description(self, client: TestClient) -> None:
        """The description field should be correctly returned."""
        created = _create_todo(client, title="With desc", description="Details")
        response = client.get(f"/todos/{created['id']}")
        assert response.status_code == 200
        assert response.json()["description"] == "Details"


# ------------------------------------------------------------------
# PUT /todos/{todo_id}
# ------------------------------------------------------------------

class TestUpdateTodo:
    """Tests for the PUT /todos/{todo_id} endpoint."""

    def test_update_title(self, client: TestClient) -> None:
        """Updating the title should change it and leave other fields intact."""
        created = _create_todo(client, title="Old title")
        response = client.put(
            f"/todos/{created['id']}",
            json={"title": "New title"},
        )
        assert response.status_code == 200
        body = response.json()
        assert body["title"] == "New title"
        assert body["completed"] == created["completed"]

    def test_update_completed(self, client: TestClient) -> None:
        """Updating completed status should toggle the value."""
        created = _create_todo(client, title="Toggle me")
        assert created["completed"] is False

        response = client.put(
            f"/todos/{created['id']}",
            json={"completed": True},
        )
        assert response.status_code == 200
        assert response.json()["completed"] is True

    def test_update_description(self, client: TestClient) -> None:
        """Updating description should change it."""
        created = _create_todo(client, title="Desc test")
        response = client.put(
            f"/todos/{created['id']}",
            json={"description": "Added later"},
        )
        assert response.status_code == 200
        assert response.json()["description"] == "Added later"

    def test_update_multiple_fields(self, client: TestClient) -> None:
        """Updating multiple fields at once should apply all changes."""
        created = _create_todo(client, title="Multi")
        response = client.put(
            f"/todos/{created['id']}",
            json={
                "title": "Updated multi",
                "description": "New desc",
                "completed": True,
            },
        )
        assert response.status_code == 200
        body = response.json()
        assert body["title"] == "Updated multi"
        assert body["description"] == "New desc"
        assert body["completed"] is True

    def test_update_no_fields(self, client: TestClient) -> None:
        """Sending an empty update body should succeed without changes."""
        created = _create_todo(client, title="No change")
        response = client.put(f"/todos/{created['id']}", json={})
        assert response.status_code == 200
        assert response.json()["title"] == "No change"

    def test_update_not_found(self, client: TestClient) -> None:
        """Updating a non-existent todo should return 404."""
        response = client.put("/todos/999", json={"title": "Ghost"})
        assert response.status_code == 404
        assert response.json()["detail"] == "Todo not found"

    def test_update_preserves_id(self, client: TestClient) -> None:
        """The ID must not change after an update."""
        created = _create_todo(client, title="Keep ID")
        response = client.put(
            f"/todos/{created['id']}",
            json={"title": "Still same ID"},
        )
        assert response.json()["id"] == created["id"]


# ------------------------------------------------------------------
# DELETE /todos/{todo_id}
# ------------------------------------------------------------------

class TestDeleteTodo:
    """Tests for the DELETE /todos/{todo_id} endpoint."""

    def test_delete_existing_todo(self, client: TestClient) -> None:
        """Deleting an existing todo should return 204 No Content."""
        created = _create_todo(client, title="To be deleted")
        response = client.delete(f"/todos/{created['id']}")
        assert response.status_code == 204
        assert response.content == b""  # No body for 204

    def test_delete_removes_todo(self, client: TestClient) -> None:
        """After deletion the todo must no longer be retrievable."""
        created = _create_todo(client, title="Ephemeral")
        todo_id = created["id"]

        client.delete(f"/todos/{todo_id}")

        get_response = client.get(f"/todos/{todo_id}")
        assert get_response.status_code == 404

    def test_delete_removes_from_list(self, client: TestClient) -> None:
        """After deletion the todo must not appear in the list."""
        first = _create_todo(client, title="Keep")
        second = _create_todo(client, title="Remove")

        client.delete(f"/todos/{second['id']}")

        listing = client.get("/todos").json()
        assert len(listing) == 1
        assert listing[0]["id"] == first["id"]

    def test_delete_not_found(self, client: TestClient) -> None:
        """Deleting a non-existent todo should return 404."""
        response = client.delete("/todos/999")
        assert response.status_code == 404
        assert response.json()["detail"] == "Todo not found"

    def test_delete_twice(self, client: TestClient) -> None:
        """Deleting the same todo twice should return 404 on the second call."""
        created = _create_todo(client, title="Double delete")
        todo_id = created["id"]

        first_delete = client.delete(f"/todos/{todo_id}")
        assert first_delete.status_code == 204

        second_delete = client.delete(f"/todos/{todo_id}")
        assert second_delete.status_code == 404


# ------------------------------------------------------------------
# Root endpoint
# ------------------------------------------------------------------

class TestRootEndpoint:
    """Tests for the GET / root endpoint."""

    def test_root_returns_message(self, client: TestClient) -> None:
        """The root endpoint should confirm the API is running."""
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Todo API is running"}


# ------------------------------------------------------------------
# Store isolation between tests
# ------------------------------------------------------------------

class TestStoreIsolation:
    """Verify the store is properly reset between tests."""

    def test_isolation_first(self, client: TestClient) -> None:
        """Create a todo — the next test should NOT see it."""
        _create_todo(client, title="Should not leak")
        listing = client.get("/todos").json()
        assert len(listing) == 1

    def test_isolation_second(self, client: TestClient) -> None:
        """The store should be empty after the fixture reset."""
        listing = client.get("/todos").json()
        assert len(listing) == 0

    def test_isolation_ids_reset(self, client: TestClient) -> None:
        """IDs should restart from 1 after a store reset."""
        created = _create_todo(client, title="Fresh start")
        assert created["id"] == 1
