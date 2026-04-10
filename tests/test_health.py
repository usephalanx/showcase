"""Test suite for the /health endpoint.

Verifies that the GET /health endpoint returns HTTP 200 with the
expected JSON body {"status": "ok"}.
"""

from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app

client: TestClient = TestClient(app)


def test_health_returns_200() -> None:
    """GET /health must return HTTP 200 status code."""
    response = client.get("/health")
    assert response.status_code == 200


def test_health_returns_correct_json() -> None:
    """GET /health must return JSON body {"status": "ok"}."""
    response = client.get("/health")
    assert response.json() == {"status": "ok"}


def test_health_content_type_is_json() -> None:
    """GET /health must return application/json content type."""
    response = client.get("/health")
    assert "application/json" in response.headers["content-type"]


def test_health_post_method_not_allowed() -> None:
    """POST /health must return 405 Method Not Allowed."""
    response = client.post("/health")
    assert response.status_code == 405


def test_health_put_method_not_allowed() -> None:
    """PUT /health must return 405 Method Not Allowed."""
    response = client.put("/health")
    assert response.status_code == 405


def test_health_delete_method_not_allowed() -> None:
    """DELETE /health must return 405 Method Not Allowed."""
    response = client.delete("/health")
    assert response.status_code == 405


def test_health_patch_method_not_allowed() -> None:
    """PATCH /health must return 405 Method Not Allowed."""
    response = client.patch("/health")
    assert response.status_code == 405
