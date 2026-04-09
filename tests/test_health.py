"""Tests for the GET /health endpoint."""

from __future__ import annotations

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_health_returns_200() -> None:
    """GET /health should respond with HTTP 200."""
    response = client.get("/health")
    assert response.status_code == 200


def test_health_returns_status_ok() -> None:
    """GET /health should return {"status": "ok"} JSON body."""
    response = client.get("/health")
    assert response.json() == {"status": "ok"}


def test_health_content_type_json() -> None:
    """GET /health response Content-Type should be application/json."""
    response = client.get("/health")
    assert "application/json" in response.headers["content-type"]
