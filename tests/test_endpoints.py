"""Tests for the /health and /hello API endpoints.

Uses the FastAPI TestClient to verify correct HTTP status codes
and JSON response bodies.
"""

from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_endpoint_status_code() -> None:
    """GET /health should return HTTP 200."""
    response = client.get("/health")
    assert response.status_code == 200


def test_health_endpoint_json() -> None:
    """GET /health should return {'status': 'ok'}."""
    response = client.get("/health")
    assert response.json() == {"status": "ok"}


def test_hello_endpoint_status_code() -> None:
    """GET /hello should return HTTP 200."""
    response = client.get("/hello")
    assert response.status_code == 200


def test_hello_endpoint_json() -> None:
    """GET /hello should return {'message': 'Hello, world!'}."""
    response = client.get("/hello")
    assert response.json() == {"message": "Hello, world!"}


def test_hello_endpoint_content_type() -> None:
    """GET /hello should return application/json content type."""
    response = client.get("/hello")
    assert "application/json" in response.headers["content-type"]


def test_health_endpoint_content_type() -> None:
    """GET /health should return application/json content type."""
    response = client.get("/health")
    assert "application/json" in response.headers["content-type"]
