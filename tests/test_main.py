"""Tests for the root GET / endpoint.

Validates that the hello endpoint returns the correct status code,
JSON body, and content type.
"""

from __future__ import annotations

from fastapi.testclient import TestClient

from main import app

client: TestClient = TestClient(app)


def test_root_returns_200() -> None:
    """GET / must respond with HTTP 200 OK."""
    response = client.get("/")
    assert response.status_code == 200


def test_root_returns_hello_message() -> None:
    """GET / must return {"message": "hello"} as the JSON body."""
    response = client.get("/")
    assert response.json() == {"message": "hello"}


def test_root_content_type_is_json() -> None:
    """GET / response Content-Type must be application/json."""
    response = client.get("/")
    assert "application/json" in response.headers["content-type"]


def test_root_post_not_allowed() -> None:
    """POST / must return HTTP 405 Method Not Allowed."""
    response = client.post("/")
    assert response.status_code == 405


def test_root_put_not_allowed() -> None:
    """PUT / must return HTTP 405 Method Not Allowed."""
    response = client.put("/")
    assert response.status_code == 405


def test_root_delete_not_allowed() -> None:
    """DELETE / must return HTTP 405 Method Not Allowed."""
    response = client.delete("/")
    assert response.status_code == 405


def test_root_response_body_keys() -> None:
    """GET / response body must contain exactly one key: 'message'."""
    response = client.get("/")
    data = response.json()
    assert list(data.keys()) == ["message"]


def test_root_message_value_type() -> None:
    """The 'message' value in the GET / response must be a string."""
    response = client.get("/")
    data = response.json()
    assert isinstance(data["message"], str)
