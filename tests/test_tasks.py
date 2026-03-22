"""Tests for the tasks API endpoints."""

from __future__ import annotations

from fastapi.testclient import TestClient


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _create_project(client: TestClient, name: str = "Proj") -> dict:
    """Create a project and return its JSON."""
    resp = client.post("/api/projects", json={"name": name})
    assert resp.status_code == 201
    return resp.json()


def _create_task(client: TestClient, project_id: int, **kwargs) -> dict:
    """Create a task and return its JSON."""
    payload = {"project_id": project_id, "title": "Test Task"}
    payload.update(kwargs)
    resp = client.post("/api/tasks", json=payload)
    assert resp.status_code == 201, resp.text
    return resp.json()


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestListTasks:
    """GET /api/tasks."""

    def test_empty(self, client: TestClient) -> None:
        """Returns empty list when no tasks exist."""
        resp = client.get("/api/tasks")
        assert resp.status_code == 200
        assert resp.json() == []

    def test_filter_by_status(self, client: TestClient) -> None:
        """Filters tasks by status query parameter."""
        proj = _create_project(client)
        _create_task(client, proj["id"], title="A", status="todo")
        _create_task(client, proj["id"], title="B", status="done")
        resp = client.get("/api/tasks?status=todo")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 1
        assert data[0]["status"] == "todo"

    def test_filter_by_project_id(self, client: TestClient) -> None:
        """Filters tasks by project_id query parameter."""
        p1 = _create_project(client, name="P1")
        p2 = _create_project(client, name="P2")
        _create_task(client, p1["id"])
        _create_task(client, p2["id"])
        resp = client.get(f"/api/tasks?project_id={p1['id']}")
        assert resp.status_code == 200
        assert len(resp.json()) == 1

    def test_filter_by_priority(self, client: TestClient) -> None:
        """Filters tasks by priority query parameter."""
        proj = _create_project(client)
        _create_task(client, proj["id"], title="Low", priority="low")
        _create_task(client, proj["id"], title="High", priority="high")
        resp = client.get("/api/tasks?priority=high")
        assert resp.status_code == 200
        data = resp.json()
        assert all(t["priority"] == "high" for t in data)


class TestCreateTask:
    """POST /api/tasks."""

    def test_create_success(self, client: TestClient) -> None:
        """Successful creation returns 201."""
        proj = _create_project(client)
        data = _create_task(client, proj["id"], title="My Task")
        assert data["title"] == "My Task"
        assert data["status"] == "todo"
        assert data["priority"] == "medium"

    def test_create_with_due_date(self, client: TestClient) -> None:
        """Task can be created with a due date."""
        proj = _create_project(client)
        data = _create_task(client, proj["id"], due_date="2025-06-01")
        assert data["due_date"] == "2025-06-01"

    def test_create_invalid_project_id(self, client: TestClient) -> None:
        """Referencing a non-existent project returns 400."""
        resp = client.post(
            "/api/tasks", json={"project_id": 9999, "title": "Bad"}
        )
        assert resp.status_code == 400

    def test_create_missing_title(self, client: TestClient) -> None:
        """Missing title returns 422."""
        proj = _create_project(client)
        resp = client.post("/api/tasks", json={"project_id": proj["id"]})
        assert resp.status_code == 422

    def test_create_empty_title(self, client: TestClient) -> None:
        """Empty title returns 422."""
        proj = _create_project(client)
        resp = client.post(
            "/api/tasks", json={"project_id": proj["id"], "title": ""}
        )
        assert resp.status_code == 422

    def test_create_invalid_status(self, client: TestClient) -> None:
        """Invalid status enum returns 422."""
        proj = _create_project(client)
        resp = client.post(
            "/api/tasks",
            json={"project_id": proj["id"], "title": "T", "status": "invalid"},
        )
        assert resp.status_code == 422


class TestGetTask:
    """GET /api/tasks/{id}."""

    def test_get_existing(self, client: TestClient) -> None:
        """Returns a task by id."""
        proj = _create_project(client)
        task = _create_task(client, proj["id"])
        resp = client.get(f"/api/tasks/{task['id']}")
        assert resp.status_code == 200
        assert resp.json()["id"] == task["id"]

    def test_get_not_found(self, client: TestClient) -> None:
        """Returns 404 for nonexistent task."""
        resp = client.get("/api/tasks/9999")
        assert resp.status_code == 404


class TestUpdateTask:
    """PUT /api/tasks/{id}."""

    def test_update_title(self, client: TestClient) -> None:
        """Update only the title."""
        proj = _create_project(client)
        task = _create_task(client, proj["id"], title="Old")
        resp = client.put(f"/api/tasks/{task['id']}", json={"title": "New"})
        assert resp.status_code == 200
        assert resp.json()["title"] == "New"

    def test_update_multiple_fields(self, client: TestClient) -> None:
        """Update status and priority at once."""
        proj = _create_project(client)
        task = _create_task(client, proj["id"])
        resp = client.put(
            f"/api/tasks/{task['id']}",
            json={"status": "done", "priority": "high"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "done"
        assert data["priority"] == "high"

    def test_update_not_found(self, client: TestClient) -> None:
        """Returns 404 for nonexistent task."""
        resp = client.put("/api/tasks/9999", json={"title": "X"})
        assert resp.status_code == 404


class TestPatchTaskStatus:
    """PATCH /api/tasks/{id}/status."""

    def test_patch_status(self, client: TestClient) -> None:
        """Status-only update works."""
        proj = _create_project(client)
        task = _create_task(client, proj["id"])
        resp = client.patch(
            f"/api/tasks/{task['id']}/status", json={"status": "in_progress"}
        )
        assert resp.status_code == 200
        assert resp.json()["status"] == "in_progress"

    def test_patch_status_invalid(self, client: TestClient) -> None:
        """Invalid status enum returns 422."""
        proj = _create_project(client)
        task = _create_task(client, proj["id"])
        resp = client.patch(
            f"/api/tasks/{task['id']}/status", json={"status": "nope"}
        )
        assert resp.status_code == 422

    def test_patch_status_not_found(self, client: TestClient) -> None:
        """Returns 404 for nonexistent task."""
        resp = client.patch("/api/tasks/9999/status", json={"status": "done"})
        assert resp.status_code == 404


class TestDeleteTask:
    """DELETE /api/tasks/{id}."""

    def test_delete_existing(self, client: TestClient) -> None:
        """Successful delete returns 204."""
        proj = _create_project(client)
        task = _create_task(client, proj["id"])
        resp = client.delete(f"/api/tasks/{task['id']}")
        assert resp.status_code == 204
        # Verify gone
        resp2 = client.get(f"/api/tasks/{task['id']}")
        assert resp2.status_code == 404

    def test_delete_not_found(self, client: TestClient) -> None:
        """Returns 404 for nonexistent task."""
        resp = client.delete("/api/tasks/9999")
        assert resp.status_code == 404
