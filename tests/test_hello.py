"""Tests for the GET /hello endpoint.

Verifies that the endpoint returns HTTP 200 and the expected JSON body.
"""

from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_hello_status_code() -> None:
    """GET /hello should return HTTP 200."""
    response = client.get("/hello")
    assert response.status_code == 200


def test_get_hello_json_body() -> None:
    """GET /hello should return JSON {'message': 'hello'}."""
    response = client.get("/hello")
    assert response.json() == {"message": "hello"}


def test_get_hello_content_type() -> None:
    """GET /hello should return application/json content type."""
    response = client.get("/hello")
    assert "application/json" in response.headers["content-type"]


def test_post_hello_not_allowed() -> None:
    """POST /hello should return HTTP 405 Method Not Allowed."""
    response = client.post("/hello")
    assert response.status_code == 405


def test_nonexistent_endpoint_returns_404() -> None:
    """Requesting a non-existent path should return HTTP 404."""
    response = client.get("/nonexistent")
    assert response.status_code == 404
