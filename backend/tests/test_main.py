"""Tests for the FastAPI application startup and health endpoint."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture()
def client() -> TestClient:
    """Return a TestClient with lifespan events enabled."""
    with TestClient(app) as c:
        yield c


class TestHealthCheck:
    """Tests for the /health endpoint."""

    def test_health_returns_ok(self, client: TestClient) -> None:
        """GET /health should return 200 with status ok."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data == {"status": "ok"}
