"""Test suite for the FastAPI /hello endpoint.

Covers:
- GET /hello returns 200 with correct JSON body.
- POST /hello returns 405 Method Not Allowed.
- Other unsupported methods (PUT, DELETE, PATCH) return 405.
- Non-existent route returns 404.
"""

from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.fixture
def anyio_backend() -> str:
    """Select asyncio as the anyio backend for async tests."""
    return "asyncio"


@pytest.fixture
async def client() -> AsyncClient:
    """Create an async HTTP client bound to the FastAPI app."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
        yield ac


@pytest.mark.anyio
async def test_hello_returns_200(client: AsyncClient) -> None:
    """GET /hello should return HTTP 200."""
    response = await client.get("/hello")
    assert response.status_code == 200


@pytest.mark.anyio
async def test_hello_returns_correct_json(client: AsyncClient) -> None:
    """GET /hello should return {'message': 'Hello, World!'}."""
    response = await client.get("/hello")
    assert response.json() == {"message": "Hello, World!"}


@pytest.mark.anyio
async def test_hello_content_type_is_json(client: AsyncClient) -> None:
    """GET /hello should return a JSON content-type header."""
    response = await client.get("/hello")
    assert "application/json" in response.headers.get("content-type", "")


@pytest.mark.anyio
async def test_hello_post_method_not_allowed(client: AsyncClient) -> None:
    """POST /hello should return 405 Method Not Allowed."""
    response = await client.post("/hello")
    assert response.status_code == 405


@pytest.mark.anyio
async def test_hello_put_method_not_allowed(client: AsyncClient) -> None:
    """PUT /hello should return 405 Method Not Allowed."""
    response = await client.put("/hello")
    assert response.status_code == 405


@pytest.mark.anyio
async def test_hello_delete_method_not_allowed(client: AsyncClient) -> None:
    """DELETE /hello should return 405 Method Not Allowed."""
    response = await client.delete("/hello")
    assert response.status_code == 405


@pytest.mark.anyio
async def test_hello_patch_method_not_allowed(client: AsyncClient) -> None:
    """PATCH /hello should return 405 Method Not Allowed."""
    response = await client.patch("/hello")
    assert response.status_code == 405


@pytest.mark.anyio
async def test_nonexistent_route_returns_404(client: AsyncClient) -> None:
    """GET /nonexistent should return 404 Not Found."""
    response = await client.get("/nonexistent")
    assert response.status_code == 404
