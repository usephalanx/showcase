"""Tests for the DELETE /tasks/{task_id} endpoint (delete task)."""

from __future__ import annotations

from fastapi.testclient import TestClient


def test_delete_task_success(client: TestClient, sample_task: dict) -> None:
    """Deleting an existing task should return 200 and remove the task."""
    task_id = sample_task["id"]
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200

    # Verify the task is gone
    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 404


def test_delete_task_not_found(client: TestClient) -> None:
    """Deleting a non-existent task returns 404."""
    response = client.delete("/tasks/99999")
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data


def test_delete_task_removes_from_list(client: TestClient) -> None:
    """After deletion the task no longer appears in the list endpoint."""
    # Create two tasks
    r1 = client.post("/tasks", json={"title": "Keep me"})
    r2 = client.post("/tasks", json={"title": "Delete me"})
    assert r1.status_code == 201
    assert r2.status_code == 201

    delete_id = r2.json()["id"]
    keep_id = r1.json()["id"]

    # Delete the second one
    client.delete(f"/tasks/{delete_id}")

    # Verify list only contains the first task
    list_response = client.get("/tasks")
    assert list_response.status_code == 200
    data = list_response.json()
    ids = [t["id"] for t in data]
    assert keep_id in ids
    assert delete_id not in ids


def test_delete_task_twice_returns_404(client: TestClient, sample_task: dict) -> None:
    """Deleting the same task a second time returns 404."""
    task_id = sample_task["id"]
    first = client.delete(f"/tasks/{task_id}")
    assert first.status_code == 200

    second = client.delete(f"/tasks/{task_id}")
    assert second.status_code == 404
