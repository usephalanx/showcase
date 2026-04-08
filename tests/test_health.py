"""Tests for the health-check endpoint."""

from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app


def test_health_check() -> None:
    """GET /health returns 200 with status ok."""
    client = TestClient(app)
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}
