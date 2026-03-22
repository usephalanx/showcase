"""Tests for the projects API endpoints."""

from __future__ import annotations

from fastapi.testclient import TestClient


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------


def _create_project(client: TestClient, **kwargs) -> dict:
    """Create a project via the API and return the JSON response."""
    payload = {"name": "Test Project", "description": "A test", "status": "active"}
    payload.update(kwargs)
    resp = client.post("/api/projects", json=payload)
    assert resp.status_code == 201, resp.text
    return resp.json()


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestListProjects:
    """GET /api/projects."""

    def test_empty_list(self, client: TestClient) -> None:
        """Returns empty list when no projects exist."""
        resp = client.get("/api/projects")
        assert resp.status_code == 200
        assert resp.json() == []

    def test_list_returns_created(self, client: TestClient) -> None:
        """Returns projects that were created."""
        _create_project(client, name="Alpha")
        _create_project(client, name="Beta")
        resp = client.get("/api/projects")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 2


class TestCreateProject:
    """POST /api/projects."""

    def test_create_success(self, client: TestClient) -> None:
        """Successful creation returns 201 with project data."""
        data = _create_project(client, name="My Project")
        assert data["name"] == "My Project"
        assert data["status"] == "active"
        assert "id" in data
        assert "created_at" in data

    def test_create_missing_name(self, client: TestClient) -> None:
        """Missing name returns 422."""
        resp = client.post("/api/projects", json={"description": "no name"})
        assert resp.status_code == 422

    def test_create_empty_name(self, client: TestClient) -> None:
        """Empty name string returns 422."""
        resp = client.post("/api/projects", json={"name": ""})
        assert resp.status_code == 422

    def test_create_name_too_long(self, client: TestClient) -> None:
        """Name exceeding 100 chars returns 422."""
        resp = client.post("/api/projects", json={"name": "x" * 101})
        assert resp.status_code == 422

    def test_create_invalid_status(self, client: TestClient) -> None:
        """Invalid status enum returns 422."""
        resp = client.post("/api/projects", json={"name": "P", "status": "nope"})
        assert resp.status_code == 422


class TestGetProject:
    """GET /api/projects/{id}."""

    def test_get_existing(self, client: TestClient) -> None:
        """Returns project by id."""
        created = _create_project(client)
        resp = client.get(f"/api/projects/{created['id']}")
        assert resp.status_code == 200
        assert resp.json()["id"] == created["id"]

    def test_get_not_found(self, client: TestClient) -> None:
        """Returns 404 for nonexistent project."""
        resp = client.get("/api/projects/9999")
        assert resp.status_code == 404


class TestUpdateProject:
    """PUT /api/projects/{id}."""

    def test_update_name(self, client: TestClient) -> None:
        """Update only the name."""
        created = _create_project(client, name="Old")
        resp = client.put(
            f"/api/projects/{created['id']}", json={"name": "New"}
        )
        assert resp.status_code == 200
        assert resp.json()["name"] == "New"

    def test_update_status(self, client: TestClient) -> None:
        """Update the status."""
        created = _create_project(client)
        resp = client.put(
            f"/api/projects/{created['id']}", json={"status": "archived"}
        )
        assert resp.status_code == 200
        assert resp.json()["status"] == "archived"

    def test_update_not_found(self, client: TestClient) -> None:
        """Returns 404 for nonexistent project."""
        resp = client.put("/api/projects/9999", json={"name": "X"})
        assert resp.status_code == 404

    def test_update_invalid_status(self, client: TestClient) -> None:
        """Invalid status returns 422."""
        created = _create_project(client)
        resp = client.put(
            f"/api/projects/{created['id']}", json={"status": "bad"}
        )
        assert resp.status_code == 422


class TestDeleteProject:
    """DELETE /api/projects/{id}."""

    def test_delete_existing(self, client: TestClient) -> None:
        """Successful delete returns 204."""
        created = _create_project(client)
        resp = client.delete(f"/api/projects/{created['id']}")
        assert resp.status_code == 204
        # Verify it's gone
        resp2 = client.get(f"/api/projects/{created['id']}")
        assert resp2.status_code == 404

    def test_delete_not_found(self, client: TestClient) -> None:
        """Returns 404 for nonexistent project."""
        resp = client.delete("/api/projects/9999")
        assert resp.status_code == 404

    def test_delete_cascades_tasks(self, client: TestClient) -> None:
        """Deleting a project also deletes its tasks."""
        proj = _create_project(client)
        # Create a task under that project
        task_resp = client.post(
            "/api/tasks",
            json={"project_id": proj["id"], "title": "Orphan me"},
        )
        assert task_resp.status_code == 201
        task_id = task_resp.json()["id"]
        # Delete the project
        client.delete(f"/api/projects/{proj['id']}")
        # Task should be gone
        resp = client.get(f"/api/tasks/{task_id}")
        assert resp.status_code == 404


class TestListProjectTasks:
    """GET /api/projects/{id}/tasks."""

    def test_tasks_for_project(self, client: TestClient) -> None:
        """Returns only tasks belonging to the project."""
        proj = _create_project(client)
        client.post("/api/tasks", json={"project_id": proj["id"], "title": "T1"})
        client.post("/api/tasks", json={"project_id": proj["id"], "title": "T2"})
        resp = client.get(f"/api/projects/{proj['id']}/tasks")
        assert resp.status_code == 200
        assert len(resp.json()) == 2

    def test_tasks_project_not_found(self, client: TestClient) -> None:
        """Returns 404 when the project doesn't exist."""
        resp = client.get("/api/projects/9999/tasks")
        assert resp.status_code == 404
