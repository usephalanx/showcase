"""Tests for the App component and its state management logic.

These tests verify the React component structure by parsing the source
files directly, ensuring correct component composition, state management
patterns, and handler implementations.
"""

import os
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent


def _read(path: str) -> str:
    """Read a file relative to the project root."""
    full_path = ROOT / path
    assert full_path.exists(), f"File not found: {full_path}"
    return full_path.read_text(encoding="utf-8")


class TestTodoType:
    """Tests for the Todo type definition."""

    def test_todo_type_file_exists(self) -> None:
        """Ensure src/types/todo.ts exists."""
        assert (ROOT / "src" / "types" / "todo.ts").exists()

    def test_todo_has_id_field(self) -> None:
        """Todo interface must have an id field of type string."""
        content = _read("src/types/todo.ts")
        assert re.search(r"id\s*:\s*string", content)

    def test_todo_has_text_field(self) -> None:
        """Todo interface must have a text field of type string."""
        content = _read("src/types/todo.ts")
        assert re.search(r"text\s*:\s*string", content)

    def test_todo_has_completed_field(self) -> None:
        """Todo interface must have a completed field of type boolean."""
        content = _read("src/types/todo.ts")
        assert re.search(r"completed\s*:\s*boolean", content)


class TestAppComponent:
    """Tests for the App component (src/App.tsx)."""

    def test_app_file_exists(self) -> None:
        """Ensure src/App.tsx exists."""
        assert (ROOT / "src" / "App.tsx").exists()

    def test_imports_use_state(self) -> None:
        """App must import useState from react."""
        content = _read("src/App.tsx")
        assert "useState" in content

    def test_imports_todo_type(self) -> None:
        """App must import the Todo type."""
        content = _read("src/App.tsx")
        assert "Todo" in content

    def test_imports_todo_input(self) -> None:
        """App must import TodoInput component."""
        content = _read("src/App.tsx")
        assert "TodoInput" in content

    def test_imports_todo_list(self) -> None:
        """App must import TodoList component."""
        content = _read("src/App.tsx")
        assert "TodoList" in content

    def test_uses_state_with_todo_array(self) -> None:
        """App must use useState<Todo[]>."""
        content = _read("src/App.tsx")
        assert "useState<Todo[]>" in content

    def test_initial_state_is_empty_array(self) -> None:
        """App must initialise todos with an empty array."""
        content = _read("src/App.tsx")
        assert re.search(r"useState<Todo\[\]>\(\[\]\)", content)

    def test_add_todo_uses_crypto_random_uuid(self) -> None:
        """addTodo must use crypto.randomUUID() for id generation."""
        content = _read("src/App.tsx")
        assert "crypto.randomUUID()" in content

    def test_add_todo_function_exists(self) -> None:
        """App must define an addTodo function."""
        content = _read("src/App.tsx")
        assert re.search(r"const\s+addTodo", content)

    def test_toggle_todo_function_exists(self) -> None:
        """App must define a toggleTodo function."""
        content = _read("src/App.tsx")
        assert re.search(r"const\s+toggleTodo", content)

    def test_delete_todo_function_exists(self) -> None:
        """App must define a deleteTodo function."""
        content = _read("src/App.tsx")
        assert re.search(r"const\s+deleteTodo", content)

    def test_toggle_todo_flips_completed(self) -> None:
        """toggleTodo must flip the completed property."""
        content = _read("src/App.tsx")
        assert "!todo.completed" in content

    def test_delete_todo_filters_by_id(self) -> None:
        """deleteTodo must filter todos by id."""
        content = _read("src/App.tsx")
        assert "filter" in content

    def test_renders_heading(self) -> None:
        """App must render an h1 heading."""
        content = _read("src/App.tsx")
        assert "<h1" in content
        assert "Todo App" in content

    def test_renders_todo_input_component(self) -> None:
        """App must render <TodoInput> in its JSX."""
        content = _read("src/App.tsx")
        assert "<TodoInput" in content

    def test_renders_todo_list_component(self) -> None:
        """App must render <TodoList> in its JSX."""
        content = _read("src/App.tsx")
        assert "<TodoList" in content

    def test_passes_on_add_to_todo_input(self) -> None:
        """App must pass onAdd prop to TodoInput."""
        content = _read("src/App.tsx")
        assert re.search(r"<TodoInput[^>]*onAdd", content)

    def test_passes_todos_to_todo_list(self) -> None:
        """App must pass todos prop to TodoList."""
        content = _read("src/App.tsx")
        assert re.search(r"<TodoList[^>]*todos", content)

    def test_passes_on_toggle_to_todo_list(self) -> None:
        """App must pass onToggle prop to TodoList."""
        content = _read("src/App.tsx")
        assert re.search(r"<TodoList[^>]*onToggle", content)

    def test_passes_on_delete_to_todo_list(self) -> None:
        """App must pass onDelete prop to TodoList."""
        content = _read("src/App.tsx")
        assert re.search(r"<TodoList[^>]*onDelete", content)

    def test_imports_app_css(self) -> None:
        """App must import App.css."""
        content = _read("src/App.tsx")
        assert "./App.css" in content

    def test_exports_default(self) -> None:
        """App must have a default export."""
        content = _read("src/App.tsx")
        assert "export default App" in content


class TestAppCss:
    """Tests for the App.css stylesheet."""

    def test_app_css_file_exists(self) -> None:
        """Ensure src/App.css exists."""
        assert (ROOT / "src" / "App.css").exists()

    def test_has_app_class(self) -> None:
        """App.css must define the .app class."""
        content = _read("src/App.css")
        assert ".app" in content

    def test_has_todo_list_class(self) -> None:
        """App.css must define the .todo-list class."""
        content = _read("src/App.css")
        assert ".todo-list" in content

    def test_has_todo_item_class(self) -> None:
        """App.css must define the .todo-item class."""
        content = _read("src/App.css")
        assert ".todo-item" in content

    def test_has_todo_input_class(self) -> None:
        """App.css must define the .todo-input class."""
        content = _read("src/App.css")
        assert ".todo-input" in content


class TestTodoInputComponent:
    """Tests for the TodoInput component."""

    def test_todo_input_file_exists(self) -> None:
        """Ensure TodoInput component file exists."""
        assert (ROOT / "src" / "components" / "TodoInput" / "TodoInput.tsx").exists()

    def test_uses_form_element(self) -> None:
        """TodoInput must use a <form> element for submission."""
        content = _read("src/components/TodoInput/TodoInput.tsx")
        assert "<form" in content

    def test_uses_on_submit(self) -> None:
        """TodoInput must handle onSubmit on the form."""
        content = _read("src/components/TodoInput/TodoInput.tsx")
        assert "onSubmit" in content

    def test_prevents_default(self) -> None:
        """TodoInput must call preventDefault on form submit."""
        content = _read("src/components/TodoInput/TodoInput.tsx")
        assert "preventDefault" in content

    def test_trims_input(self) -> None:
        """TodoInput must trim whitespace before submitting."""
        content = _read("src/components/TodoInput/TodoInput.tsx")
        assert ".trim()" in content

    def test_rejects_empty_input(self) -> None:
        """TodoInput must not call onAdd with empty text."""
        content = _read("src/components/TodoInput/TodoInput.tsx")
        # Should check length or emptiness
        assert re.search(r"(length\s*===\s*0|===\s*['\"]\s*['\"])", content)

    def test_clears_input_after_submit(self) -> None:
        """TodoInput must clear the input field after successful submission."""
        content = _read("src/components/TodoInput/TodoInput.tsx")
        assert 'setText("")' in content or "setText('')" in content

    def test_has_on_add_prop(self) -> None:
        """TodoInput must accept an onAdd prop."""
        content = _read("src/components/TodoInput/TodoInput.tsx")
        assert "onAdd" in content


class TestTodoListComponent:
    """Tests for the TodoList component."""

    def test_todo_list_file_exists(self) -> None:
        """Ensure TodoList component file exists."""
        assert (ROOT / "src" / "components" / "TodoList" / "TodoList.tsx").exists()

    def test_renders_todo_items(self) -> None:
        """TodoList must map todos and render TodoItem components."""
        content = _read("src/components/TodoList/TodoList.tsx")
        assert "TodoItem" in content
        assert ".map(" in content

    def test_has_empty_state(self) -> None:
        """TodoList must show a message when there are no todos."""
        content = _read("src/components/TodoList/TodoList.tsx")
        assert re.search(r"(No todos|empty|nothing)", content, re.IGNORECASE)

    def test_accepts_required_props(self) -> None:
        """TodoList must accept todos, onToggle, and onDelete props."""
        content = _read("src/components/TodoList/TodoList.tsx")
        assert "todos" in content
        assert "onToggle" in content
        assert "onDelete" in content


class TestTodoItemComponent:
    """Tests for the TodoItem component."""

    def test_todo_item_file_exists(self) -> None:
        """Ensure TodoItem component file exists."""
        assert (ROOT / "src" / "components" / "TodoItem" / "TodoItem.tsx").exists()

    def test_renders_checkbox(self) -> None:
        """TodoItem must render a checkbox input."""
        content = _read("src/components/TodoItem/TodoItem.tsx")
        assert 'type="checkbox"' in content

    def test_renders_delete_button(self) -> None:
        """TodoItem must render a delete button."""
        content = _read("src/components/TodoItem/TodoItem.tsx")
        assert "Delete" in content

    def test_applies_line_through_when_completed(self) -> None:
        """TodoItem must apply line-through text decoration when completed."""
        content = _read("src/components/TodoItem/TodoItem.tsx")
        assert "line-through" in content

    def test_calls_on_toggle(self) -> None:
        """TodoItem must call onToggle when checkbox changes."""
        content = _read("src/components/TodoItem/TodoItem.tsx")
        assert "onToggle" in content

    def test_calls_on_delete(self) -> None:
        """TodoItem must call onDelete when delete button is clicked."""
        content = _read("src/components/TodoItem/TodoItem.tsx")
        assert "onDelete" in content
