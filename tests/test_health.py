"""Tests for the /health endpoint."""

from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_returns_200() -> None:
    """GET /health should return HTTP 200."""
    response = client.get("/health")
    assert response.status_code == 200


def test_health_returns_ok_status() -> None:
    """GET /health should return JSON body {"status": "ok"}."""
    response = client.get("/health")
    assert response.json() == {"status": "ok"}


def test_health_content_type_is_json() -> None:
    """GET /health should return application/json content type."""
    response = client.get("/health")
    assert "application/json" in response.headers["content-type"]


def test_health_post_not_allowed() -> None:
    """POST /health should return 405 Method Not Allowed."""
    response = client.post("/health")
    assert response.status_code == 405


def test_health_put_not_allowed() -> None:
    """PUT /health should return 405 Method Not Allowed."""
    response = client.put("/health")
    assert response.status_code == 405


def test_health_delete_not_allowed() -> None:
    """DELETE /health should return 405 Method Not Allowed."""
    response = client.delete("/health")
    assert response.status_code == 405
