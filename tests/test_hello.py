"""Tests for the GET /hello endpoint.

Verifies status codes, response body, content type, and correct
behaviour for unknown routes and disallowed HTTP methods.
"""

from __future__ import annotations

from fastapi.testclient import TestClient

from app import app

client: TestClient = TestClient(app)


def test_hello_returns_200_with_message() -> None:
    """GET /hello should return 200 and the expected JSON body."""
    response = client.get("/hello")
    assert response.status_code == 200
    assert response.json() == {"message": "hello world"}


def test_hello_content_type_is_json() -> None:
    """GET /hello should return Content-Type application/json."""
    response = client.get("/hello")
    assert "application/json" in response.headers["content-type"]


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
    """GET to an unregistered path should return 404."""
    response = client.get("/notfound")
    assert response.status_code == 404


def test_hello_response_body_keys() -> None:
    """The response JSON should contain exactly the 'message' key."""
    response = client.get("/hello")
    data = response.json()
    assert list(data.keys()) == ["message"]


def test_hello_message_value_is_string() -> None:
    """The 'message' value should be a string."""
    response = client.get("/hello")
    data = response.json()
    assert isinstance(data["message"], str)
