"""Tests for the FastAPI application setup in app.main."""

from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check() -> None:
    """GET /health should return 200 with status ok."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_cors_headers_present() -> None:
    """CORS middleware should add access-control-allow-origin header."""
    response = client.get("/health", headers={"Origin": "http://localhost:3000"})
    assert response.status_code == 200
    assert "access-control-allow-origin" in response.headers
    assert response.headers["access-control-allow-origin"] == "http://localhost:3000"


def test_cors_preflight() -> None:
    """OPTIONS preflight request should succeed with CORS headers."""
    response = client.options(
        "/health",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "GET",
        },
    )
    assert response.status_code == 200
    assert "access-control-allow-origin" in response.headers
