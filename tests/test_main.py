"""Tests for the /hello endpoint in app.main."""

from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.mark.anyio
async def test_hello_returns_hello_world() -> None:
    """GET /hello should return 200 with the expected JSON greeting."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/hello")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}


@pytest.mark.anyio
async def test_hello_method_not_allowed() -> None:
    """POST /hello should return 405 Method Not Allowed."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/hello")
    assert response.status_code == 405


@pytest.mark.anyio
async def test_nonexistent_endpoint_returns_404() -> None:
    """GET /nonexistent should return 404 Not Found."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/nonexistent")
    assert response.status_code == 404
