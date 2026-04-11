"""Tests for the /hello endpoint."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture()
def client() -> TestClient:
    """Return a TestClient instance for the FastAPI app."""
    return TestClient(app)


def test_hello_endpoint_returns_200(client: TestClient) -> None:
    """GET /hello should return HTTP 200."""
    response = client.get("/hello")
    assert response.status_code == 200


def test_hello_endpoint_returns_correct_json(client: TestClient) -> None:
    """GET /hello should return {'message': 'Hello, World!'}."""
    response = client.get("/hello")
    assert response.json() == {"message": "Hello, World!"}


def test_hello_endpoint_content_type(client: TestClient) -> None:
    """GET /hello should return application/json content type."""
    response = client.get("/hello")
    assert "application/json" in response.headers["content-type"]


def test_hello_endpoint_with_query_params(client: TestClient) -> None:
    """GET /hello with unexpected query params still returns correct response."""
    response = client.get("/hello", params={"foo": "bar", "baz": "123"})
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}


def test_nonexistent_endpoint_returns_404(client: TestClient) -> None:
    """Requesting a non-existent endpoint should return 404."""
    response = client.get("/nonexistent")
    assert response.status_code == 404
