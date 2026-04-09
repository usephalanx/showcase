"""Tests for the GET / endpoint of the Hello API.

Uses FastAPI's TestClient (backed by httpx) to exercise the endpoint
without starting a real server.
"""

from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root_returns_200() -> None:
    """GET / must respond with HTTP 200 OK."""
    response = client.get("/")
    assert response.status_code == 200


def test_root_returns_hello_message() -> None:
    """GET / must return JSON body {"message": "hello"}."""
    response = client.get("/")
    assert response.json() == {"message": "hello"}


def test_root_content_type_is_json() -> None:
    """GET / must set Content-Type to application/json."""
    response = client.get("/")
    assert "application/json" in response.headers["content-type"]


def test_post_root_returns_405() -> None:
    """POST / must return 405 Method Not Allowed."""
    response = client.post("/")
    assert response.status_code == 405
