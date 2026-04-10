"""Tests for the GET /hello endpoint."""

from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_hello_returns_200() -> None:
    """GET /hello should return HTTP 200."""
    response = client.get("/hello")
    assert response.status_code == 200


def test_get_hello_returns_correct_json() -> None:
    """GET /hello should return JSON body {'message': 'hello'}."""
    response = client.get("/hello")
    assert response.json() == {"message": "hello"}


def test_get_hello_content_type() -> None:
    """GET /hello should return application/json content type."""
    response = client.get("/hello")
    assert "application/json" in response.headers["content-type"]
