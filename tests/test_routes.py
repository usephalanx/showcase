"""Tests for the Task CRUD API routes.

Uses an in-memory SQLite database so tests are isolated and fast.
"""

from __future__ import annotations

from datetime import date
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.database import Base, get_db
from app.main import app

# ---------------------------------------------------------------------------
# Test database setup
# ---------------------------------------------------------------------------

SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///"

test_engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
TestSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=test_engine,
)


def override_get_db() -> Generator[Session, None, None]:
    """Yield a test database session."""
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def _setup_db() -> Generator[None, None, None]:
    """Create tables before each test and drop them afterward."""
    import app.models  # noqa: F401 – register models

    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


client = TestClient(app)


# ---------------------------------------------------------------------------
# POST /tasks
# ---------------------------------------------------------------------------


class TestCreateTask:
    """Tests for the POST /tasks endpoint."""

    def test_create_task_minimal(self) -> None:
        """Create a task with only a title."""
        response = client.post("/tasks", json={"title": "Buy groceries"})
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Buy groceries"
        assert data["status"] == "todo"
        assert data["due_date"] is None
        assert "id" in data

    def test_create_task_full(self) -> None:
        """Create a task with all fields."""
        payload = {
            "title": "Finish report",
            "status": "in-progress",
            "due_date": "2025-12-31",
        }
        response = client.post("/tasks", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Finish report"
        assert data["status"] == "in-progress"
        assert data["due_date"] == "2025-12-31"

    def test_create_task_empty_title_rejected(self) -> None:
        """A task with an empty title should be rejected."""
        response = client.post("/tasks", json={"title": ""})
        assert response.status_code == 422

    def test_create_task_missing_title_rejected(self) -> None:
        """A task without a title field should be rejected."""
        response = client.post("/tasks", json={})
        assert response.status_code == 422


# ---------------------------------------------------------------------------
# GET /tasks
# ---------------------------------------------------------------------------


class TestListTasks:
    """Tests for the GET /tasks endpoint."""

    def test_list_tasks_empty(self) -> None:
        """An empty database should return an empty list."""
        response = client.get("/tasks")
        assert response.status_code == 200
        assert response.json() == []

    def test_list_tasks_returns_all(self) -> None:
        """All created tasks should be returned."""
        client.post("/tasks", json={"title": "Task 1"})
        client.post("/tasks", json={"title": "Task 2"})
        response = client.get("/tasks")
        assert response.status_code == 200
        assert len(response.json()) == 2

    def test_list_tasks_filter_by_status(self) -> None:
        """Only tasks matching the status filter should be returned."""
        client.post("/tasks", json={"title": "A", "status": "todo"})
        client.post("/tasks", json={"title": "B", "status": "done"})
        client.post("/tasks", json={"title": "C", "status": "todo"})

        response = client.get("/tasks", params={"status": "todo"})
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert all(t["status"] == "todo" for t in data)

    def test_list_tasks_filter_done(self) -> None:
        """Filter by 'done' status."""
        client.post("/tasks", json={"title": "A", "status": "todo"})
        client.post("/tasks", json={"title": "B", "status": "done"})

        response = client.get("/tasks", params={"status": "done"})
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["title"] == "B"

    def test_list_tasks_filter_invalid_status(self) -> None:
        """An invalid status filter should return 422."""
        response = client.get("/tasks", params={"status": "invalid"})
        assert response.status_code == 422


# ---------------------------------------------------------------------------
# GET /tasks/{task_id}
# ---------------------------------------------------------------------------


class TestGetTask:
    """Tests for the GET /tasks/{task_id} endpoint."""

    def test_get_existing_task(self) -> None:
        """Retrieve a task by its ID."""
        create_resp = client.post("/tasks", json={"title": "Test task"})
        task_id = create_resp.json()["id"]

        response = client.get(f"/tasks/{task_id}")
        assert response.status_code == 200
        assert response.json()["id"] == task_id
        assert response.json()["title"] == "Test task"

    def test_get_nonexistent_task(self) -> None:
        """Requesting a non-existent task should return 404."""
        response = client.get("/tasks/9999")
        assert response.status_code == 404


# ---------------------------------------------------------------------------
# PUT /tasks/{task_id}
# ---------------------------------------------------------------------------


class TestUpdateTask:
    """Tests for the PUT /tasks/{task_id} endpoint."""

    def test_update_title(self) -> None:
        """Update only the title of a task."""
        create_resp = client.post("/tasks", json={"title": "Old title"})
        task_id = create_resp.json()["id"]

        response = client.put(
            f"/tasks/{task_id}", json={"title": "New title"}
        )
        assert response.status_code == 200
        assert response.json()["title"] == "New title"
        # Status should remain unchanged
        assert response.json()["status"] == "todo"

    def test_update_status(self) -> None:
        """Update only the status of a task."""
        create_resp = client.post("/tasks", json={"title": "Task"})
        task_id = create_resp.json()["id"]

        response = client.put(
            f"/tasks/{task_id}", json={"status": "done"}
        )
        assert response.status_code == 200
        assert response.json()["status"] == "done"

    def test_update_due_date(self) -> None:
        """Update the due date of a task."""
        create_resp = client.post("/tasks", json={"title": "Task"})
        task_id = create_resp.json()["id"]

        response = client.put(
            f"/tasks/{task_id}", json={"due_date": "2025-06-15"}
        )
        assert response.status_code == 200
        assert response.json()["due_date"] == "2025-06-15"

    def test_update_all_fields(self) -> None:
        """Update all fields at once."""
        create_resp = client.post("/tasks", json={"title": "Old"})
        task_id = create_resp.json()["id"]

        payload = {
            "title": "Updated",
            "status": "in-progress",
            "due_date": "2025-01-01",
        }
        response = client.put(f"/tasks/{task_id}", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated"
        assert data["status"] == "in-progress"
        assert data["due_date"] == "2025-01-01"

    def test_update_nonexistent_task(self) -> None:
        """Updating a non-existent task should return 404."""
        response = client.put(
            "/tasks/9999", json={"title": "Nope"}
        )
        assert response.status_code == 404

    def test_update_empty_body(self) -> None:
        """Sending an empty body should succeed (no fields changed)."""
        create_resp = client.post("/tasks", json={"title": "Task"})
        task_id = create_resp.json()["id"]

        response = client.put(f"/tasks/{task_id}", json={})
        assert response.status_code == 200
        assert response.json()["title"] == "Task"


# ---------------------------------------------------------------------------
# DELETE /tasks/{task_id}
# ---------------------------------------------------------------------------


class TestDeleteTask:
    """Tests for the DELETE /tasks/{task_id} endpoint."""

    def test_delete_existing_task(self) -> None:
        """Delete an existing task."""
        create_resp = client.post("/tasks", json={"title": "To delete"})
        task_id = create_resp.json()["id"]

        response = client.delete(f"/tasks/{task_id}")
        assert response.status_code == 200
        assert "deleted" in response.json()["detail"].lower()

        # Verify it's actually gone
        get_resp = client.get(f"/tasks/{task_id}")
        assert get_resp.status_code == 404

    def test_delete_nonexistent_task(self) -> None:
        """Deleting a non-existent task should return 404."""
        response = client.delete("/tasks/9999")
        assert response.status_code == 404

    def test_delete_twice(self) -> None:
        """Deleting the same task twice should return 404 on the second attempt."""
        create_resp = client.post("/tasks", json={"title": "Once"})
        task_id = create_resp.json()["id"]

        first = client.delete(f"/tasks/{task_id}")
        assert first.status_code == 200

        second = client.delete(f"/tasks/{task_id}")
        assert second.status_code == 404


# ---------------------------------------------------------------------------
# Integration / workflow tests
# ---------------------------------------------------------------------------


class TestWorkflow:
    """End-to-end workflow tests combining multiple endpoints."""

    def test_create_read_update_delete(self) -> None:
        """Full CRUD lifecycle for a single task."""
        # Create
        resp = client.post("/tasks", json={"title": "Lifecycle task"})
        assert resp.status_code == 201
        task_id = resp.json()["id"]

        # Read
        resp = client.get(f"/tasks/{task_id}")
        assert resp.status_code == 200
        assert resp.json()["title"] == "Lifecycle task"

        # Update
        resp = client.put(
            f"/tasks/{task_id}",
            json={"title": "Updated lifecycle", "status": "done"},
        )
        assert resp.status_code == 200
        assert resp.json()["title"] == "Updated lifecycle"
        assert resp.json()["status"] == "done"

        # Delete
        resp = client.delete(f"/tasks/{task_id}")
        assert resp.status_code == 200

        # Confirm gone
        resp = client.get(f"/tasks/{task_id}")
        assert resp.status_code == 404

    def test_list_after_multiple_operations(self) -> None:
        """Ensure list endpoint reflects create and delete operations."""
        # Create 3 tasks
        ids = []
        for i in range(3):
            resp = client.post("/tasks", json={"title": f"Task {i}"})
            ids.append(resp.json()["id"])

        resp = client.get("/tasks")
        assert len(resp.json()) == 3

        # Delete one
        client.delete(f"/tasks/{ids[1]}")

        resp = client.get("/tasks")
        assert len(resp.json()) == 2
        remaining_ids = [t["id"] for t in resp.json()]
        assert ids[1] not in remaining_ids
