"""Tests for the PUT /tasks/{task_id} endpoint (update task)."""

from __future__ import annotations

from fastapi.testclient import TestClient


def test_update_task_title(client: TestClient, sample_task: dict) -> None:
    """Updating only the title should preserve other fields."""
    task_id = sample_task["id"]
    response = client.put(f"/tasks/{task_id}", json={"title": "Updated title"})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated title"
    assert data["status"] == sample_task["status"]
    assert data["id"] == task_id


def test_update_task_status(client: TestClient, sample_task: dict) -> None:
    """Updating the status should persist correctly."""
    task_id = sample_task["id"]
    response = client.put(f"/tasks/{task_id}", json={"status": "done"})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "done"


def test_update_task_due_date(client: TestClient, sample_task: dict) -> None:
    """Updating the due_date should reflect the new value."""
    task_id = sample_task["id"]
    response = client.put(f"/tasks/{task_id}", json={"due_date": "2026-01-01"})
    assert response.status_code == 200
    data = response.json()
    assert data["due_date"] == "2026-01-01"


def test_update_task_multiple_fields(client: TestClient, sample_task: dict) -> None:
    """Updating multiple fields at once should work."""
    task_id = sample_task["id"]
    payload = {"title": "Multi-update", "status": "in-progress", "due_date": "2025-11-11"}
    response = client.put(f"/tasks/{task_id}", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Multi-update"
    assert data["status"] == "in-progress"
    assert data["due_date"] == "2025-11-11"


def test_update_task_not_found(client: TestClient) -> None:
    """Updating a non-existent task returns 404."""
    response = client.put("/tasks/99999", json={"title": "Ghost"})
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data


def test_update_task_no_changes(client: TestClient, sample_task: dict) -> None:
    """Sending an empty update body should still return the task unchanged."""
    task_id = sample_task["id"]
    response = client.put(f"/tasks/{task_id}", json={})
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == sample_task["title"]
