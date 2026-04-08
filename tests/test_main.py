"""Tests for the main FastAPI application entry point.

Covers the root GET / endpoint and verifies the app metadata.
"""

from __future__ import annotations

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_root_returns_welcome_message() -> None:
    """GET / should return 200 with a welcome message."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Welcome" in data["message"]


def test_root_response_content_type() -> None:
    """GET / should return application/json content."""
    response = client.get("/")
    assert "application/json" in response.headers["content-type"]


def test_app_title() -> None:
    """The app title should be set correctly."""
    assert app.title == "Todo API"


def test_app_description() -> None:
    """The app description should be set correctly."""
    assert app.description == "A simple Todo REST API with in-memory storage."


def test_app_version() -> None:
    """The app version should be set correctly."""
    assert app.version == "1.0.0"
