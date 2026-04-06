"""Tests for the GET /tasks/{task_id} endpoint (get single task)."""

from __future__ import annotations

from fastapi.testclient import TestClient


def test_get_task_success(client: TestClient, sample_task: dict) -> None:
    """Retrieving an existing task by ID returns the correct data."""
    task_id = sample_task["id"]
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == sample_task["title"]
    assert data["status"] == sample_task["status"]
    assert data["due_date"] == sample_task["due_date"]


def test_get_task_not_found(client: TestClient) -> None:
    """Requesting a non-existent task ID returns 404."""
    response = client.get("/tasks/99999")
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data


def test_get_task_not_found_zero(client: TestClient) -> None:
    """Requesting task ID 0 (which never exists) returns 404."""
    response = client.get("/tasks/0")
    assert response.status_code == 404
