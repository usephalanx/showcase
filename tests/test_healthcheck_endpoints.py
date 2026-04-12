"""Tests for the healthcheck FastAPI app (healthcheck/e36e389f/main.py).

Covers: serving index.html, /api/todos CRUD endpoints, and toggle endpoint.
Uses a temporary database to isolate tests.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Dict
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

_HC_DIR = str(Path(__file__).resolve().parent.parent / "healthcheck" / "e36e389f")
if _HC_DIR not in sys.path:
    sys.path.insert(0, _HC_DIR)


@pytest.fixture(autouse=True)
def _patch_database(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Patch the database path to use a temporary file for each test."""
    import database

    db_path = tmp_path / "hc_test_todos.db"
    monkeypatch.setattr(database, "DATABASE_PATH", str(db_path))
    database.init_db()


@pytest.fixture()
def hc_client() -> TestClient:
    """Return a TestClient for the healthcheck FastAPI app."""
    # Import after patching
    import importlib

    import main as hc_main

    importlib.reload(hc_main)
    return TestClient(hc_main.app, raise_server_exceptions=False)


def _hc_create_todo(client: TestClient, title: str = "Task") -> Dict[str, Any]:
    """Helper to create a todo via the healthcheck API."""
    response = client.post("/api/todos", json={"title": title})
    assert response.status_code == 201
    return response.json()


class TestHealthcheckListTodos:
    """Tests for GET /api/todos."""

    def test_list_empty(self, hc_client: TestClient) -> None:
        """Empty database returns empty list."""
        resp = hc_client.get("/api/todos")
        assert resp.status_code == 200
        assert resp.json() == []

    def test_list_after_create(self, hc_client: TestClient) -> None:
        """Created todos appear in the list."""
        _hc_create_todo(hc_client, "A")
        _hc_create_todo(hc_client, "B")
        resp = hc_client.get("/api/todos")
        assert len(resp.json()) == 2


class TestHealthcheckCreateTodo:
    """Tests for POST /api/todos."""

    def test_create_success(self, hc_client: TestClient) -> None:
        """Creating a todo returns 201."""
        resp = hc_client.post("/api/todos", json={"title": "New"})
        assert resp.status_code == 201
        data = resp.json()
        assert data["title"] == "New"
        assert data["completed"] is False

    def test_create_empty_title(self, hc_client: TestClient) -> None:
        """Empty title returns 422."""
        resp = hc_client.post("/api/todos", json={"title": ""})
        assert resp.status_code == 422


class TestHealthcheckToggleTodo:
    """Tests for PATCH /api/todos/{todo_id}."""

    def test_toggle_todo(self, hc_client: TestClient) -> None:
        """Toggling a todo flips its completed status."""
        created = _hc_create_todo(hc_client, "Toggle me")
        assert created["completed"] is False

        resp = hc_client.patch(f"/api/todos/{created['id']}")
        assert resp.status_code == 200
        assert resp.json()["completed"] is True

    def test_toggle_twice_returns_to_original(self, hc_client: TestClient) -> None:
        """Toggling twice returns to original state."""
        created = _hc_create_todo(hc_client)
        hc_client.patch(f"/api/todos/{created['id']}")
        resp = hc_client.patch(f"/api/todos/{created['id']}")
        assert resp.json()["completed"] is False

    def test_toggle_nonexistent(self, hc_client: TestClient) -> None:
        """Toggling a non-existent todo returns 404."""
        resp = hc_client.patch("/api/todos/99999")
        assert resp.status_code == 404


class TestHealthcheckDeleteTodo:
    """Tests for DELETE /api/todos/{todo_id}."""

    def test_delete_existing(self, hc_client: TestClient) -> None:
        """Deleting an existing todo returns 200."""
        created = _hc_create_todo(hc_client)
        resp = hc_client.delete(f"/api/todos/{created['id']}")
        assert resp.status_code == 200

    def test_delete_nonexistent(self, hc_client: TestClient) -> None:
        """Deleting a non-existent todo returns 404."""
        resp = hc_client.delete("/api/todos/99999")
        assert resp.status_code == 404

    def test_delete_removes_from_list(self, hc_client: TestClient) -> None:
        """After deletion the todo no longer appears in the list."""
        created = _hc_create_todo(hc_client)
        hc_client.delete(f"/api/todos/{created['id']}")
        resp = hc_client.get("/api/todos")
        ids = [t["id"] for t in resp.json()]
        assert created["id"] not in ids


class TestHealthcheckServeIndex:
    """Tests for GET / (frontend serving)."""

    def test_serve_index_when_file_exists(
        self, hc_client: TestClient, tmp_path: Path
    ) -> None:
        """When static/index.html exists, it is served."""
        static_dir = Path(_HC_DIR) / "static"
        index_path = static_dir / "index.html"
        if index_path.exists():
            resp = hc_client.get("/")
            assert resp.status_code == 200
            assert "text/html" in resp.headers.get("content-type", "")

    def test_serve_index_when_missing(self, hc_client: TestClient) -> None:
        """When static/index.html is missing, 404 is returned."""
        static_dir = Path(_HC_DIR) / "static"
        index_path = static_dir / "index.html"
        if not index_path.exists():
            resp = hc_client.get("/")
            assert resp.status_code == 404
