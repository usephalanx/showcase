"""Tests for the FastAPI application instance and CORS configuration.

Uses the httpx AsyncClient via FastAPI's TestClient to verify that the
app starts correctly and CORS headers are present for allowed origins.
"""

from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_app_instance_exists() -> None:
    """The FastAPI app should be importable and have the expected title."""
    assert app.title == "Todo API"


def test_app_version() -> None:
    """The app version should be 1.0.0."""
    assert app.version == "1.0.0"


def test_cors_allows_localhost_5173() -> None:
    """CORS should include Access-Control-Allow-Origin for localhost:5173."""
    response = client.options(
        "/",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "GET",
        },
    )
    assert response.headers.get("access-control-allow-origin") == "http://localhost:5173"


def test_cors_rejects_unknown_origin() -> None:
    """CORS should not include Access-Control-Allow-Origin for unknown origins."""
    response = client.options(
        "/",
        headers={
            "Origin": "http://evil.example.com",
            "Access-Control-Request-Method": "GET",
        },
    )
    assert response.headers.get("access-control-allow-origin") != "http://evil.example.com"


def test_cors_allows_all_methods() -> None:
    """CORS should allow all HTTP methods for the permitted origin."""
    response = client.options(
        "/",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "DELETE",
        },
    )
    allow_methods = response.headers.get("access-control-allow-methods", "")
    assert "DELETE" in allow_methods or "*" in allow_methods


def test_cors_allows_credentials() -> None:
    """CORS should indicate that credentials are allowed."""
    response = client.options(
        "/",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "GET",
        },
    )
    assert response.headers.get("access-control-allow-credentials") == "true"


def test_tables_created_on_startup() -> None:
    """Database tables should be created when the app starts."""
    from sqlalchemy import inspect as sa_inspect

    from app.database import engine

    inspector = sa_inspect(engine)
    tables = inspector.get_table_names()
    assert "tasks" in tables


def test_openapi_schema_available() -> None:
    """The OpenAPI JSON schema should be accessible."""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    data = response.json()
    assert data["info"]["title"] == "Todo API"
