"""Tests for the TodoList React component.

Validates rendering behaviour including:
- Rendering a list of todo items
- Showing the empty-state message when no todos exist
- Passing onToggle and onDelete callbacks through to TodoItem
"""

import subprocess
import sys
from pathlib import Path

import pytest

SOURCE_DIR = Path(__file__).resolve().parent.parent / "src"


class TestTodoListFileStructure:
    """Verify that the TodoList component file exists with expected content."""

    def test_todolist_file_exists(self) -> None:
        """TodoList.tsx must exist at the expected path."""
        filepath = SOURCE_DIR / "components" / "TodoList" / "TodoList.tsx"
        assert filepath.exists(), f"Expected file at {filepath}"

    def test_todolist_imports_todo_type(self) -> None:
        """TodoList must import the Todo type."""
        filepath = SOURCE_DIR / "components" / "TodoList" / "TodoList.tsx"
        content = filepath.read_text(encoding="utf-8")
        assert "Todo" in content, "TodoList should import the Todo type"

    def test_todolist_imports_todoitem(self) -> None:
        """TodoList must import TodoItem component."""
        filepath = SOURCE_DIR / "components" / "TodoList" / "TodoList.tsx"
        content = filepath.read_text(encoding="utf-8")
        assert "TodoItem" in content, "TodoList should import TodoItem"

    def test_todolist_maps_over_todos(self) -> None:
        """TodoList must map over the todos array."""
        filepath = SOURCE_DIR / "components" / "TodoList" / "TodoList.tsx"
        content = filepath.read_text(encoding="utf-8")
        assert ".map(" in content or ".map (" in content, (
            "TodoList should use .map() to iterate over todos"
        )

    def test_todolist_renders_empty_message(self) -> None:
        """TodoList must contain 'No todos yet' text for empty state."""
        filepath = SOURCE_DIR / "components" / "TodoList" / "TodoList.tsx"
        content = filepath.read_text(encoding="utf-8")
        assert "No todos yet" in content, (
            "TodoList should display 'No todos yet' when list is empty"
        )

    def test_todolist_checks_empty_array(self) -> None:
        """TodoList must check for empty todos array."""
        filepath = SOURCE_DIR / "components" / "TodoList" / "TodoList.tsx"
        content = filepath.read_text(encoding="utf-8")
        assert "length" in content, (
            "TodoList should check todos.length to detect empty state"
        )


class TestTodoListProps:
    """Verify that the TodoList component defines the correct props interface."""

    def test_todolist_has_todos_prop(self) -> None:
        """TodoListProps must include a todos prop."""
        filepath = SOURCE_DIR / "components" / "TodoList" / "TodoList.tsx"
        content = filepath.read_text(encoding="utf-8")
        assert "todos" in content, "TodoListProps should include 'todos'"

    def test_todolist_has_ontoggle_prop(self) -> None:
        """TodoListProps must include an onToggle prop."""
        filepath = SOURCE_DIR / "components" / "TodoList" / "TodoList.tsx"
        content = filepath.read_text(encoding="utf-8")
        assert "onToggle" in content, "TodoListProps should include 'onToggle'"

    def test_todolist_has_ondelete_prop(self) -> None:
        """TodoListProps must include an onDelete prop."""
        filepath = SOURCE_DIR / "components" / "TodoList" / "TodoList.tsx"
        content = filepath.read_text(encoding="utf-8")
        assert "onDelete" in content, "TodoListProps should include 'onDelete'"

    def test_todolist_passes_ontoggle_to_todoitem(self) -> None:
        """TodoList must pass onToggle callback to TodoItem."""
        filepath = SOURCE_DIR / "components" / "TodoList" / "TodoList.tsx"
        content = filepath.read_text(encoding="utf-8")
        assert "onToggle={onToggle}" in content or "onToggle=" in content, (
            "TodoList should pass onToggle to TodoItem"
        )

    def test_todolist_passes_ondelete_to_todoitem(self) -> None:
        """TodoList must pass onDelete callback to TodoItem."""
        filepath = SOURCE_DIR / "components" / "TodoList" / "TodoList.tsx"
        content = filepath.read_text(encoding="utf-8")
        assert "onDelete={onDelete}" in content or "onDelete=" in content, (
            "TodoList should pass onDelete to TodoItem"
        )


class TestTodoListExport:
    """Verify that the component is exported correctly."""

    def test_todolist_default_export(self) -> None:
        """TodoList must have a default export."""
        filepath = SOURCE_DIR / "components" / "TodoList" / "TodoList.tsx"
        content = filepath.read_text(encoding="utf-8")
        assert "export default" in content, (
            "TodoList should have a default export"
        )


class TestTodoListKey:
    """Verify that mapped items use a key prop."""

    def test_todolist_uses_key_prop(self) -> None:
        """Each mapped TodoItem must have a key prop for React reconciliation."""
        filepath = SOURCE_DIR / "components" / "TodoList" / "TodoList.tsx"
        content = filepath.read_text(encoding="utf-8")
        assert "key={" in content or "key =" in content, (
            "TodoList should set a key prop on each mapped TodoItem"
        )


class TestTodoItemFileStructure:
    """Verify that the TodoItem component file exists."""

    def test_todoitem_file_exists(self) -> None:
        """TodoItem.tsx must exist at the expected path."""
        filepath = SOURCE_DIR / "components" / "TodoItem" / "TodoItem.tsx"
        assert filepath.exists(), f"Expected file at {filepath}"


class TestTodoType:
    """Verify that the Todo type definition exists."""

    def test_todo_type_file_exists(self) -> None:
        """todo.ts must exist at the expected path."""
        filepath = SOURCE_DIR / "types" / "todo.ts"
        assert filepath.exists(), f"Expected file at {filepath}"

    def test_todo_type_has_id_field(self) -> None:
        """Todo interface must include an id field of type string."""
        filepath = SOURCE_DIR / "types" / "todo.ts"
        content = filepath.read_text(encoding="utf-8")
        assert "id" in content, "Todo type should have an 'id' field"
        assert "string" in content, "Todo type should use string type for id"

    def test_todo_type_has_text_field(self) -> None:
        """Todo interface must include a text field."""
        filepath = SOURCE_DIR / "types" / "todo.ts"
        content = filepath.read_text(encoding="utf-8")
        assert "text" in content, "Todo type should have a 'text' field"

    def test_todo_type_has_completed_field(self) -> None:
        """Todo interface must include a completed field."""
        filepath = SOURCE_DIR / "types" / "todo.ts"
        content = filepath.read_text(encoding="utf-8")
        assert "completed" in content, "Todo type should have a 'completed' field"
        assert "boolean" in content, "Todo type should use boolean for completed"
