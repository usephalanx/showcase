"""Tests for the TodoItem React component.

Validates rendering, checkbox toggling, delete button clicks,
and line-through styling when a todo is completed.

These tests parse the TSX source to verify component structure
and behaviour contracts without requiring a full JS runtime.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

COMPONENT_PATH = Path("src/components/TodoItem/TodoItem.tsx")
TYPES_PATH = Path("src/types/todo.ts")
CSS_PATH = Path("src/components/TodoItem/TodoItem.module.css")


@pytest.fixture()
def component_source() -> str:
    """Read and return the TodoItem component source code."""
    assert COMPONENT_PATH.exists(), f"{COMPONENT_PATH} does not exist"
    return COMPONENT_PATH.read_text(encoding="utf-8")


@pytest.fixture()
def types_source() -> str:
    """Read and return the Todo type definition source code."""
    assert TYPES_PATH.exists(), f"{TYPES_PATH} does not exist"
    return TYPES_PATH.read_text(encoding="utf-8")


@pytest.fixture()
def css_source() -> str:
    """Read and return the TodoItem CSS module source code."""
    assert CSS_PATH.exists(), f"{CSS_PATH} does not exist"
    return CSS_PATH.read_text(encoding="utf-8")


class TestTodoTypeDefinition:
    """Verify the Todo interface is correctly defined."""

    def test_todo_interface_exists(self, types_source: str) -> None:
        """The Todo interface must be exported."""
        assert "export interface Todo" in types_source

    def test_todo_has_id_field(self, types_source: str) -> None:
        """The Todo interface must have an id field of type string."""
        assert re.search(r"id\s*:\s*string", types_source)

    def test_todo_has_text_field(self, types_source: str) -> None:
        """The Todo interface must have a text field of type string."""
        assert re.search(r"text\s*:\s*string", types_source)

    def test_todo_has_completed_field(self, types_source: str) -> None:
        """The Todo interface must have a completed field of type boolean."""
        assert re.search(r"completed\s*:\s*boolean", types_source)


class TestTodoItemComponent:
    """Verify the TodoItem component structure and behaviour."""

    def test_file_exists(self) -> None:
        """TodoItem.tsx must exist at the expected path."""
        assert COMPONENT_PATH.exists()

    def test_imports_todo_type(self, component_source: str) -> None:
        """Component must import the Todo type."""
        assert "Todo" in component_source
        assert "import" in component_source

    def test_renders_checkbox(self, component_source: str) -> None:
        """Component must render an input with type checkbox."""
        assert 'type="checkbox"' in component_source

    def test_checkbox_reflects_completed_state(self, component_source: str) -> None:
        """Checkbox checked prop must be bound to todo.completed."""
        assert re.search(r"checked=\{todo\.completed\}", component_source)

    def test_calls_on_toggle_when_checkbox_clicked(self, component_source: str) -> None:
        """Checkbox onChange must call onToggle with todo.id."""
        assert re.search(r"onChange=\{.*onToggle\(todo\.id\).*\}", component_source)

    def test_renders_todo_text(self, component_source: str) -> None:
        """Component must render todo.text content."""
        assert "{todo.text}" in component_source

    def test_applies_line_through_when_completed(self, component_source: str) -> None:
        """Component must apply line-through textDecoration when completed."""
        assert "line-through" in component_source
        # Verify it's conditional on todo.completed
        assert re.search(
            r"todo\.completed\s*\?\s*[\"']line-through[\"']", component_source
        )

    def test_no_line_through_when_not_completed(self, component_source: str) -> None:
        """Component must use 'none' textDecoration when not completed."""
        assert re.search(
            r":\s*[\"']none[\"']", component_source
        )

    def test_renders_delete_button(self, component_source: str) -> None:
        """Component must render a delete button."""
        assert "Delete" in component_source
        assert "<button" in component_source

    def test_calls_on_delete_when_button_clicked(self, component_source: str) -> None:
        """Delete button onClick must call onDelete with todo.id."""
        assert re.search(r"onClick=\{.*onDelete\(todo\.id\).*\}", component_source)

    def test_props_interface_has_todo(self, component_source: str) -> None:
        """Props interface must include a todo prop of type Todo."""
        assert re.search(r"todo\s*:\s*Todo", component_source)

    def test_props_interface_has_on_toggle(self, component_source: str) -> None:
        """Props interface must include onToggle callback."""
        assert re.search(r"onToggle\s*:", component_source)

    def test_props_interface_has_on_delete(self, component_source: str) -> None:
        """Props interface must include onDelete callback."""
        assert re.search(r"onDelete\s*:", component_source)

    def test_default_export(self, component_source: str) -> None:
        """Component must have a default export."""
        assert "export default TodoItem" in component_source

    def test_renders_as_list_item(self, component_source: str) -> None:
        """Component must render as a <li> element for use in lists."""
        assert "<li" in component_source

    def test_has_accessibility_labels(self, component_source: str) -> None:
        """Component should have aria-labels for accessibility."""
        assert "aria-label" in component_source


class TestTodoItemCSS:
    """Verify the CSS module for TodoItem."""

    def test_css_file_exists(self) -> None:
        """CSS module file must exist."""
        assert CSS_PATH.exists()

    def test_has_todo_item_class(self, css_source: str) -> None:
        """CSS must define .todoItem class."""
        assert ".todoItem" in css_source

    def test_has_delete_button_class(self, css_source: str) -> None:
        """CSS must define .deleteButton class."""
        assert ".deleteButton" in css_source

    def test_has_todo_text_class(self, css_source: str) -> None:
        """CSS must define .todoText class."""
        assert ".todoText" in css_source
