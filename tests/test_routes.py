"""Tests for the CRUD API routes defined in backend/routes.py.

Covers listing, filtering, creating, reading, updating, and deleting
tasks, as well as 404 error handling for missing resources.
"""

from __future__ import annotations

from fastapi.testclient import TestClient


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------


def test_health_check(client: TestClient) -> None:
    """GET /api/health returns status ok."""
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


# ---------------------------------------------------------------------------
# GET /api/tasks — list tasks
# ---------------------------------------------------------------------------


def test_list_tasks_empty(client: TestClient) -> None:
    """GET /api/tasks returns an empty list when no tasks exist."""
    response = client.get("/api/tasks")
    assert response.status_code == 200
    assert response.json() == []


def test_list_tasks_returns_created_tasks(client: TestClient) -> None:
    """GET /api/tasks returns all tasks that have been created."""
    client.post("/api/tasks", json={"title": "Task 1"})
    client.post("/api/tasks", json={"title": "Task 2"})

    response = client.get("/api/tasks")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    titles = {t["title"] for t in data}
    assert titles == {"Task 1", "Task 2"}


def test_list_tasks_filter_by_status(client: TestClient) -> None:
    """GET /api/tasks?status=done returns only tasks with matching status."""
    client.post("/api/tasks", json={"title": "Todo task", "status": "todo"})
    client.post("/api/tasks", json={"title": "Done task", "status": "done"})

    response = client.get("/api/tasks", params={"status": "done"})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Done task"
    assert data[0]["status"] == "done"


def test_list_tasks_filter_by_status_no_match(client: TestClient) -> None:
    """GET /api/tasks?status=in-progress returns empty when nothing matches."""
    client.post("/api/tasks", json={"title": "A task", "status": "todo"})

    response = client.get("/api/tasks", params={"status": "in-progress"})
    assert response.status_code == 200
    assert response.json() == []


# ---------------------------------------------------------------------------
# POST /api/tasks — create task
# ---------------------------------------------------------------------------


def test_create_task_minimal(client: TestClient) -> None:
    """POST /api/tasks with only title creates a task with defaults."""
    response = client.post("/api/tasks", json={"title": "Buy groceries"})
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Buy groceries"
    assert data["status"] == "todo"
    assert data["due_date"] is None
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_create_task_with_all_fields(client: TestClient) -> None:
    """POST /api/tasks with all fields populates them correctly."""
    payload = {
        "title": "Finish report",
        "status": "in-progress",
        "due_date": "2025-12-31",
    }
    response = client.post("/api/tasks", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Finish report"
    assert data["status"] == "in-progress"
    assert data["due_date"] == "2025-12-31"


def test_create_task_validation_empty_title(client: TestClient) -> None:
    """POST /api/tasks with empty title returns 422."""
    response = client.post("/api/tasks", json={"title": ""})
    assert response.status_code == 422


def test_create_task_validation_missing_title(client: TestClient) -> None:
    """POST /api/tasks with missing title returns 422."""
    response = client.post("/api/tasks", json={})
    assert response.status_code == 422


def test_create_task_validation_invalid_status(client: TestClient) -> None:
    """POST /api/tasks with invalid status returns 422."""
    response = client.post(
        "/api/tasks", json={"title": "X", "status": "invalid"}
    )
    assert response.status_code == 422


# ---------------------------------------------------------------------------
# GET /api/tasks/{id} — get single task
# ---------------------------------------------------------------------------


def test_get_task_success(client: TestClient) -> None:
    """GET /api/tasks/{id} returns the correct task."""
    create_resp = client.post("/api/tasks", json={"title": "Read a book"})
    task_id = create_resp.json()["id"]

    response = client.get(f"/api/tasks/{task_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == "Read a book"


def test_get_task_not_found(client: TestClient) -> None:
    """GET /api/tasks/{id} returns 404 for a non-existent task."""
    response = client.get("/api/tasks/99999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


# ---------------------------------------------------------------------------
# PUT /api/tasks/{id} — update task
# ---------------------------------------------------------------------------


def test_update_task_title(client: TestClient) -> None:
    """PUT /api/tasks/{id} updates the title."""
    create_resp = client.post("/api/tasks", json={"title": "Old title"})
    task_id = create_resp.json()["id"]

    response = client.put(
        f"/api/tasks/{task_id}", json={"title": "New title"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New title"


def test_update_task_status(client: TestClient) -> None:
    """PUT /api/tasks/{id} updates the status."""
    create_resp = client.post("/api/tasks", json={"title": "A task"})
    task_id = create_resp.json()["id"]

    response = client.put(
        f"/api/tasks/{task_id}", json={"status": "done"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "done"


def test_update_task_due_date(client: TestClient) -> None:
    """PUT /api/tasks/{id} updates the due_date."""
    create_resp = client.post("/api/tasks", json={"title": "A task"})
    task_id = create_resp.json()["id"]

    response = client.put(
        f"/api/tasks/{task_id}", json={"due_date": "2025-06-15"}
    )
    assert response.status_code == 200
    assert response.json()["due_date"] == "2025-06-15"


def test_update_task_multiple_fields(client: TestClient) -> None:
    """PUT /api/tasks/{id} updates multiple fields at once."""
    create_resp = client.post("/api/tasks", json={"title": "Original"})
    task_id = create_resp.json()["id"]

    response = client.put(
        f"/api/tasks/{task_id}",
        json={"title": "Updated", "status": "in-progress", "due_date": "2025-01-01"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated"
    assert data["status"] == "in-progress"
    assert data["due_date"] == "2025-01-01"


def test_update_task_no_fields(client: TestClient) -> None:
    """PUT /api/tasks/{id} with empty body returns the task unchanged."""
    create_resp = client.post("/api/tasks", json={"title": "Unchanged"})
    task_id = create_resp.json()["id"]

    response = client.put(f"/api/tasks/{task_id}", json={})
    assert response.status_code == 200
    assert response.json()["title"] == "Unchanged"


def test_update_task_not_found(client: TestClient) -> None:
    """PUT /api/tasks/{id} returns 404 for a non-existent task."""
    response = client.put("/api/tasks/99999", json={"title": "Nope"})
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_update_task_invalid_status(client: TestClient) -> None:
    """PUT /api/tasks/{id} with invalid status returns 422."""
    create_resp = client.post("/api/tasks", json={"title": "A task"})
    task_id = create_resp.json()["id"]

    response = client.put(
        f"/api/tasks/{task_id}", json={"status": "bogus"}
    )
    assert response.status_code == 422


# ---------------------------------------------------------------------------
# DELETE /api/tasks/{id} — delete task
# ---------------------------------------------------------------------------


def test_delete_task_success(client: TestClient) -> None:
    """DELETE /api/tasks/{id} removes the task and returns 204."""
    create_resp = client.post("/api/tasks", json={"title": "To delete"})
    task_id = create_resp.json()["id"]

    response = client.delete(f"/api/tasks/{task_id}")
    assert response.status_code == 204

    # Verify it is actually gone.
    get_resp = client.get(f"/api/tasks/{task_id}")
    assert get_resp.status_code == 404


def test_delete_task_not_found(client: TestClient) -> None:
    """DELETE /api/tasks/{id} returns 404 for a non-existent task."""
    response = client.delete("/api/tasks/99999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


# ---------------------------------------------------------------------------
# Integration: full lifecycle
# ---------------------------------------------------------------------------


def test_full_task_lifecycle(client: TestClient) -> None:
    """Create, read, update, and delete a task end-to-end."""
    # Create
    create_resp = client.post(
        "/api/tasks",
        json={"title": "Lifecycle task", "status": "todo"},
    )
    assert create_resp.status_code == 201
    task_id = create_resp.json()["id"]

    # Read
    get_resp = client.get(f"/api/tasks/{task_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["title"] == "Lifecycle task"

    # Update
    put_resp = client.put(
        f"/api/tasks/{task_id}",
        json={"status": "done", "title": "Lifecycle task (done)"},
    )
    assert put_resp.status_code == 200
    assert put_resp.json()["status"] == "done"
    assert put_resp.json()["title"] == "Lifecycle task (done)"

    # List (confirm it shows up)
    list_resp = client.get("/api/tasks")
    assert list_resp.status_code == 200
    assert any(t["id"] == task_id for t in list_resp.json())

    # Delete
    del_resp = client.delete(f"/api/tasks/{task_id}")
    assert del_resp.status_code == 204

    # Confirm deletion
    confirm_resp = client.get(f"/api/tasks/{task_id}")
    assert confirm_resp.status_code == 404
