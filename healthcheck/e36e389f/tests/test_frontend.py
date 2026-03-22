"""Tests for the frontend HTML page served at GET /.

Verifies that the HTML template is served correctly, contains all
required UI elements, JavaScript fetch calls, and CSS styling.
"""

from __future__ import annotations

import os
import tempfile
from pathlib import Path
from typing import Generator

import pytest
from fastapi.testclient import TestClient

import database
from main import app


@pytest.fixture(autouse=True)
def _use_temp_db(tmp_path: Path) -> Generator[None, None, None]:
    """Switch to a temporary database for every test."""
    db_path = str(tmp_path / "test_todos.db")
    original = database.DATABASE_PATH
    database.DATABASE_PATH = db_path
    database.init_db()
    yield
    database.DATABASE_PATH = original


@pytest.fixture()
def client() -> TestClient:
    """Return a FastAPI test client."""
    return TestClient(app, raise_server_exceptions=False)


# ------------------------------------------------------------------
# Test: GET / serves the HTML page
# ------------------------------------------------------------------


def test_serve_index_returns_html(client: TestClient) -> None:
    """GET / should return a 200 with text/html content type."""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_serve_index_contains_doctype(client: TestClient) -> None:
    """The response must start with an HTML5 doctype."""
    response = client.get("/")
    assert response.text.strip().startswith("<!DOCTYPE html>")


# ------------------------------------------------------------------
# Test: Required UI elements are present
# ------------------------------------------------------------------


def test_html_has_input_field(client: TestClient) -> None:
    """The page must contain a text input for entering todo titles."""
    html = client.get("/").text
    assert 'id="todo-input"' in html
    assert 'type="text"' in html


def test_html_has_add_button(client: TestClient) -> None:
    """The page must contain an 'Add' button."""
    html = client.get("/").text
    assert 'id="add-btn"' in html
    assert ">Add</button>" in html


def test_html_has_todo_list_container(client: TestClient) -> None:
    """The page must contain a <ul> for the todo list."""
    html = client.get("/").text
    assert 'id="todo-list"' in html


def test_html_has_heading(client: TestClient) -> None:
    """The page must have a heading with 'Todo App'."""
    html = client.get("/").text
    assert "<h1>Todo App</h1>" in html


def test_html_has_error_message_element(client: TestClient) -> None:
    """The page must have an element for displaying error messages."""
    html = client.get("/").text
    assert 'id="error-message"' in html


# ------------------------------------------------------------------
# Test: JavaScript fetch calls to API endpoints
# ------------------------------------------------------------------


def test_js_calls_get_api_todos(client: TestClient) -> None:
    """JavaScript must call fetch(API) for loading todos."""
    html = client.get("/").text
    assert "fetch(API)" in html or "fetch('/api/todos')" in html


def test_js_calls_post_api_todos(client: TestClient) -> None:
    """JavaScript must call POST to create new todos."""
    html = client.get("/").text
    assert "method: 'POST'" in html
    assert "'Content-Type': 'application/json'" in html


def test_js_calls_patch_api_todos(client: TestClient) -> None:
    """JavaScript must call PATCH to toggle a todo."""
    html = client.get("/").text
    assert "method: 'PATCH'" in html


def test_js_calls_delete_api_todos(client: TestClient) -> None:
    """JavaScript must call DELETE to remove a todo."""
    html = client.get("/").text
    assert "method: 'DELETE'" in html


def test_js_defines_api_base_url(client: TestClient) -> None:
    """JavaScript must define the API base URL constant."""
    html = client.get("/").text
    assert "var API = '/api/todos'" in html or "const API = '/api/todos'" in html


# ------------------------------------------------------------------
# Test: CSS styling
# ------------------------------------------------------------------


def test_css_has_centered_layout(client: TestClient) -> None:
    """The CSS must center the body content with max-width and auto margin."""
    html = client.get("/").text
    assert "max-width: 600px" in html or "max-width:600px" in html
    assert "margin:" in html


def test_css_has_strikethrough_for_completed(client: TestClient) -> None:
    """The CSS must apply a strikethrough to completed todo items."""
    html = client.get("/").text
    assert "text-decoration: line-through" in html or "text-decoration:line-through" in html


def test_css_has_input_group_styling(client: TestClient) -> None:
    """The CSS must style the input group with flex layout."""
    html = client.get("/").text
    assert ".input-group" in html
    assert "display: flex" in html or "display:flex" in html


def test_css_has_list_item_styling(client: TestClient) -> None:
    """The CSS must style list items with background and shadow."""
    html = client.get("/").text
    assert "box-shadow" in html


def test_css_has_delete_button_color(client: TestClient) -> None:
    """The CSS must color the delete button red."""
    html = client.get("/").text
    assert "#e53935" in html


# ------------------------------------------------------------------
# Test: Accessibility attributes
# ------------------------------------------------------------------


def test_html_has_aria_labels(client: TestClient) -> None:
    """The page must include aria-label attributes for accessibility."""
    html = client.get("/").text
    assert 'aria-label="New todo title"' in html
    assert 'aria-label="Add todo"' in html
    assert 'aria-label="Todo list"' in html


def test_html_has_lang_attribute(client: TestClient) -> None:
    """The <html> element must include a lang attribute."""
    html = client.get("/").text
    assert '<html lang="en">' in html


def test_html_has_viewport_meta(client: TestClient) -> None:
    """The page must include a viewport meta tag for responsiveness."""
    html = client.get("/").text
    assert 'name="viewport"' in html


# ------------------------------------------------------------------
# Test: JavaScript behaviour features
# ------------------------------------------------------------------


def test_js_handles_enter_key(client: TestClient) -> None:
    """JavaScript must listen for the Enter key on the input field."""
    html = client.get("/").text
    assert "'Enter'" in html or '"Enter"' in html
    assert "keydown" in html


def test_js_loads_on_page_load(client: TestClient) -> None:
    """JavaScript must call loadTodos() on page load."""
    html = client.get("/").text
    assert "loadTodos()" in html


def test_js_refetches_after_add(client: TestClient) -> None:
    """JavaScript must re-fetch the todo list after adding a new one."""
    html = client.get("/").text
    # The addTodo function should call loadTodos after successful POST
    assert "loadTodos" in html


def test_js_has_escape_html_function(client: TestClient) -> None:
    """JavaScript must have an XSS-prevention escapeHtml helper."""
    html = client.get("/").text
    assert "escapeHtml" in html


def test_js_has_error_handling(client: TestClient) -> None:
    """JavaScript must handle fetch errors with try/catch."""
    html = client.get("/").text
    assert "catch" in html
    assert "showError" in html


# ------------------------------------------------------------------
# Test: Empty state display
# ------------------------------------------------------------------


def test_js_has_empty_state_message(client: TestClient) -> None:
    """JavaScript must show a message when there are no todos."""
    html = client.get("/").text
    assert "No todos yet" in html or "empty-state" in html


# ------------------------------------------------------------------
# Test: Full integration – frontend + API round trip
# ------------------------------------------------------------------


def test_integration_create_and_list(client: TestClient) -> None:
    """Create a todo via the API and verify the list endpoint returns it."""
    # Page loads
    response = client.get("/")
    assert response.status_code == 200

    # Create a todo
    response = client.post(
        "/api/todos",
        json={"title": "Integration test todo"},
    )
    assert response.status_code == 201
    todo = response.json()
    assert todo["title"] == "Integration test todo"
    assert todo["completed"] is False

    # List should include it
    response = client.get("/api/todos")
    assert response.status_code == 200
    todos = response.json()
    assert len(todos) == 1
    assert todos[0]["title"] == "Integration test todo"


def test_integration_toggle_todo(client: TestClient) -> None:
    """Toggle a todo's completion status and verify the change."""
    # Create
    response = client.post("/api/todos", json={"title": "Toggle me"})
    todo_id = response.json()["id"]

    # Toggle (should become True)
    response = client.patch(f"/api/todos/{todo_id}")
    assert response.status_code == 200
    assert response.json()["completed"] is True

    # Toggle again (should become False)
    response = client.patch(f"/api/todos/{todo_id}")
    assert response.status_code == 200
    assert response.json()["completed"] is False


def test_integration_delete_todo(client: TestClient) -> None:
    """Delete a todo and verify it no longer appears in the list."""
    # Create
    response = client.post("/api/todos", json={"title": "Delete me"})
    todo_id = response.json()["id"]

    # Delete
    response = client.delete(f"/api/todos/{todo_id}")
    assert response.status_code == 200

    # Should be gone
    response = client.get("/api/todos")
    assert response.json() == []


def test_integration_delete_nonexistent_returns_404(client: TestClient) -> None:
    """Deleting a non-existent todo should return 404."""
    response = client.delete("/api/todos/99999")
    assert response.status_code == 404


def test_integration_toggle_nonexistent_returns_404(client: TestClient) -> None:
    """Toggling a non-existent todo should return 404."""
    response = client.patch("/api/todos/99999")
    assert response.status_code == 404
