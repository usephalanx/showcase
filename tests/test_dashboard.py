"""Tests for the dashboard API endpoint."""

from __future__ import annotations

from fastapi.testclient import TestClient


class TestDashboard:
    """GET /api/dashboard."""

    def test_empty_dashboard(self, client: TestClient) -> None:
        """Returns zero counts when the database is empty."""
        resp = client.get("/api/dashboard")
        assert resp.status_code == 200
        data = resp.json()
        assert data["project_count"] == 0
        assert data["open_task_count"] == 0

    def test_dashboard_with_data(self, client: TestClient) -> None:
        """Counts reflect created projects and tasks."""
        # Create a project
        proj_resp = client.post("/api/projects", json={"name": "P1"})
        assert proj_resp.status_code == 201
        pid = proj_resp.json()["id"]

        # Create tasks: 2 open, 1 done
        client.post("/api/tasks", json={"project_id": pid, "title": "T1", "status": "todo"})
        client.post("/api/tasks", json={"project_id": pid, "title": "T2", "status": "in_progress"})
        client.post("/api/tasks", json={"project_id": pid, "title": "T3", "status": "done"})

        resp = client.get("/api/dashboard")
        assert resp.status_code == 200
        data = resp.json()
        assert data["project_count"] == 1
        assert data["open_task_count"] == 2  # "done" is excluded

    def test_dashboard_done_tasks_not_counted(self, client: TestClient) -> None:
        """Only tasks NOT in 'done' status are counted as open."""
        proj = client.post("/api/projects", json={"name": "P"}).json()
        pid = proj["id"]

        # All tasks are done
        client.post("/api/tasks", json={"project_id": pid, "title": "D1", "status": "done"})
        client.post("/api/tasks", json={"project_id": pid, "title": "D2", "status": "done"})

        resp = client.get("/api/dashboard")
        data = resp.json()
        assert data["project_count"] == 1
        assert data["open_task_count"] == 0
