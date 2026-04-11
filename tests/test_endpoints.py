"""Tests for the /health and /hello endpoints.

Uses FastAPI's TestClient to verify correct HTTP status codes
and JSON response bodies.
"""

from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_endpoint() -> None:
    """GET /health returns 200 and {'status': 'ok'}."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_health_endpoint_content_type() -> None:
    """GET /health returns application/json content type."""
    response = client.get("/health")
    assert "application/json" in response.headers["content-type"]


def test_hello_endpoint() -> None:
    """GET /hello returns 200 and {'message': 'Hello, world!'}."""
    response = client.get("/hello")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, world!"}


def test_hello_endpoint_content_type() -> None:
    """GET /hello returns application/json content type."""
    response = client.get("/hello")
    assert "application/json" in response.headers["content-type"]


def test_health_post_not_allowed() -> None:
    """POST /health returns 405 Method Not Allowed."""
    response = client.post("/health")
    assert response.status_code == 405


def test_hello_post_not_allowed() -> None:
    """POST /hello returns 405 Method Not Allowed."""
    response = client.post("/hello")
    assert response.status_code == 405
