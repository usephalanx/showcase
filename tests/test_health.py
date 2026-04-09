"""Tests for the /health endpoint.

Verifies that GET /health returns 200 with {"status": "ok"} and that
unsupported HTTP methods return 405 Method Not Allowed.
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

    assert "application/json" in response.headers["content-type"]


@pytest.mark.asyncio
async def test_root_returns_welcome() -> None:
    """GET / should return 200 with a welcome message."""
    transport = ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Todo API"}
