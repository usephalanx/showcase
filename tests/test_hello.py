"""Tests for the GET /hello endpoint."""

from __future__ import annotations

import datetime

from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_hello_returns_200() -> None:
    """GET /hello should return HTTP 200."""
    response = client.get("/hello")
    assert response.status_code == 200


def test_hello_response_has_message_field() -> None:
    """Response body must contain message == 'hello world'."""
    response = client.get("/hello")
    body = response.json()
    assert body["message"] == "hello world"


def test_hello_response_has_timestamp_iso8601() -> None:
    """Response timestamp must be a valid ISO-8601 string with UTC timezone."""
    response = client.get("/hello")
    body = response.json()
    parsed = datetime.datetime.fromisoformat(body["timestamp"])
    assert parsed.tzinfo is not None
    assert parsed.tzinfo.utcoffset(None) == datetime.timedelta(0)


def test_hello_response_keys_exact() -> None:
    """Response body must contain exactly 'message' and 'timestamp' keys."""
    response = client.get("/hello")
    body = response.json()
    assert set(body.keys()) == {"message", "timestamp"}


def test_hello_method_not_allowed_post() -> None:
    """POST /hello should return 405 Method Not Allowed."""
    response = client.post("/hello")
    assert response.status_code == 405
