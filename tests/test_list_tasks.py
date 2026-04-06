"""Tests for the GET /tasks endpoint (list tasks)."""

from __future__ import annotations

from fastapi.testclient import TestClient


def test_list_tasks_empty(client: TestClient) -> None:
    """An empty database should return an empty list."""
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.json() == []


def test_list_tasks_returns_created_tasks(client: TestClient) -> None:
    """After creating tasks, the list endpoint returns all of them."""
    titles = ["First", "Second", "Third"]
    for title in titles:
        client.post("/tasks", json={"title": title})

    response = client.get("/tasks")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    returned_titles = {t["title"] for t in data}
    assert returned_titles == set(titles)


def test_list_tasks_response_shape(client: TestClient, sample_task: dict) -> None:
    """Each task in the list has the expected fields."""
    response = client.get("/tasks")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    task = data[0]
    assert "id" in task
    assert "title" in task
    assert "status" in task
    assert "due_date" in task
