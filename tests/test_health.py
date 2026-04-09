"""Tests for the GET /health endpoint.

Validates that the health-check endpoint returns the expected status code,
JSON body, and content-type header.
"""

from __future__ import annotations

from fastapi.testclient import TestClient

from main import app

client: TestClient = TestClient(app)


def test_health_returns_200() -> None:
    """GET /health should return HTTP 200 with {"status": "ok"}."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_health_content_type_json() -> None:
    """GET /health response should have an application/json content-type header."""
    response = client.get("/health")
    content_type: str = response.headers.get("content-type", "")
    assert "application/json" in content_type
