"""Test suite verifying all endpoint behaviour.

Uses FastAPI's synchronous TestClient to exercise the /hello and /
endpoints, including positive and negative scenarios.
"""

from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


# ------------------------------------------------------------------
# GET /hello
# ------------------------------------------------------------------


def test_get_hello_returns_200() -> None:
    """GET /hello should return HTTP 200."""
    response = client.get("/hello")
    assert response.status_code == 200


def test_get_hello_returns_correct_json() -> None:
    """GET /hello should return {"message": "hello-world"}."""
    response = client.get("/hello")
    assert response.json() == {"message": "hello-world"}


def test_get_hello_content_type() -> None:
    """GET /hello should return Content-Type application/json."""
    response = client.get("/hello")
    assert "application/json" in response.headers["content-type"]


# ------------------------------------------------------------------
# GET / (health check)
# ------------------------------------------------------------------


def test_health_check_returns_200() -> None:
    """GET / should return HTTP 200."""
    response = client.get("/")
    assert response.status_code == 200


def test_health_check_returns_ok() -> None:
    """GET / should return {"status": "ok"}."""
    response = client.get("/")
    assert response.json() == {"status": "ok"}


# ------------------------------------------------------------------
# Negative / edge-case tests
# ------------------------------------------------------------------


def test_post_hello_returns_405() -> None:
    """POST /hello should return HTTP 405 Method Not Allowed."""
    response = client.post("/hello")
    assert response.status_code == 405


def test_nonexistent_route_returns_404() -> None:
    """GET /nonexistent should return HTTP 404 Not Found."""
    response = client.get("/nonexistent")
    assert response.status_code == 404
