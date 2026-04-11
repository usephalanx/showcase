"""Tests for the /hello endpoint in app.main.

Covers:
- GET /hello returns 200 with correct JSON body.
- POST /hello returns 405 Method Not Allowed.
- PUT /hello returns 405 Method Not Allowed.
- DELETE /hello returns 405 Method Not Allowed.
- PATCH /hello returns 405 Method Not Allowed.
- GET on a non-existent path returns 404.
- Response Content-Type is application/json.
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
    """Create an async HTTP client wired to the FastAPI app."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
        yield ac


@pytest.mark.anyio
async def test_hello_returns_hello_world(client: AsyncClient) -> None:
    """GET /hello must return 200 with {'message': 'Hello, World!'}."""
    response = await client.get("/hello")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}


@pytest.mark.anyio
async def test_hello_response_content_type(client: AsyncClient) -> None:
    """GET /hello must return application/json content type."""
    response = await client.get("/hello")
    assert "application/json" in response.headers["content-type"]


@pytest.mark.anyio
async def test_hello_post_method_not_allowed(client: AsyncClient) -> None:
    """POST /hello must return 405 Method Not Allowed."""
    response = await client.post("/hello")
    assert response.status_code == 405


@pytest.mark.anyio
async def test_hello_put_method_not_allowed(client: AsyncClient) -> None:
    """PUT /hello must return 405 Method Not Allowed."""
    response = await client.put("/hello")
    assert response.status_code == 405


@pytest.mark.anyio
async def test_hello_delete_method_not_allowed(client: AsyncClient) -> None:
    """DELETE /hello must return 405 Method Not Allowed."""
    response = await client.delete("/hello")
    assert response.status_code == 405


@pytest.mark.anyio
async def test_hello_patch_method_not_allowed(client: AsyncClient) -> None:
    """PATCH /hello must return 405 Method Not Allowed."""
    response = await client.patch("/hello")
    assert response.status_code == 405


@pytest.mark.anyio
async def test_nonexistent_path_returns_404(client: AsyncClient) -> None:
    """GET on a non-existent path must return 404."""
    response = await client.get("/nonexistent")
    assert response.status_code == 404
