"""Tests for the Echo API endpoints.

Covers the following scenarios:
- GET  /      returns 200 with {"status": "ok"}
- POST /echo  with a simple JSON object echoes it back
- POST /echo  with a nested JSON object echoes it back
- POST /echo  with an empty JSON object echoes it back
- POST /echo  with a JSON array (non-object) returns 422
- POST /echo  with non-JSON body returns 422
"""

from __future__ import annotations

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


# ---------------------------------------------------------------------------
# GET /  (health check)
# ---------------------------------------------------------------------------


def test_health_returns_200() -> None:
    """GET / should return HTTP 200."""
    response = client.get("/")
    assert response.status_code == 200


def test_health_returns_status_ok() -> None:
    """GET / response body should contain {"status": "ok"}."""
    response = client.get("/")
    assert response.json() == {"status": "ok"}


# ---------------------------------------------------------------------------
# POST /echo  — simple JSON object
# ---------------------------------------------------------------------------


def test_echo_simple_json_status() -> None:
    """POST /echo with a simple JSON object should return HTTP 200."""
    payload = {"message": "hello"}
    response = client.post("/echo", json=payload)
    assert response.status_code == 200


def test_echo_simple_json_body() -> None:
    """POST /echo with a simple JSON object should echo the same object."""
    payload = {"message": "hello"}
    response = client.post("/echo", json=payload)
    assert response.json() == payload


def test_echo_multiple_keys() -> None:
    """POST /echo with multiple top-level keys returns them all unchanged."""
    payload = {"a": 1, "b": "two", "c": True, "d": None}
    response = client.post("/echo", json=payload)
    assert response.status_code == 200
    assert response.json() == payload


# ---------------------------------------------------------------------------
# POST /echo  — nested JSON object
# ---------------------------------------------------------------------------


def test_echo_nested_json_status() -> None:
    """POST /echo with a nested JSON object should return HTTP 200."""
    payload = {
        "user": {
            "name": "Alice",
            "address": {
                "city": "Wonderland",
                "zip": "00000",
            },
        },
        "tags": ["admin", "active"],
    }
    response = client.post("/echo", json=payload)
    assert response.status_code == 200


def test_echo_nested_json_body() -> None:
    """POST /echo with nested JSON should echo the same nested structure."""
    payload = {
        "user": {
            "name": "Alice",
            "address": {
                "city": "Wonderland",
                "zip": "00000",
            },
        },
        "tags": ["admin", "active"],
    }
    response = client.post("/echo", json=payload)
    assert response.json() == payload


def test_echo_deeply_nested_json() -> None:
    """POST /echo with deeply nested JSON preserves structure."""
    payload = {"level1": {"level2": {"level3": {"level4": "deep"}}}}
    response = client.post("/echo", json=payload)
    assert response.status_code == 200
    assert response.json() == payload


# ---------------------------------------------------------------------------
# POST /echo  — empty JSON object
# ---------------------------------------------------------------------------


def test_echo_empty_object_status() -> None:
    """POST /echo with an empty JSON object should return HTTP 200."""
    response = client.post("/echo", json={})
    assert response.status_code == 200


def test_echo_empty_object_body() -> None:
    """POST /echo with an empty JSON object should return {}."""
    response = client.post("/echo", json={})
    assert response.json() == {}


# ---------------------------------------------------------------------------
# POST /echo  — invalid payloads
# ---------------------------------------------------------------------------


def test_echo_rejects_json_array() -> None:
    """POST /echo with a JSON array (not object) should return 422."""
    response = client.post(
        "/echo",
        content='[1, 2, 3]',
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 422


def test_echo_rejects_plain_text() -> None:
    """POST /echo with plain text body should return 422."""
    response = client.post(
        "/echo",
        content="just a string",
        headers={"Content-Type": "text/plain"},
    )
    assert response.status_code == 422


def test_echo_rejects_no_body() -> None:
    """POST /echo with no body should return 422."""
    response = client.post("/echo")
    assert response.status_code == 422
