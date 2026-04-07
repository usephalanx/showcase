"""Tests that validate the todoHelpers TypeScript utility file.

These tests read the source file and assert that the required
function signatures and logic patterns are present.
"""

from __future__ import annotations

from pathlib import Path

import pytest

ROOT_DIR: Path = Path(__file__).resolve().parent.parent
HELPERS_PATH: Path = ROOT_DIR / "src" / "utils" / "todoHelpers.ts"


@pytest.fixture()
def helpers_content() -> str:
    """Read and return the contents of src/utils/todoHelpers.ts."""
    assert HELPERS_PATH.exists(), f"{HELPERS_PATH} does not exist"
    return HELPERS_PATH.read_text(encoding="utf-8")


class TestTodoHelpersFile:
    """Verify the todoHelpers module exists and is well-structured."""

    def test_file_exists(self) -> None:
        """src/utils/todoHelpers.ts must exist."""
        assert HELPERS_PATH.exists()

    def test_imports_todo_type(self, helpers_content: str) -> None:
        """The file must import from the types module."""
        assert "from '../types/todo'" in helpers_content or 'from "../types/todo"' in helpers_content


class TestGenerateId:
    """Verify the generateId function."""

    def test_export_exists(self, helpers_content: str) -> None:
        """generateId must be an exported function."""
        assert "export function generateId" in helpers_content

    def test_returns_string(self, helpers_content: str) -> None:
        """generateId must have a string return type."""
        # Look for the return type annotation
        assert "generateId(): string" in helpers_content

    def test_uses_crypto_random_uuid(self, helpers_content: str) -> None:
        """generateId should use crypto.randomUUID when available."""
        assert "crypto.randomUUID" in helpers_content


class TestCreateTodo:
    """Verify the createTodo function."""

    def test_export_exists(self, helpers_content: str) -> None:
        """createTodo must be an exported function."""
        assert "export function createTodo" in helpers_content

    def test_accepts_text_param(self, helpers_content: str) -> None:
        """createTodo must accept a text parameter of type string."""
        assert "createTodo(text: string)" in helpers_content

    def test_returns_todo(self, helpers_content: str) -> None:
        """createTodo must return a Todo."""
        assert "createTodo(text: string): Todo" in helpers_content

    def test_trims_text(self, helpers_content: str) -> None:
        """createTodo must trim the input text."""
        assert ".trim()" in helpers_content

    def test_rejects_empty_text(self, helpers_content: str) -> None:
        """createTodo must throw on empty/whitespace-only text."""
        assert "throw" in helpers_content.lower() or "Error" in helpers_content

    def test_sets_completed_false(self, helpers_content: str) -> None:
        """New todos must default to completed: false."""
        assert "completed: false" in helpers_content


class TestToggleTodo:
    """Verify the toggleTodo function."""

    def test_export_exists(self, helpers_content: str) -> None:
        """toggleTodo must be an exported function."""
        assert "export function toggleTodo" in helpers_content

    def test_accepts_todo_param(self, helpers_content: str) -> None:
        """toggleTodo must accept a Todo parameter."""
        assert "toggleTodo(todo: Todo)" in helpers_content

    def test_returns_todo(self, helpers_content: str) -> None:
        """toggleTodo must return a Todo."""
        assert "toggleTodo(todo: Todo): Todo" in helpers_content

    def test_flips_completed(self, helpers_content: str) -> None:
        """toggleTodo must negate the completed field."""
        assert "!todo.completed" in helpers_content

    def test_uses_spread(self, helpers_content: str) -> None:
        """toggleTodo must use spread to avoid mutation."""
        assert "...todo" in helpers_content


class TestFilterTodos:
    """Verify the filterTodos function."""

    def test_export_exists(self, helpers_content: str) -> None:
        """filterTodos must be an exported function."""
        assert "export function filterTodos" in helpers_content

    def test_accepts_todos_array(self, helpers_content: str) -> None:
        """filterTodos must accept a Todo[] parameter."""
        assert "todos: Todo[]" in helpers_content or "todos:Todo[]" in helpers_content

    def test_accepts_filter_param(self, helpers_content: str) -> None:
        """filterTodos must accept a FilterType parameter."""
        assert "filter: FilterType" in helpers_content or "filter:FilterType" in helpers_content

    def test_returns_todo_array(self, helpers_content: str) -> None:
        """filterTodos must return Todo[]."""
        assert "Todo[]" in helpers_content

    def test_handles_active_filter(self, helpers_content: str) -> None:
        """filterTodos must handle the 'active' case."""
        assert "'active'" in helpers_content

    def test_handles_completed_filter(self, helpers_content: str) -> None:
        """filterTodos must handle the 'completed' case."""
        assert "'completed'" in helpers_content

    def test_handles_all_filter(self, helpers_content: str) -> None:
        """filterTodos must handle the 'all' case."""
        assert "'all'" in helpers_content

    def test_todos_default_empty_array(self, helpers_content: str) -> None:
        """todos parameter must default to an empty array."""
        assert "todos: Todo[] = []" in helpers_content

    def test_filter_default_all(self, helpers_content: str) -> None:
        """filter parameter must default to 'all'."""
        assert "filter: FilterType = 'all'" in helpers_content
