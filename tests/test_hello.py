"""Tests for the GET /hello endpoint.

Uses starlette.testclient.TestClient (shipped with FastAPI) to exercise
the hello-world application without starting a real server.
"""

from __future__ import annotations

from starlette.testclient import TestClient

from app import app

client = TestClient(app)


def test_hello_returns_200_with_message() -> None:
    """GET /hello should return 200 and the expected JSON body."""
    response = client.get("/hello")
    assert response.status_code == 200
    assert response.json() == {"message": "hello world"}


def test_hello_content_type_is_json() -> None:
    """GET /hello response Content-Type must be application/json."""
    response = client.get("/hello")
    content_type = response.headers.get("content-type", "")
    assert "application/json" in content_type


def test_hello_post_returns_405() -> None:
    """POST /hello should return 405 Method Not Allowed."""
    response = client.post("/hello")
    assert response.status_code == 405


def test_hello_put_returns_405() -> None:
    """PUT /hello should return 405 Method Not Allowed."""
    response = client.put("/hello")
    assert response.status_code == 405


def test_hello_delete_returns_405() -> None:
    """DELETE /hello should return 405 Method Not Allowed."""
    response = client.delete("/hello")
    assert response.status_code == 405


def test_unknown_route_returns_404() -> None:
    """GET /notfound should return 404 Not Found."""
    response = client.get("/notfound")
    assert response.status_code == 404
