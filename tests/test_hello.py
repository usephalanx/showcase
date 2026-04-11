"""Tests for the /hello endpoint in app.main."""

from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.mark.anyio
async def test_hello_endpoint() -> None:
    """GET /hello should return 200 with the expected JSON body."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/hello")

    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}


@pytest.mark.anyio
async def test_hello_endpoint_with_query_params() -> None:
    """GET /hello with unexpected query params still returns correct response."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/hello", params={"foo": "bar"})

    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}


@pytest.mark.anyio
async def test_nonexistent_endpoint_returns_404() -> None:
    """Requesting a non-existent path should return 404."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/nonexistent")

    assert response.status_code == 404
