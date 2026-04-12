"""Tests for the Hello World API endpoints."""

from __future__ import annotations

import datetime

from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_hello_returns_200() -> None:
    """GET /hello should return HTTP 200."""
    response = client.get("/hello")
    assert response.status_code == 200


def test_hello_response_has_message() -> None:
    """GET /hello response body should contain message 'hello world'."""
    response = client.get("/hello")
    body = response.json()
    assert body["message"] == "hello world"


def test_hello_response_has_iso_timestamp() -> None:
    """GET /hello response timestamp should be valid ISO 8601."""
    response = client.get("/hello")
    body = response.json()
    # Will raise ValueError if the timestamp is not valid ISO format
    parsed = datetime.datetime.fromisoformat(body["timestamp"])
    assert parsed is not None


def test_hello_response_timestamp_is_utc() -> None:
    """GET /hello response timestamp should be UTC (offset +00:00)."""
    response = client.get("/hello")
    body = response.json()
    parsed = datetime.datetime.fromisoformat(body["timestamp"])
    assert parsed.tzinfo is not None
    assert parsed.utcoffset() == datetime.timedelta(0)


def test_hello_response_schema_keys() -> None:
    """GET /hello response should contain exactly 'message' and 'timestamp' keys."""
    response = client.get("/hello")
    body = response.json()
    assert set(body.keys()) == {"message", "timestamp"}


def test_root_returns_200() -> None:
    """GET / should return HTTP 200 with status ok."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_hello_method_not_allowed() -> None:
    """POST /hello should return HTTP 405 Method Not Allowed."""
    response = client.post("/hello")
    assert response.status_code == 405
