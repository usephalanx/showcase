"""Tests for the GET /health endpoint.

Verifies that the health-check route returns the expected JSON payload
and that unsupported HTTP methods are rejected.
"""

from __future__ import annotations

import pytest
import httpx
from httpx import ASGITransport

from main import app


@pytest.mark.asyncio
async def test_health_returns_ok() -> None:
    """GET /health should return 200 with {"status": "ok"}."""
    transport = ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_health_method_not_allowed() -> None:
    """POST /health should return 405 Method Not Allowed."""
    transport = ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.post("/health")

    assert response.status_code == 405


@pytest.mark.asyncio
async def test_health_response_content_type() -> None:
    """GET /health should return application/json content type."""
    transport = ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.get("/health")

    assert "application/json" in response.headers.get("content-type", "")


@pytest.mark.asyncio
async def test_health_put_method_not_allowed() -> None:
    """PUT /health should return 405 Method Not Allowed."""
    transport = ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.put("/health")

    assert response.status_code == 405


@pytest.mark.asyncio
async def test_health_delete_method_not_allowed() -> None:
    """DELETE /health should return 405 Method Not Allowed."""
    transport = ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.delete("/health")

    assert response.status_code == 405
