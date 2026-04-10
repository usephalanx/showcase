"""Tests for the /hello endpoint.

Verifies that GET /hello returns HTTP 200 and the expected JSON body.
"""

from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_hello_returns_200() -> None:
    """GET /hello should return HTTP 200."""
    response = client.get("/hello")
    assert response.status_code == 200


def test_hello_returns_correct_json() -> None:
    """GET /hello should return {"message": "hello world"}."""
    response = client.get("/hello")
    assert response.json() == {"message": "hello world"}


def test_hello_with_query_params() -> None:
    """GET /hello with extra query parameters should still return correct response."""
    response = client.get("/hello", params={"extra": "param"})
    assert response.status_code == 200
    assert response.json() == {"message": "hello world"}


def test_hello_content_type() -> None:
    """GET /hello should return application/json content type."""
    response = client.get("/hello")
    assert "application/json" in response.headers["content-type"]
