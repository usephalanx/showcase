"""Tests for the POST /tasks endpoint (create task)."""

from __future__ import annotations

from fastapi.testclient import TestClient


def test_create_task_minimal(client: TestClient) -> None:
    """Creating a task with only a title should succeed with defaults."""
    payload = {"title": "Buy groceries"}
    response = client.post("/tasks", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Buy groceries"
    assert data["status"] == "todo"
    assert data["due_date"] is None
    assert "id" in data


def test_create_task_with_all_fields(client: TestClient) -> None:
    """Creating a task with all fields populates them correctly."""
    payload = {
        "title": "Write report",
        "status": "in-progress",
        "due_date": "2025-06-15",
    }
    response = client.post("/tasks", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Write report"
    assert data["status"] == "in-progress"
    assert data["due_date"] == "2025-06-15"


def test_create_task_returns_unique_ids(client: TestClient) -> None:
    """Each created task should receive a unique id."""
    ids = set()
    for i in range(5):
        resp = client.post("/tasks", json={"title": f"Task {i}"})
        assert resp.status_code == 201
        ids.add(resp.json()["id"])
    assert len(ids) == 5


def test_create_task_empty_title_rejected(client: TestClient) -> None:
    """A task with an empty title should be rejected (422)."""
    payload = {"title": ""}
    response = client.post("/tasks", json=payload)
    assert response.status_code == 422


def test_create_task_missing_title_rejected(client: TestClient) -> None:
    """A task without a title field should be rejected (422)."""
    payload = {"status": "todo"}
    response = client.post("/tasks", json=payload)
    assert response.status_code == 422
