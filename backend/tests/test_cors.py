"""Dedicated tests for CORS middleware configuration."""

from __future__ import annotations

from fastapi.testclient import TestClient


def test_cors_allows_vite_dev_server_origin(client: TestClient) -> None:
    """The default Vite dev server origin should be allowed."""
    response = client.options(
        "/api/boards",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "GET",
        },
    )
    assert "access-control-allow-origin" in response.headers
    assert response.headers["access-control-allow-origin"] == "http://localhost:5173"


def test_cors_allows_localhost_3000(client: TestClient) -> None:
    """localhost:3000 should also be allowed by default."""
    response = client.options(
        "/api/boards",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "POST",
        },
    )
    assert response.headers.get("access-control-allow-origin") == "http://localhost:3000"


def test_cors_allows_all_methods(client: TestClient) -> None:
    """CORS should allow all HTTP methods."""
    for method in ["GET", "POST", "PUT", "DELETE", "PATCH"]:
        response = client.options(
            "/api/boards",
            headers={
                "Origin": "http://localhost:5173",
                "Access-Control-Request-Method": method,
            },
        )
        allow_methods = response.headers.get("access-control-allow-methods", "")
        assert method in allow_methods or "*" in allow_methods, (
            f"Method {method} should be allowed in CORS"
        )


def test_cors_allows_credentials(client: TestClient) -> None:
    """CORS should include allow-credentials header."""
    response = client.options(
        "/api/boards",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "GET",
        },
    )
    assert response.headers.get("access-control-allow-credentials") == "true"


def test_cors_disallows_unknown_origin(client: TestClient) -> None:
    """An unknown origin should not receive CORS allow-origin header."""
    response = client.options(
        "/api/boards",
        headers={
            "Origin": "http://evil-site.example.com",
            "Access-Control-Request-Method": "GET",
        },
    )
    allow_origin = response.headers.get("access-control-allow-origin")
    # Should either be missing or not match the evil origin
    assert allow_origin != "http://evil-site.example.com"
