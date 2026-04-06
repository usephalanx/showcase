"""Tests for the FastAPI application entry point (backend/main.py).

Covers application instantiation, CORS configuration, startup table
creation, and router inclusion.
"""

from __future__ import annotations

import importlib
from typing import Generator

import pytest
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.testclient import TestClient

from backend.main import ALLOWED_ORIGINS, app


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def client() -> Generator[TestClient, None, None]:
    """Provide a ``TestClient`` that triggers the app lifespan events."""
    with TestClient(app) as c:
        yield c


# ---------------------------------------------------------------------------
# Application instance tests
# ---------------------------------------------------------------------------


def test_app_is_fastapi_instance() -> None:
    """The ``app`` object must be a FastAPI instance."""
    assert isinstance(app, FastAPI)


def test_app_title() -> None:
    """The app title should be set to 'Todo API'."""
    assert app.title == "Todo API"


def test_app_version() -> None:
    """The app version should be '1.0.0'."""
    assert app.version == "1.0.0"


# ---------------------------------------------------------------------------
# CORS middleware tests
# ---------------------------------------------------------------------------


def test_allowed_origins_contains_vite_dev_server() -> None:
    """localhost:5173 must be in the allowed-origins list."""
    assert "http://localhost:5173" in ALLOWED_ORIGINS


def test_cors_middleware_is_registered() -> None:
    """CORSMiddleware must be present in the middleware stack."""
    # FastAPI wraps middleware; walk the middleware stack to find CORS.
    middleware_classes = [type(m) for m in app.user_middleware]
    # user_middleware stores Middleware objects; check their cls attribute
    cors_found = any(
        getattr(m, "cls", None) is CORSMiddleware
        for m in app.user_middleware
    )
    assert cors_found, (
        f"CORSMiddleware not found in user_middleware: {middleware_classes}"
    )


def test_cors_preflight_returns_allow_origin(client: TestClient) -> None:
    """An OPTIONS preflight from the Vite origin should be accepted."""
    response = client.options(
        "/health",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "GET",
        },
    )
    assert response.status_code == 200
    assert (
        response.headers.get("access-control-allow-origin")
        == "http://localhost:5173"
    )


def test_cors_disallows_unknown_origin(client: TestClient) -> None:
    """An OPTIONS preflight from an unknown origin should not echo it."""
    response = client.options(
        "/health",
        headers={
            "Origin": "http://evil.example.com",
            "Access-Control-Request-Method": "GET",
        },
    )
    assert response.headers.get("access-control-allow-origin") != "http://evil.example.com"


# ---------------------------------------------------------------------------
# Router inclusion tests
# ---------------------------------------------------------------------------


def test_health_endpoint(client: TestClient) -> None:
    """The /health endpoint should return {"status": "ok"}."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_router_is_included() -> None:
    """Routes from backend.routes must be registered on the app."""
    paths = [route.path for route in app.routes]
    assert "/health" in paths


# ---------------------------------------------------------------------------
# Startup / lifespan tests
# ---------------------------------------------------------------------------


def test_startup_creates_tables(client: TestClient) -> None:
    """After startup the 'tasks' table must exist in the database."""
    from backend.database import engine
    from sqlalchemy import inspect

    inspector = inspect(engine)
    table_names = inspector.get_table_names()
    assert "tasks" in table_names


# ---------------------------------------------------------------------------
# Module importability
# ---------------------------------------------------------------------------


def test_main_module_importable() -> None:
    """backend.main must be importable without errors."""
    mod = importlib.import_module("backend.main")
    assert hasattr(mod, "app")


def test_routes_module_importable() -> None:
    """backend.routes must be importable without errors."""
    mod = importlib.import_module("backend.routes")
    assert hasattr(mod, "router")
