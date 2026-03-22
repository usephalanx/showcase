"""Tests for the main application setup and global error handling."""

from __future__ import annotations

from fastapi.testclient import TestClient


class TestGlobalErrorHandler:
    """Verify that the global exception handler catches unexpected errors."""

    def test_unhandled_exception_returns_500(self, client: TestClient) -> None:
        """Simulated unhandled errors produce a 500 JSON response."""
        from backend.app.main import app
        from fastapi import APIRouter

        _error_router = APIRouter()

        @_error_router.get("/api/_test_error")
        def _boom() -> None:
            """Intentionally raise to test the global handler."""
            raise RuntimeError("boom")

        app.include_router(_error_router)
        resp = client.get("/api/_test_error")
        assert resp.status_code == 500
        assert resp.json()["detail"] == "Internal server error"


class TestCORSHeaders:
    """Verify CORS middleware is active."""

    def test_cors_allows_origin(self, client: TestClient) -> None:
        """OPTIONS request includes CORS headers."""
        resp = client.options(
            "/api/projects",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "GET",
            },
        )
        # CORS middleware should respond
        assert resp.status_code == 200
        assert "access-control-allow-origin" in resp.headers
