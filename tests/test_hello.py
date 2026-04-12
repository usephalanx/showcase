"""Test suite for the Hello World API.

Covers:
- GET /hello returns 200
- Response JSON contains 'message' key with value 'hello world'
- Response JSON contains 'timestamp' key that is a valid ISO 8601 string
- Timestamp is UTC-aware
- Response schema has exactly the expected keys
- GET / health-check returns 200
- POST /hello returns 405 (Method Not Allowed)
- GET on a non-existent route returns 404
"""

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
    """Response body must contain 'message' equal to 'hello world'."""
    response = client.get("/hello")
    body = response.json()
    assert "message" in body
    assert body["message"] == "hello world"


def test_hello_response_has_iso_timestamp() -> None:
    """Response body must contain 'timestamp' that is a valid ISO 8601 string."""
    response = client.get("/hello")
    body = response.json()
    assert "timestamp" in body
    # datetime.fromisoformat will raise ValueError for non-ISO strings
    parsed = datetime.datetime.fromisoformat(body["timestamp"])
    assert isinstance(parsed, datetime.datetime)


def test_hello_response_timestamp_is_utc() -> None:
    """Parsed timestamp must be timezone-aware with UTC offset of zero."""
    response = client.get("/hello")
    body = response.json()
    parsed = datetime.datetime.fromisoformat(body["timestamp"])
    assert parsed.tzinfo is not None
    assert parsed.utcoffset() == datetime.timedelta(0)


def test_hello_response_schema_keys() -> None:
    """Response JSON must contain exactly 'message' and 'timestamp' keys."""
    response = client.get("/hello")
    body = response.json()
    assert set(body.keys()) == {"message", "timestamp"}


def test_root_returns_200() -> None:
    """GET / health-check must return 200 with {'status': 'ok'}."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_hello_method_not_allowed() -> None:
    """POST /hello must return 405 Method Not Allowed."""
    response = client.post("/hello")
    assert response.status_code == 405


def test_nonexistent_route_returns_404() -> None:
    """GET on a route that does not exist must return 404."""
    response = client.get("/nonexistent-route")
    assert response.status_code == 404
