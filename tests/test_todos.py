"""Tests for the Todo CRUD endpoints.

Verifies creation, listing, retrieval, update, and deletion of
todo items via the /todos routes.
"""

from __future__ import annotations

import pytest
import httpx
from httpx import ASGITransport

from main import app
from routes import store


@pytest.fixture(autouse=True)
def _reset_store() -> None:
    """Reset the in-memory store before each test to ensure isolation."""
    store._todos.clear()
    store._next_id = 1


@pytest.mark.asyncio
async def test_create_todo() -> None:
    """POST /todos should create a todo and return 201."""
    transport = ASGITransport(app=app)  # type: ignore[arg-type]
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/todos", json={"title": "Buy milk"})

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Buy milk"
    assert data["completed"] is False
    assert "id" in data
    assert "created_at" in data


@pytest.mark.asyncio
async def test_create_todo_empty_title() -> None:
    """POST /todos with empty title should return 422."""
    transport = ASGITransport(app=app)  # type: ignore[arg-type]
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/todos", json={"title": ""})

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_list_todos_empty() -> None:
    """GET /todos with no items should return an empty list."""
    transport = ASGITransport(app=app)  # type: ignore[arg-type]
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/todos")

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_list_todos_with_items() -> None:
    """GET /todos should return all created items."""
    transport = ASGITransport(app=app)  # type: ignore[arg-type]
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/todos", json={"title": "Task 1"})
        await client.post("/todos", json={"title": "Task 2"})
        response = await client.get("/todos")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


@pytest.mark.asyncio
async def test_get_todo_by_id() -> None:
    """GET /todos/{id} should return the specific todo."""
    transport = ASGITransport(app=app)  # type: ignore[arg-type]
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        create_resp = await client.post("/todos", json={"title": "Specific"})
        todo_id = create_resp.json()["id"]
        response = await client.get(f"/todos/{todo_id}")

    assert response.status_code == 200
    assert response.json()["title"] == "Specific"


@pytest.mark.asyncio
async def test_get_todo_not_found() -> None:
    """GET /todos/{id} with non-existent id should return 404."""
    transport = ASGITransport(app=app)  # type: ignore[arg-type]
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/todos/9999")

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_todo() -> None:
    """PUT /todos/{id} should update the todo fields."""
    transport = ASGITransport(app=app)  # type: ignore[arg-type]
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        create_resp = await client.post("/todos", json={"title": "Original"})
        todo_id = create_resp.json()["id"]
        response = await client.put(
            f"/todos/{todo_id}",
            json={"title": "Updated", "completed": True},
        )

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated"
    assert data["completed"] is True


@pytest.mark.asyncio
async def test_update_todo_not_found() -> None:
    """PUT /todos/{id} with non-existent id should return 404."""
    transport = ASGITransport(app=app)  # type: ignore[arg-type]
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.put(
            "/todos/9999", json={"title": "Nope"}
        )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_todo() -> None:
    """DELETE /todos/{id} should remove the todo and return 200."""
    transport = ASGITransport(app=app)  # type: ignore[arg-type]
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        create_resp = await client.post("/todos", json={"title": "To delete"})
        todo_id = create_resp.json()["id"]
        response = await client.delete(f"/todos/{todo_id}")

    assert response.status_code == 200
    assert response.json()["detail"] == "Todo deleted successfully"


@pytest.mark.asyncio
async def test_delete_todo_not_found() -> None:
    """DELETE /todos/{id} with non-existent id should return 404."""
    transport = ASGITransport(app=app)  # type: ignore[arg-type]
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.delete("/todos/9999")

    assert response.status_code == 404
