"""Tests for the /health endpoint.

Verifies that GET /health returns 200 with {"status": "ok"} and that
unsupported HTTP methods return 405 Method Not Allowed.
"""

from __future__ import annotations

from fastapi.testclient import TestClient

from main import app


def test_health_returns_ok() -> None:
    """GET /health should return 200 with {"status": "ok"}."""
    client = TestClient(app)
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_health_method_not_allowed() -> None:
    """POST /health should return 405 Method Not Allowed."""
    client = TestClient(app)
    response = client.post("/health")

    assert response.status_code == 405


def test_health_response_content_type() -> None:
    """GET /health should return application/json content type."""
    client = TestClient(app)
    response = client.get("/health")

    assert response.status_code == 200
    assert "application/json" in response.headers["content-type"]


def test_health_put_not_allowed() -> None:
    """PUT /health should return 405 Method Not Allowed."""
    client = TestClient(app)
    response = client.put("/health")

    assert response.status_code == 405


def test_health_delete_not_allowed() -> None:
    """DELETE /health should return 405 Method Not Allowed."""
    client = TestClient(app)
    response = client.delete("/health")

    assert response.status_code == 405


def test_root_returns_welcome() -> None:
    """GET / should return 200 with a welcome message."""
    client = TestClient(app)
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Todo API"}
