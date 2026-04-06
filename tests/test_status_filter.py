"""Tests for the status query-parameter filter on GET /tasks."""

from __future__ import annotations

from fastapi.testclient import TestClient


def _seed_tasks(client: TestClient) -> list[dict]:
    """Create tasks with different statuses and return them."""
    tasks = [
        {"title": "Todo task 1", "status": "todo"},
        {"title": "Todo task 2", "status": "todo"},
        {"title": "In-progress task", "status": "in-progress"},
        {"title": "Done task", "status": "done"},
    ]
    created = []
    for t in tasks:
        r = client.post("/tasks", json=t)
        assert r.status_code == 201
        created.append(r.json())
    return created


def test_filter_by_todo(client: TestClient) -> None:
    """Filtering by 'todo' returns only todo tasks."""
    _seed_tasks(client)
    response = client.get("/tasks", params={"status": "todo"})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert all(t["status"] == "todo" for t in data)


def test_filter_by_in_progress(client: TestClient) -> None:
    """Filtering by 'in-progress' returns only in-progress tasks."""
    _seed_tasks(client)
    response = client.get("/tasks", params={"status": "in-progress"})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["status"] == "in-progress"
    assert data[0]["title"] == "In-progress task"


def test_filter_by_done(client: TestClient) -> None:
    """Filtering by 'done' returns only done tasks."""
    _seed_tasks(client)
    response = client.get("/tasks", params={"status": "done"})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["status"] == "done"


def test_filter_no_match(client: TestClient) -> None:
    """Filtering by a status with no matching tasks returns an empty list."""
    client.post("/tasks", json={"title": "Only todo", "status": "todo"})
    response = client.get("/tasks", params={"status": "done"})
    assert response.status_code == 200
    assert response.json() == []


def test_no_filter_returns_all(client: TestClient) -> None:
    """Without a status filter all tasks are returned."""
    _seed_tasks(client)
    response = client.get("/tasks")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 4
