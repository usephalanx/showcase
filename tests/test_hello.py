"""Tests for the GET /hello and GET / endpoints."""

from __future__ import annotations

import datetime

from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_hello_returns_200() -> None:
    """GET /hello must return HTTP 200."""
    response = client.get("/hello")
    assert response.status_code == 200


def test_hello_response_has_message() -> None:
    """The response body must contain message='hello world'."""
    response = client.get("/hello")
    body = response.json()
    assert body["message"] == "hello world"


def test_hello_response_has_iso_timestamp() -> None:
    """The timestamp field must be a valid ISO 8601 string."""
    response = client.get("/hello")
    body = response.json()
    # Will raise ValueError if not a valid ISO 8601 string
    parsed = datetime.datetime.fromisoformat(body["timestamp"])
    assert isinstance(parsed, datetime.datetime)


def test_hello_response_timestamp_is_utc() -> None:
    """The parsed timestamp must carry UTC timezone info (offset == 0)."""
    response = client.get("/hello")
    body = response.json()
    parsed = datetime.datetime.fromisoformat(body["timestamp"])
    assert parsed.tzinfo is not None
    assert parsed.utcoffset() == datetime.timedelta(0)


def test_hello_response_schema_keys() -> None:
    """The response JSON must contain exactly 'message' and 'timestamp'."""
    response = client.get("/hello")
    body = response.json()
    assert set(body.keys()) == {"message", "timestamp"}


def test_root_returns_200() -> None:
    """GET / must return 200 with {'status': 'ok'}."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_hello_method_not_allowed() -> None:
    """POST /hello must return 405 Method Not Allowed."""
    response = client.post("/hello")
    assert response.status_code == 405
