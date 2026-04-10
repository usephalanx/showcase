"""Tests for the /hello endpoint."""

from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_hello_returns_hello_world() -> None:
    """GET /hello should return 200 with the expected greeting JSON."""
    response = client.get("/hello")
    assert response.status_code == 200
    assert response.json() == {"message": "hello world"}


def test_hello_with_extra_query_params() -> None:
    """GET /hello with extra query parameters should still return 200 and correct JSON."""
    response = client.get("/hello", params={"foo": "bar", "baz": "1"})
    assert response.status_code == 200
    assert response.json() == {"message": "hello world"}


def test_hello_post_not_allowed() -> None:
    """POST /hello should return 405 Method Not Allowed."""
    response = client.post("/hello")
    assert response.status_code == 405
