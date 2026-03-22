"""Tests for the static/index.html frontend page.

Validates that the HTML file exists, contains the required structural
elements, and that the embedded JavaScript calls the correct API endpoints.
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

STATIC_DIR: Path = Path(__file__).resolve().parent.parent / "static"
HTML_PATH: Path = STATIC_DIR / "index.html"


@pytest.fixture(scope="module")
def html_content() -> str:
    """Read and return the contents of static/index.html."""
    assert HTML_PATH.exists(), f"{HTML_PATH} does not exist"
    return HTML_PATH.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# Existence & basic structure
# ---------------------------------------------------------------------------


def test_index_html_exists() -> None:
    """static/index.html must exist and be non-empty."""
    assert HTML_PATH.exists()
    assert HTML_PATH.stat().st_size > 0


def test_has_doctype(html_content: str) -> None:
    """The page should start with a DOCTYPE declaration."""
    assert html_content.strip().startswith("<!DOCTYPE html>")


def test_has_html_lang(html_content: str) -> None:
    """The <html> tag must include a lang attribute."""
    assert 'lang="en"' in html_content


def test_has_meta_charset(html_content: str) -> None:
    """The page must declare UTF-8 charset."""
    assert 'charset="UTF-8"' in html_content


def test_has_viewport_meta(html_content: str) -> None:
    """The page must include a viewport meta tag for responsiveness."""
    assert "viewport" in html_content


def test_has_title(html_content: str) -> None:
    """The page title must be 'Todo App'."""
    assert "<title>Todo App</title>" in html_content


# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------


def test_has_header(html_content: str) -> None:
    """The page must contain an h1 header with 'Todo App'."""
    assert "<h1>" in html_content
    assert "Todo App" in html_content


# ---------------------------------------------------------------------------
# Input & Add button
# ---------------------------------------------------------------------------


def test_has_input_field(html_content: str) -> None:
    """The page must contain an input element for entering todos."""
    assert 'id="todo-input"' in html_content


def test_has_add_button(html_content: str) -> None:
    """The page must contain an Add button."""
    assert 'id="add-btn"' in html_content
    assert ">Add</" in html_content


# ---------------------------------------------------------------------------
# Todo list container
# ---------------------------------------------------------------------------


def test_has_todo_list(html_content: str) -> None:
    """The page must contain a list element for displaying todos."""
    assert 'id="todo-list"' in html_content


# ---------------------------------------------------------------------------
# Embedded CSS
# ---------------------------------------------------------------------------


def test_has_embedded_css(html_content: str) -> None:
    """The page must contain a <style> block with CSS."""
    assert "<style>" in html_content
    assert "</style>" in html_content


def test_css_has_todo_item_class(html_content: str) -> None:
    """CSS must define styles for .todo-item."""
    assert ".todo-item" in html_content


def test_css_has_completed_strikethrough(html_content: str) -> None:
    """CSS must define line-through for completed items."""
    assert "line-through" in html_content


def test_css_has_delete_btn(html_content: str) -> None:
    """CSS must define styles for .delete-btn."""
    assert ".delete-btn" in html_content


# ---------------------------------------------------------------------------
# Embedded JavaScript
# ---------------------------------------------------------------------------


def test_has_embedded_script(html_content: str) -> None:
    """The page must contain a <script> block."""
    assert "<script>" in html_content
    assert "</script>" in html_content


def test_js_fetches_todos_on_load(html_content: str) -> None:
    """JavaScript must call GET /api/todos on page load."""
    assert "fetch(" in html_content
    assert "/api/todos" in html_content


def test_js_posts_new_todo(html_content: str) -> None:
    """JavaScript must POST to /api/todos when adding."""
    assert '"POST"' in html_content


def test_js_patches_todo(html_content: str) -> None:
    """JavaScript must use PATCH to update a todo."""
    assert '"PATCH"' in html_content


def test_js_deletes_todo(html_content: str) -> None:
    """JavaScript must use DELETE to remove a todo."""
    assert '"DELETE"' in html_content


def test_js_sends_json_content_type(html_content: str) -> None:
    """POST and PATCH requests must send Content-Type: application/json."""
    assert '"Content-Type": "application/json"' in html_content


def test_js_uses_json_stringify(html_content: str) -> None:
    """The script must serialize payloads with JSON.stringify."""
    assert "JSON.stringify" in html_content


def test_js_checkbox_handling(html_content: str) -> None:
    """The script must create checkbox inputs for toggling completion."""
    assert '"checkbox"' in html_content


def test_js_dynamic_url_construction(html_content: str) -> None:
    """The script must build per-todo URLs like /api/todos/{id}."""
    # The JS concatenates the base with the id
    assert 'API_BASE + "/"' in html_content or "API_BASE + \"/\"" in html_content


# ---------------------------------------------------------------------------
# Integration test with FastAPI TestClient
# ---------------------------------------------------------------------------


def test_serve_frontend_returns_html() -> None:
    """GET / must return the HTML page with status 200."""
    # Import here to avoid import errors if FastAPI/httpx not installed
    from fastapi.testclient import TestClient

    from main import app

    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Todo App" in response.text


def test_serve_frontend_contains_key_elements() -> None:
    """The served HTML must contain the input, button, and list elements."""
    from fastapi.testclient import TestClient

    from main import app

    client = TestClient(app)
    response = client.get("/")
    body = response.text
    assert 'id="todo-input"' in body
    assert 'id="add-btn"' in body
    assert 'id="todo-list"' in body


def test_full_crud_workflow() -> None:
    """Exercise the full API workflow that the frontend JS would perform."""
    from fastapi.testclient import TestClient

    from main import app

    client = TestClient(app)

    # 1. List todos (should be empty or contain pre-existing data)
    resp = client.get("/api/todos")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)

    # 2. Create a todo
    resp = client.post("/api/todos", json={"title": "Frontend test todo"})
    assert resp.status_code == 201
    todo = resp.json()
    assert todo["title"] == "Frontend test todo"
    assert todo["completed"] is False
    todo_id = todo["id"]

    # 3. Toggle completed via PATCH
    resp = client.patch(f"/api/todos/{todo_id}", json={"completed": True})
    assert resp.status_code == 200
    assert resp.json()["completed"] is True

    # 4. Toggle back
    resp = client.patch(f"/api/todos/{todo_id}", json={"completed": False})
    assert resp.status_code == 200
    assert resp.json()["completed"] is False

    # 5. Delete
    resp = client.delete(f"/api/todos/{todo_id}")
    assert resp.status_code == 200

    # 6. Confirm deletion – should 404
    resp = client.delete(f"/api/todos/{todo_id}")
    assert resp.status_code == 404
