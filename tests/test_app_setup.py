"""Tests for the application setup and scaffolding.

Verifies that the FastAPI app initialises correctly, CORS middleware
is configured, the router is included, and the root endpoint responds.
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient
from starlette.middleware.cors import CORSMiddleware

from app.main import app


@pytest.fixture()
def client() -> TestClient:
    """Return a TestClient bound to the application."""
    return TestClient(app)


class TestAppInitialisation:
    """Verify basic application configuration."""

    def test_app_title(self) -> None:
        """App title should be set."""
        assert app.title == "Todo API"

    def test_app_version(self) -> None:
        """App version should be set."""
        assert app.version == "1.0.0"

    def test_cors_middleware_present(self) -> None:
        """CORSMiddleware must be registered."""
        middleware_classes = [
            type(m) for m in getattr(app, "user_middleware", [])
        ]
        # FastAPI stores user_middleware as Middleware objects
        # We check the cls attribute instead
        middleware_cls_names = []
        for m in app.user_middleware:
            middleware_cls_names.append(m.cls.__name__)
        assert "CORSMiddleware" in middleware_cls_names


class TestRootEndpoint:
    """Verify the root (/) endpoint."""

    def test_root_returns_200(self, client: TestClient) -> None:
        """GET / should return 200 OK."""
        response = client.get("/")
        assert response.status_code == 200

    def test_root_returns_welcome_message(self, client: TestClient) -> None:
        """GET / should return a JSON welcome message."""
        response = client.get("/")
        data = response.json()
        assert "message" in data
        assert "Welcome" in data["message"]


class TestCORSHeaders:
    """Verify that CORS headers are present on responses."""

    def test_cors_allows_origin(self, client: TestClient) -> None:
        """Response should include Access-Control-Allow-Origin header."""
        response = client.get(
            "/",
            headers={"Origin": "http://example.com"},
        )
        assert response.status_code == 200
        assert "access-control-allow-origin" in response.headers
        assert response.headers["access-control-allow-origin"] == "*"

    def test_cors_preflight(self, client: TestClient) -> None:
        """OPTIONS preflight should succeed with CORS headers."""
        response = client.options(
            "/",
            headers={
                "Origin": "http://example.com",
                "Access-Control-Request-Method": "GET",
            },
        )
        assert response.status_code == 200
        assert "access-control-allow-origin" in response.headers


class TestOpenAPISchema:
    """Verify that OpenAPI schema is generated correctly."""

    def test_openapi_json(self, client: TestClient) -> None:
        """GET /openapi.json should return the schema."""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        schema = response.json()
        assert schema["info"]["title"] == "Todo API"
        assert schema["info"]["version"] == "1.0.0"

    def test_docs_endpoint(self, client: TestClient) -> None:
        """GET /docs should return the Swagger UI page."""
        response = client.get("/docs")
        assert response.status_code == 200
