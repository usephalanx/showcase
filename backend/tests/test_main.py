"""Tests for the main FastAPI application entry point.

Covers health check, CORS headers, and router registration.
"""

from __future__ import annotations

from fastapi.testclient import TestClient


def test_health_check(client: TestClient) -> None:
    """GET /health returns 200 with status ok."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data == {"status": "ok"}


def test_cors_headers_on_preflight(client: TestClient) -> None:
    """OPTIONS request from allowed origin returns CORS headers."""
    response = client.options(
        "/health",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "GET",
            "Access-Control-Request-Headers": "Content-Type",
        },
    )
    assert response.status_code == 200
    assert "access-control-allow-origin" in response.headers
    assert response.headers["access-control-allow-origin"] == "http://localhost:5173"


def test_cors_headers_on_simple_request(client: TestClient) -> None:
    """GET request from allowed origin includes CORS allow-origin header."""
    response = client.get(
        "/health",
        headers={"Origin": "http://localhost:5173"},
    )
    assert response.status_code == 200
    assert response.headers.get("access-control-allow-origin") == "http://localhost:5173"


def test_boards_router_registered(client: TestClient) -> None:
    """GET /api/boards returns 200 (router is mounted)."""
    response = client.get("/api/boards")
    assert response.status_code == 200


def test_categories_router_registered(client: TestClient) -> None:
    """GET /api/categories returns 200 (router is mounted)."""
    response = client.get("/api/categories")
    assert response.status_code == 200


def test_cards_router_registered(client: TestClient) -> None:
    """GET /api/cards returns 200 (router is mounted)."""
    response = client.get("/api/cards")
    assert response.status_code == 200


def test_openapi_schema_available(client: TestClient) -> None:
    """GET /openapi.json returns a valid OpenAPI schema."""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    assert "paths" in schema
    assert schema["info"]["title"] == "Kanban Board API"
