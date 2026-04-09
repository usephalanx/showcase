"""Tests for the GET /health endpoint."""

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_health_returns_200() -> None:
    """GET /health should return HTTP 200."""
    response = client.get("/health")
    assert response.status_code == 200


def test_health_returns_expected_body() -> None:
    """GET /health should return {"message": "hi"}."""
    response = client.get("/health")
    assert response.json() == {"message": "hi"}


def test_health_method_not_allowed_post() -> None:
    """POST /health should return HTTP 405 Method Not Allowed."""
    response = client.post("/health")
    assert response.status_code == 405


def test_health_content_type_is_json() -> None:
    """GET /health response should have application/json content type."""
    response = client.get("/health")
    assert "application/json" in response.headers["content-type"]
