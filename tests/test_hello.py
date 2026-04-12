"""Tests for the GET /hello endpoint."""

from __future__ import annotations

import datetime

from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_hello_returns_200() -> None:
    """GET /hello must return HTTP 200."""
    response = client.get("/hello")
    assert response.status_code == 200


def test_hello_response_has_message_field() -> None:
    """Response body must contain 'message' equal to 'hello world'."""
    response = client.get("/hello")
    body = response.json()
    assert body["message"] == "hello world"


def test_hello_response_has_timestamp_iso8601() -> None:
    """Response 'timestamp' must be a valid ISO-8601 string ending in 'Z'."""
    response = client.get("/hello")
    body = response.json()
    ts = body["timestamp"]
    assert ts.endswith("Z")
    # Must parse without error; strip trailing Z for fromisoformat on 3.10
    parsed = datetime.datetime.fromisoformat(ts.replace("Z", "+00:00"))
    assert parsed.tzinfo is not None


def test_hello_response_keys_exact() -> None:
    """Response body must contain exactly the keys 'message' and 'timestamp'."""
    response = client.get("/hello")
    body = response.json()
    assert set(body.keys()) == {"message", "timestamp"}


def test_hello_method_not_allowed_post() -> None:
    """POST /hello must return 405 Method Not Allowed."""
    response = client.post("/hello")
    assert response.status_code == 405
