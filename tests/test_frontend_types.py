"""Tests for frontend/src/types.ts.

Verifies the TypeScript types file exists and contains the expected
interface and type definitions.
"""

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
TYPES_PATH = REPO_ROOT / "frontend" / "src" / "types.ts"


def _read_types() -> str:
    """Read and return the full content of types.ts."""
    return TYPES_PATH.read_text(encoding="utf-8")


def test_types_file_exists() -> None:
    """types.ts must exist at frontend/src/types.ts."""
    assert TYPES_PATH.exists(), "frontend/src/types.ts not found"


def test_types_has_task_status() -> None:
    """types.ts must define the TaskStatus type with three values."""
    content = _read_types()
    assert "TaskStatus" in content
    for value in ["'todo'", "'in-progress'", "'done'"]:
        assert value in content, f"Missing status value {value} in TaskStatus"


def test_types_has_task_interface() -> None:
    """types.ts must export a Task interface with all required fields."""
    content = _read_types()
    assert "export interface Task" in content
    required_fields = ["id", "title", "status", "due_date", "created_at", "updated_at"]
    for field in required_fields:
        assert field in content, f"Missing field '{field}' in Task interface"


def test_types_has_task_create() -> None:
    """types.ts must export a TaskCreate interface."""
    content = _read_types()
    assert "export interface TaskCreate" in content
    assert "title" in content


def test_types_has_task_update() -> None:
    """types.ts must export a TaskUpdate interface."""
    content = _read_types()
    assert "export interface TaskUpdate" in content


def test_types_due_date_nullable() -> None:
    """due_date should be typed as nullable (string | null)."""
    content = _read_types()
    assert "string | null" in content, "due_date should accept string | null"
