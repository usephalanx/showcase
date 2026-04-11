"""Tests for the GET /hello endpoint."""

from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_hello_endpoint_returns_200() -> None:
    """GET /hello should return HTTP 200."""
    response = client.get("/hello")
    assert response.status_code == 200


def test_hello_endpoint_returns_correct_json() -> None:
    """GET /hello should return {'message': 'Hello, World!'}."""
    response = client.get("/hello")
    assert response.json() == {"message": "Hello, World!"}


def test_hello_endpoint_content_type() -> None:
    """GET /hello should return application/json content type."""
    response = client.get("/hello")
    assert "application/json" in response.headers["content-type"]


def test_hello_endpoint_post_not_allowed() -> None:
    """POST /hello should return HTTP 405 Method Not Allowed."""
    response = client.post("/hello")
    assert response.status_code == 405


def test_nonexistent_endpoint_returns_404() -> None:
    """GET /nonexistent should return HTTP 404."""
    response = client.get("/nonexistent")
    assert response.status_code == 404
