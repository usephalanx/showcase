"""Tests that validate the Todo TypeScript type definition file.

These tests read the source file and assert that required interface
fields and type exports are present.
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest

ROOT_DIR: Path = Path(__file__).resolve().parent.parent
TODO_TYPES_PATH: Path = ROOT_DIR / "src" / "types" / "todo.ts"


@pytest.fixture()
def todo_types_content() -> str:
    """Read and return the contents of src/types/todo.ts."""
    assert TODO_TYPES_PATH.exists(), f"{TODO_TYPES_PATH} does not exist"
    return TODO_TYPES_PATH.read_text(encoding="utf-8")


class TestTodoInterface:
    """Verify the Todo interface is correctly defined."""

    def test_file_exists(self) -> None:
        """src/types/todo.ts must exist."""
        assert TODO_TYPES_PATH.exists()

    def test_exports_todo_interface(self, todo_types_content: str) -> None:
        """The file must export a Todo interface."""
        assert "export interface Todo" in todo_types_content

    def test_id_field_is_string(self, todo_types_content: str) -> None:
        """Todo.id must be typed as string."""
        assert "id: string" in todo_types_content or "id:string" in todo_types_content

    def test_text_field_is_string(self, todo_types_content: str) -> None:
        """Todo.text must be typed as string."""
        assert "text: string" in todo_types_content or "text:string" in todo_types_content

    def test_completed_field_is_boolean(self, todo_types_content: str) -> None:
        """Todo.completed must be typed as boolean."""
        assert "completed: boolean" in todo_types_content or "completed:boolean" in todo_types_content

    def test_created_at_field_is_number(self, todo_types_content: str) -> None:
        """Todo.createdAt must be typed as number."""
        assert "createdAt: number" in todo_types_content or "createdAt:number" in todo_types_content

    def test_exports_filter_type(self, todo_types_content: str) -> None:
        """The file must export a FilterType union type."""
        assert "export type FilterType" in todo_types_content

    def test_filter_type_includes_all(self, todo_types_content: str) -> None:
        """FilterType must include 'all'."""
        assert "'all'" in todo_types_content

    def test_filter_type_includes_active(self, todo_types_content: str) -> None:
        """FilterType must include 'active'."""
        assert "'active'" in todo_types_content

    def test_filter_type_includes_completed(self, todo_types_content: str) -> None:
        """FilterType must include 'completed'."""
        assert "'completed'" in todo_types_content
