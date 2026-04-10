"""Tests for the /health endpoint.

Verifies that GET /health returns HTTP 200 and the expected JSON body.
"""

from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_returns_200() -> None:
    """GET /health should return HTTP 200."""
    response = client.get("/health")
    assert response.status_code == 200


def test_health_returns_correct_json() -> None:
    """GET /health should return {"status": "ok"}."""
    response = client.get("/health")
    assert response.json() == {"status": "ok"}


def test_health_content_type() -> None:
    """GET /health should return application/json content type."""
    response = client.get("/health")
    assert "application/json" in response.headers["content-type"]


def test_health_post_not_allowed() -> None:
    """POST /health should return HTTP 405 Method Not Allowed."""
    response = client.post("/health")
    assert response.status_code == 405
