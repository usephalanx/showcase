"""Tests for the health-check endpoint."""

from __future__ import annotations


def test_health_endpoint(client) -> None:  # type: ignore[no-untyped-def]
    """GET /health returns status ok."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
