"""Tests for the GET /hello endpoint.

Verifies status codes, response body, content type, and correct
behaviour for edge cases (wrong method, unknown routes).
"""

from __future__ import annotations

from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_hello_returns_200_with_message() -> None:
    """GET /hello should return 200 with {"message": "hello world"}."""
    response = client.get("/hello")
    assert response.status_code == 200
    assert response.json() == {"message": "hello world"}


def test_hello_content_type_is_json() -> None:
    """GET /hello response Content-Type must be application/json."""
    response = client.get("/hello")
    assert "application/json" in response.headers["content-type"]


def test_hello_message_key_exists() -> None:
    """Response JSON must contain exactly the 'message' key."""
    response = client.get("/hello")
    data = response.json()
    assert "message" in data
    assert data["message"] == "hello world"


def test_hello_post_returns_405() -> None:
    """POST /hello should return 405 Method Not Allowed."""
    response = client.post("/hello")
    assert response.status_code == 405


def test_hello_put_returns_405() -> None:
    """PUT /hello should return 405 Method Not Allowed."""
    response = client.put("/hello")
    assert response.status_code == 405


def test_hello_delete_returns_405() -> None:
    """DELETE /hello should return 405 Method Not Allowed."""
    response = client.delete("/hello")
    assert response.status_code == 405


def test_unknown_route_returns_404() -> None:
    """GET /nonexistent should return 404."""
    response = client.get("/nonexistent")
    assert response.status_code == 404


def test_hello_response_body_is_dict() -> None:
    """Response body should deserialise to a dict with one key."""
    response = client.get("/hello")
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) == 1
