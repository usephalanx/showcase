"""Tests for the /hello endpoint and FastAPI app basics.

Covers:
- GET /hello returns 200 with correct JSON body
- GET /hello with unexpected query params still succeeds
- Non-existent routes return 404
- App metadata is configured correctly
"""

from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.fixture
def client() -> AsyncClient:
    """Create an async HTTP client bound to the FastAPI app."""
    transport = ASGITransport(app=app)
    return AsyncClient(transport=transport, base_url="http://testserver")


@pytest.mark.anyio
async def test_hello_endpoint_returns_200(client: AsyncClient) -> None:
    """GET /hello should return HTTP 200."""
    response = await client.get("/hello")
    assert response.status_code == 200


@pytest.mark.anyio
async def test_hello_endpoint_returns_correct_json(client: AsyncClient) -> None:
    """GET /hello should return the expected JSON body."""
    response = await client.get("/hello")
    data = response.json()
    assert data == {"message": "Hello, World!"}


@pytest.mark.anyio
async def test_hello_endpoint_content_type(client: AsyncClient) -> None:
    """GET /hello should return application/json content type."""
    response = await client.get("/hello")
    assert "application/json" in response.headers["content-type"]


@pytest.mark.anyio
async def test_hello_endpoint_with_query_params(client: AsyncClient) -> None:
    """GET /hello with unexpected query params should still return 200 and correct JSON."""
    response = await client.get("/hello", params={"foo": "bar", "baz": "123"})
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}


@pytest.mark.anyio
async def test_nonexistent_route_returns_404(client: AsyncClient) -> None:
    """GET on a non-existent route should return HTTP 404."""
    response = await client.get("/nonexistent")
    assert response.status_code == 404


@pytest.mark.anyio
async def test_hello_post_method_not_allowed(client: AsyncClient) -> None:
    """POST /hello should return HTTP 405 Method Not Allowed."""
    response = await client.post("/hello")
    assert response.status_code == 405


@pytest.mark.anyio
async def test_hello_put_method_not_allowed(client: AsyncClient) -> None:
    """PUT /hello should return HTTP 405 Method Not Allowed."""
    response = await client.put("/hello")
    assert response.status_code == 405


@pytest.mark.anyio
async def test_hello_delete_method_not_allowed(client: AsyncClient) -> None:
    """DELETE /hello should return HTTP 405 Method Not Allowed."""
    response = await client.delete("/hello")
    assert response.status_code == 405


def test_app_title() -> None:
    """The app title should be set correctly."""
    assert app.title == "Hello World API"


def test_app_version() -> None:
    """The app version should be set correctly."""
    assert app.version == "1.0.0"


def test_app_description() -> None:
    """The app description should be set correctly."""
    assert app.description == "A simple FastAPI application with a /hello endpoint."


@pytest.mark.anyio
async def test_hello_response_message_key_exists(client: AsyncClient) -> None:
    """GET /hello response must contain the 'message' key."""
    response = await client.get("/hello")
    data = response.json()
    assert "message" in data


@pytest.mark.anyio
async def test_hello_response_message_value_type(client: AsyncClient) -> None:
    """GET /hello 'message' value must be a string."""
    response = await client.get("/hello")
    data = response.json()
    assert isinstance(data["message"], str)


@pytest.mark.anyio
async def test_hello_response_has_single_key(client: AsyncClient) -> None:
    """GET /hello response should contain exactly one key."""
    response = await client.get("/hello")
    data = response.json()
    assert len(data) == 1


@pytest.mark.anyio
async def test_openapi_schema_available(client: AsyncClient) -> None:
    """The OpenAPI schema endpoint should be accessible."""
    response = await client.get("/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    assert "paths" in schema
    assert "/hello" in schema["paths"]
