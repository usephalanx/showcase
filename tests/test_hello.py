"""Automated tests for the GET /hello endpoint.

Uses Starlette's TestClient to exercise the endpoint without starting
a real server.
"""

from __future__ import annotations

from starlette.testclient import TestClient

from app import app

client = TestClient(app)


def test_hello_returns_200() -> None:
    """GET /hello should respond with HTTP 200."""
    response = client.get("/hello")
    assert response.status_code == 200


def test_hello_returns_correct_body() -> None:
    """GET /hello should return the expected JSON payload."""
    response = client.get("/hello")
    assert response.json() == {"message": "hello world"}


def test_hello_content_type_is_json() -> None:
    """GET /hello should return a JSON content-type header."""
    response = client.get("/hello")
    assert "application/json" in response.headers["content-type"]


def test_hello_method_not_allowed_post() -> None:
    """POST /hello should return HTTP 405 Method Not Allowed."""
    response = client.post("/hello")
    assert response.status_code == 405


def test_nonexistent_route_returns_404() -> None:
    """GET /nonexistent should return HTTP 404 Not Found."""
    response = client.get("/nonexistent")
    assert response.status_code == 404


def test_hello_with_query_params_ignored() -> None:
    """GET /hello?foo=bar should still return 200 with the correct body."""
    response = client.get("/hello", params={"foo": "bar"})
    assert response.status_code == 200
    assert response.json() == {"message": "hello world"}


def test_hello_head_returns_200() -> None:
    """HEAD /hello should return HTTP 200 with an empty body."""
    response = client.head("/hello")
    assert response.status_code == 200
    assert response.content == b""
