"""Tests for the Hello World API endpoints.

Covers the GET /hello and GET / routes, as well as negative cases
such as unsupported methods and non-existent routes.
"""

from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app

client: TestClient = TestClient(app)


# ---------------------------------------------------------------------------
# GET /hello
# ---------------------------------------------------------------------------


def test_get_hello_returns_200() -> None:
    """GET /hello should respond with HTTP 200."""
    response = client.get("/hello")
    assert response.status_code == 200


def test_get_hello_returns_correct_json() -> None:
    """GET /hello should return {"message": "hello-world"}."""
    response = client.get("/hello")
    assert response.json() == {"message": "hello-world"}


def test_get_hello_content_type() -> None:
    """GET /hello should return Content-Type application/json."""
    response = client.get("/hello")
    assert response.headers["content-type"] == "application/json"


# ---------------------------------------------------------------------------
# GET / (health check)
# ---------------------------------------------------------------------------


def test_health_check_returns_200() -> None:
    """GET / should respond with HTTP 200."""
    response = client.get("/")
    assert response.status_code == 200


def test_health_check_returns_ok() -> None:
    """GET / should return {"status": "ok"}."""
    response = client.get("/")
    assert response.json() == {"status": "ok"}


def test_health_check_content_type() -> None:
    """GET / should return Content-Type application/json."""
    response = client.get("/")
    assert response.headers["content-type"] == "application/json"


# ---------------------------------------------------------------------------
# Negative / edge cases
# ---------------------------------------------------------------------------


def test_post_hello_returns_405() -> None:
    """POST /hello should return 405 Method Not Allowed."""
    response = client.post("/hello")
    assert response.status_code == 405


def test_post_root_returns_405() -> None:
    """POST / should return 405 Method Not Allowed."""
    response = client.post("/")
    assert response.status_code == 405


def test_nonexistent_route_returns_404() -> None:
    """GET /nonexistent should return 404 Not Found."""
    response = client.get("/nonexistent")
    assert response.status_code == 404


def test_put_hello_returns_405() -> None:
    """PUT /hello should return 405 Method Not Allowed."""
    response = client.put("/hello")
    assert response.status_code == 405


def test_delete_hello_returns_405() -> None:
    """DELETE /hello should return 405 Method Not Allowed."""
    response = client.delete("/hello")
    assert response.status_code == 405
