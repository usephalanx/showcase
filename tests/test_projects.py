"""Tests for the projects API endpoints."""

from __future__ import annotations

from fastapi.testclient import TestClient


def test_create_project(client: TestClient) -> None:
    """POST /api/projects creates a project and returns 201."""
    payload = {"name": "Test Project", "description": "A test project."}
    response = client.post("/api/projects", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Project"
    assert data["description"] == "A test project."
    assert "id" in data
    assert "created_at" in data


def test_create_project_minimal(client: TestClient) -> None:
    """POST /api/projects with only a name defaults description to empty string."""
    response = client.post("/api/projects", json={"name": "Minimal"})
    assert response.status_code == 201
    assert response.json()["description"] == ""


def test_create_project_empty_name_fails(client: TestClient) -> None:
    """POST /api/projects with empty name returns 422."""
    response = client.post("/api/projects", json={"name": ""})
    assert response.status_code == 422


def test_list_projects_empty(client: TestClient) -> None:
    """GET /api/projects returns empty list when no projects exist."""
    response = client.get("/api/projects")
    assert response.status_code == 200
    assert response.json() == []


def test_list_projects(client: TestClient) -> None:
    """GET /api/projects returns all created projects."""
    client.post("/api/projects", json={"name": "P1"})
    client.post("/api/projects", json={"name": "P2"})
    response = client.get("/api/projects")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


def test_get_project(client: TestClient) -> None:
    """GET /api/projects/:id returns the correct project."""
    create_resp = client.post("/api/projects", json={"name": "Solo"})
    project_id = create_resp.json()["id"]
    response = client.get(f"/api/projects/{project_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Solo"


def test_get_project_not_found(client: TestClient) -> None:
    """GET /api/projects/:id returns 404 for missing project."""
    response = client.get("/api/projects/9999")
    assert response.status_code == 404


def test_delete_project(client: TestClient) -> None:
    """DELETE /api/projects/:id removes the project."""
    create_resp = client.post("/api/projects", json={"name": "ToDelete"})
    project_id = create_resp.json()["id"]
    response = client.delete(f"/api/projects/{project_id}")
    assert response.status_code == 200
    assert response.json()["detail"] == "Project deleted successfully"
    # Verify it is gone
    assert client.get(f"/api/projects/{project_id}").status_code == 404


def test_delete_project_not_found(client: TestClient) -> None:
    """DELETE /api/projects/:id returns 404 for non-existent project."""
    response = client.delete("/api/projects/9999")
    assert response.status_code == 404
