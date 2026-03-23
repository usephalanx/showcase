"""Tests for the projects API endpoints."""

from __future__ import annotations

from fastapi.testclient import TestClient


def test_list_projects_empty(client: TestClient) -> None:
    """GET /api/projects returns an empty list when no projects exist."""
    response = client.get("/api/projects")
    assert response.status_code == 200
    assert response.json() == []


def test_create_project(client: TestClient) -> None:
    """POST /api/projects creates a project and returns it."""
    payload = {"name": "My Project", "description": "A test project"}
    response = client.post("/api/projects", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "My Project"
    assert data["description"] == "A test project"
    assert "id" in data
    assert "created_at" in data


def test_create_project_name_required(client: TestClient) -> None:
    """POST /api/projects fails if name is missing."""
    response = client.post("/api/projects", json={"description": "No name"})
    assert response.status_code == 422


def test_create_project_empty_name(client: TestClient) -> None:
    """POST /api/projects fails if name is empty string."""
    response = client.post("/api/projects", json={"name": "", "description": "x"})
    assert response.status_code == 422


def test_list_projects_after_create(client: TestClient) -> None:
    """GET /api/projects returns projects after creation."""
    client.post("/api/projects", json={"name": "Project A"})
    client.post("/api/projects", json={"name": "Project B"})
    response = client.get("/api/projects")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


def test_get_project(client: TestClient) -> None:
    """GET /api/projects/:id returns the project with tasks."""
    create_resp = client.post("/api/projects", json={"name": "Detail Project"})
    project_id = create_resp.json()["id"]
    response = client.get(f"/api/projects/{project_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Detail Project"
    assert "tasks" in data


def test_get_project_not_found(client: TestClient) -> None:
    """GET /api/projects/:id returns 404 for nonexistent project."""
    response = client.get("/api/projects/9999")
    assert response.status_code == 404


def test_delete_project(client: TestClient) -> None:
    """DELETE /api/projects/:id removes the project."""
    create_resp = client.post("/api/projects", json={"name": "To Delete"})
    project_id = create_resp.json()["id"]
    delete_resp = client.delete(f"/api/projects/{project_id}")
    assert delete_resp.status_code == 204

    # Verify it is gone
    get_resp = client.get(f"/api/projects/{project_id}")
    assert get_resp.status_code == 404


def test_delete_project_not_found(client: TestClient) -> None:
    """DELETE /api/projects/:id returns 404 for nonexistent project."""
    response = client.delete("/api/projects/9999")
    assert response.status_code == 404


def test_list_projects_pagination(client: TestClient) -> None:
    """GET /api/projects respects skip and limit query params."""
    for i in range(5):
        client.post("/api/projects", json={"name": f"Project {i}"})

    response = client.get("/api/projects?skip=2&limit=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


def test_create_project_default_description(client: TestClient) -> None:
    """POST /api/projects with no description defaults to empty string."""
    response = client.post("/api/projects", json={"name": "No Desc"})
    assert response.status_code == 201
    data = response.json()
    assert data["description"] == ""
