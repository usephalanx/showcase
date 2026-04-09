"""Tests for the /echo and / (health) endpoints."""

from __future__ import annotations

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_health_returns_ok() -> None:
    """GET / should return 200 with {"status": "ok"}."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_echo_returns_same_json() -> None:
    """POST /echo with a simple JSON object should echo it back."""
    payload = {"message": "hello"}
    response = client.post("/echo", json=payload)
    assert response.status_code == 200
    assert response.json() == payload


def test_echo_returns_nested_json() -> None:
    """POST /echo with a nested JSON object should echo it back exactly."""
    payload = {
        "user": {
            "name": "Alice",
            "tags": ["admin", "user"],
            "profile": {"age": 30, "active": True},
        },
        "count": 42,
    }
    response = client.post("/echo", json=payload)
    assert response.status_code == 200
    assert response.json() == payload


def test_echo_returns_empty_object() -> None:
    """POST /echo with an empty JSON object should return {}."""
    response = client.post("/echo", json={})
    assert response.status_code == 200
    assert response.json() == {}


def test_echo_rejects_non_json() -> None:
    """POST /echo with plain text should return 422 Unprocessable Entity."""
    response = client.post(
        "/echo",
        content="just a string",
        headers={"Content-Type": "text/plain"},
    )
    assert response.status_code == 422


def test_echo_rejects_json_array() -> None:
    """POST /echo with a JSON array (not object) should return 422."""
    response = client.post("/echo", json=[1, 2, 3])
    assert response.status_code == 422


def test_echo_preserves_numeric_types() -> None:
    """POST /echo should preserve integer and float values."""
    payload = {"int_val": 7, "float_val": 3.14, "negative": -1}
    response = client.post("/echo", json=payload)
    assert response.status_code == 200
    assert response.json() == payload


def test_echo_preserves_boolean_and_null() -> None:
    """POST /echo should preserve booleans and null values."""
    payload = {"flag": True, "other": False, "nothing": None}
    response = client.post("/echo", json=payload)
    assert response.status_code == 200
    assert response.json() == payload


def test_echo_content_type_is_json() -> None:
    """Response from /echo should have application/json content type."""
    response = client.post("/echo", json={"key": "value"})
    assert "application/json" in response.headers["content-type"]


def test_health_content_type_is_json() -> None:
    """Response from / should have application/json content type."""
    response = client.get("/")
    assert "application/json" in response.headers["content-type"]
