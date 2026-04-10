"""Tests for the /health endpoint."""

from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_returns_ok() -> None:
    """GET /health should return 200 with status ok JSON."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_health_post_not_allowed() -> None:
    """POST /health should return 405 Method Not Allowed."""
    response = client.post("/health")
    assert response.status_code == 405
