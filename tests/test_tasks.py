"""Tests for the tasks API endpoints."""

from __future__ import annotations

from fastapi.testclient import TestClient


def _create_project(client: TestClient, name: str = "TestProject") -> int:
    """Helper to create a project and return its id."""
    resp = client.post("/api/projects", json={"name": name})
    return resp.json()["id"]


def test_create_task(client: TestClient) -> None:
    """POST /api/tasks creates a task and returns 201."""
    project_id = _create_project(client)
    payload = {"project_id": project_id, "title": "Write tests"}
    response = client.post("/api/tasks", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Write tests"
    assert data["project_id"] == project_id
    assert data["status"] == "todo"
    assert data["priority"] == "medium"
    assert data["due_date"] is None
    assert "id" in data
    assert "created_at" in data


def test_create_task_with_all_fields(client: TestClient) -> None:
    """POST /api/tasks with all fields set returns correct values."""
    project_id = _create_project(client)
    payload = {
        "project_id": project_id,
        "title": "Deploy",
        "status": "in_progress",
        "priority": "high",
        "due_date": "2025-12-31",
    }
    response = client.post("/api/tasks", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "in_progress"
    assert data["priority"] == "high"
    assert data["due_date"] == "2025-12-31"


def test_create_task_invalid_project(client: TestClient) -> None:
    """POST /api/tasks with non-existent project_id returns 404."""
    payload = {"project_id": 9999, "title": "Orphan"}
    response = client.post("/api/tasks", json=payload)
    assert response.status_code == 404


def test_create_task_empty_title_fails(client: TestClient) -> None:
    """POST /api/tasks with empty title returns 422."""
    project_id = _create_project(client)
    payload = {"project_id": project_id, "title": ""}
    response = client.post("/api/tasks", json=payload)
    assert response.status_code == 422


def test_list_tasks_empty(client: TestClient) -> None:
    """GET /api/tasks returns empty list when no tasks exist."""
    response = client.get("/api/tasks")
    assert response.status_code == 200
    assert response.json() == []


def test_list_tasks(client: TestClient) -> None:
    """GET /api/tasks returns all created tasks."""
    project_id = _create_project(client)
    client.post("/api/tasks", json={"project_id": project_id, "title": "T1"})
    client.post("/api/tasks", json={"project_id": project_id, "title": "T2"})
    response = client.get("/api/tasks")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_list_tasks_filter_by_project(client: TestClient) -> None:
    """GET /api/tasks?project_id=X returns only tasks for that project."""
    p1 = _create_project(client, "P1")
    p2 = _create_project(client, "P2")
    client.post("/api/tasks", json={"project_id": p1, "title": "A"})
    client.post("/api/tasks", json={"project_id": p2, "title": "B"})
    response = client.get(f"/api/tasks?project_id={p1}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "A"


def test_get_task(client: TestClient) -> None:
    """GET /api/tasks/:id returns the correct task."""
    project_id = _create_project(client)
    create_resp = client.post(
        "/api/tasks", json={"project_id": project_id, "title": "Fetch me"}
    )
    task_id = create_resp.json()["id"]
    response = client.get(f"/api/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Fetch me"


def test_get_task_not_found(client: TestClient) -> None:
    """GET /api/tasks/:id returns 404 for missing task."""
    response = client.get("/api/tasks/9999")
    assert response.status_code == 404


def test_update_task_status(client: TestClient) -> None:
    """PATCH /api/tasks/:id updates the status."""
    project_id = _create_project(client)
    create_resp = client.post(
        "/api/tasks", json={"project_id": project_id, "title": "Update me"}
    )
    task_id = create_resp.json()["id"]
    response = client.patch(f"/api/tasks/{task_id}", json={"status": "done"})
    assert response.status_code == 200
    assert response.json()["status"] == "done"


def test_update_task_priority(client: TestClient) -> None:
    """PATCH /api/tasks/:id updates the priority."""
    project_id = _create_project(client)
    create_resp = client.post(
        "/api/tasks", json={"project_id": project_id, "title": "Priority"}
    )
    task_id = create_resp.json()["id"]
    response = client.patch(f"/api/tasks/{task_id}", json={"priority": "low"})
    assert response.status_code == 200
    assert response.json()["priority"] == "low"


def test_update_task_title(client: TestClient) -> None:
    """PATCH /api/tasks/:id updates the title."""
    project_id = _create_project(client)
    create_resp = client.post(
        "/api/tasks", json={"project_id": project_id, "title": "Old"}
    )
    task_id = create_resp.json()["id"]
    response = client.patch(f"/api/tasks/{task_id}", json={"title": "New"})
    assert response.status_code == 200
    assert response.json()["title"] == "New"


def test_update_task_not_found(client: TestClient) -> None:
    """PATCH /api/tasks/:id returns 404 for missing task."""
    response = client.patch("/api/tasks/9999", json={"status": "done"})
    assert response.status_code == 404


def test_delete_task(client: TestClient) -> None:
    """DELETE /api/tasks/:id removes the task."""
    project_id = _create_project(client)
    create_resp = client.post(
        "/api/tasks", json={"project_id": project_id, "title": "Remove me"}
    )
    task_id = create_resp.json()["id"]
    response = client.delete(f"/api/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["detail"] == "Task deleted successfully"
    # Verify it is gone
    assert client.get(f"/api/tasks/{task_id}").status_code == 404


def test_delete_task_not_found(client: TestClient) -> None:
    """DELETE /api/tasks/:id returns 404 for non-existent task."""
    response = client.delete("/api/tasks/9999")
    assert response.status_code == 404


def test_cascade_delete_project_removes_tasks(client: TestClient) -> None:
    """Deleting a project cascades to delete its tasks."""
    project_id = _create_project(client)
    client.post("/api/tasks", json={"project_id": project_id, "title": "Child"})
    client.delete(f"/api/projects/{project_id}")
    response = client.get(f"/api/tasks?project_id={project_id}")
    assert response.status_code == 200
    assert response.json() == []
