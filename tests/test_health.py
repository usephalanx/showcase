"""Tests for the GET /health endpoint.

Validates that the health-check endpoint returns the expected
HTTP 200 status, JSON content type, and {"status": "ok"} body.
"""

from __future__ import annotations

from fastapi.testclient import TestClient

from main import app

client: TestClient = TestClient(app)


def test_health_returns_200() -> None:
    """GET /health must respond with HTTP 200."""
    response = client.get("/health")
    assert response.status_code == 200


def test_health_returns_status_ok() -> None:
    """GET /health must return {"status": "ok"} as JSON body."""
    response = client.get("/health")
    assert response.json() == {"status": "ok"}


def test_health_content_type_json() -> None:
    """GET /health response Content-Type must be application/json."""
    response = client.get("/health")
    content_type = response.headers.get("content-type", "")
    assert "application/json" in content_type
