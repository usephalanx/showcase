"""Comprehensive tests for the Hello World API /hello endpoint.

Covers:
- GET /hello returns 200
- Response JSON contains 'message' key with value 'hello world'
- Response JSON contains 'timestamp' key with a valid ISO 8601 string (UTC)
- Response body contains exactly the expected keys
- Non-existent routes return 404
- Wrong HTTP method on /hello returns 405
"""

from __future__ import annotations

import datetime

from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_hello_returns_200() -> None:
    """GET /hello must return HTTP 200 OK."""
    response = client.get("/hello")
    assert response.status_code == 200


def test_hello_response_has_message_field() -> None:
    """Response JSON must contain 'message' equal to 'hello world'."""
    response = client.get("/hello")
    body = response.json()
    assert "message" in body
    assert body["message"] == "hello world"


def test_hello_response_has_timestamp_iso8601() -> None:
    """Response JSON must contain 'timestamp' that is a valid ISO 8601 UTC string."""
    response = client.get("/hello")
    body = response.json()
    assert "timestamp" in body

    # Must parse without raising an exception
    parsed = datetime.datetime.fromisoformat(body["timestamp"])

    # Must carry timezone information (UTC)
    assert parsed.tzinfo is not None
    assert parsed.tzinfo == datetime.timezone.utc


def test_hello_response_keys_exact() -> None:
    """Response JSON must contain exactly 'message' and 'timestamp' keys."""
    response = client.get("/hello")
    body = response.json()
    assert set(body.keys()) == {"message", "timestamp"}


def test_hello_timestamp_is_recent() -> None:
    """The returned timestamp should be within a few seconds of 'now'."""
    before = datetime.datetime.now(datetime.timezone.utc)
    response = client.get("/hello")
    after = datetime.datetime.now(datetime.timezone.utc)

    body = response.json()
    ts = datetime.datetime.fromisoformat(body["timestamp"])

    assert before <= ts <= after


def test_hello_content_type_json() -> None:
    """GET /hello must return a JSON content type."""
    response = client.get("/hello")
    assert "application/json" in response.headers["content-type"]


def test_nonexistent_route_returns_404() -> None:
    """A request to a route that does not exist must return 404."""
    response = client.get("/")
    assert response.status_code == 404


def test_nonexistent_route_random_path_returns_404() -> None:
    """A request to an arbitrary undefined path must return 404."""
    response = client.get("/nonexistent")
    assert response.status_code == 404


def test_hello_method_not_allowed_post() -> None:
    """POST /hello must return 405 Method Not Allowed."""
    response = client.post("/hello")
    assert response.status_code == 405


def test_hello_method_not_allowed_put() -> None:
    """PUT /hello must return 405 Method Not Allowed."""
    response = client.put("/hello")
    assert response.status_code == 405


def test_hello_method_not_allowed_delete() -> None:
    """DELETE /hello must return 405 Method Not Allowed."""
    response = client.delete("/hello")
    assert response.status_code == 405


def test_hello_method_not_allowed_patch() -> None:
    """PATCH /hello must return 405 Method Not Allowed."""
    response = client.patch("/hello")
    assert response.status_code == 405
