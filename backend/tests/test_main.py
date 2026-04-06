"""Tests for the main application entry-point."""

from __future__ import annotations

from fastapi.testclient import TestClient


class TestHealthCheck:
    """Tests for the health check endpoint."""

    def test_health_check(self, client: TestClient) -> None:
        """GET /health should return status ok."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}
