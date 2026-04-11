"""Test suite for the /health and /hello API endpoints.

Uses FastAPI's TestClient to verify that each endpoint returns the
expected HTTP status code and JSON payload.
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture()
def client() -> TestClient:
    """Return a TestClient instance wired to the FastAPI application."""
    return TestClient(app)


# --------------------------------------------------------------------------- #
# /health endpoint tests
# --------------------------------------------------------------------------- #


def test_health_endpoint_status_code(client: TestClient) -> None:
    """GET /health must return HTTP 200."""
    response = client.get("/health")
    assert response.status_code == 200


def test_health_endpoint_json_payload(client: TestClient) -> None:
    """GET /health must return {'status': 'ok'}."""
    response = client.get("/health")
    assert response.json() == {"status": "ok"}


def test_health_endpoint_content_type(client: TestClient) -> None:
    """GET /health must return application/json content type."""
    response = client.get("/health")
    assert "application/json" in response.headers["content-type"]


# --------------------------------------------------------------------------- #
# /hello endpoint tests
# --------------------------------------------------------------------------- #


def test_hello_endpoint_status_code(client: TestClient) -> None:
    """GET /hello must return HTTP 200."""
    response = client.get("/hello")
    assert response.status_code == 200


def test_hello_endpoint_json_payload(client: TestClient) -> None:
    """GET /hello must return {'message': 'Hello, world!'}."""
    response = client.get("/hello")
    assert response.json() == {"message": "Hello, world!"}


def test_hello_endpoint_content_type(client: TestClient) -> None:
    """GET /hello must return application/json content type."""
    response = client.get("/hello")
    assert "application/json" in response.headers["content-type"]


# --------------------------------------------------------------------------- #
# Method-not-allowed tests
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize("method", ["post", "put", "patch", "delete"])
def test_health_rejects_non_get_methods(client: TestClient, method: str) -> None:
    """Non-GET requests to /health must return 405 Method Not Allowed."""
    response = getattr(client, method)("/health")
    assert response.status_code == 405


@pytest.mark.parametrize("method", ["post", "put", "patch", "delete"])
def test_hello_rejects_non_get_methods(client: TestClient, method: str) -> None:
    """Non-GET requests to /hello must return 405 Method Not Allowed."""
    response = getattr(client, method)("/hello")
    assert response.status_code == 405
