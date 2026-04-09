"""Tests for the GET /health endpoint."""

from __future__ import annotations

from starlette.testclient import TestClient

from main import app

client = TestClient(app)


def test_health_returns_200() -> None:
    """GET /health should respond with HTTP 200."""
    response = client.get("/health")
    assert response.status_code == 200


def test_health_returns_correct_body() -> None:
    """GET /health should return {"status": "ok"} as JSON."""
    response = client.get("/health")
    assert response.json() == {"status": "ok"}


def test_health_content_type_is_json() -> None:
    """GET /health should return a JSON content-type header."""
    response = client.get("/health")
    assert response.headers["content-type"].startswith("application/json")
