"""Tests for frontend/src/api.ts.

Verifies the API service file exists, configures axios correctly, and
exports all required CRUD functions.
"""

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
API_PATH = REPO_ROOT / "frontend" / "src" / "api.ts"


def _read_api() -> str:
    """Read and return the full content of api.ts."""
    return API_PATH.read_text(encoding="utf-8")


def test_api_file_exists() -> None:
    """api.ts must exist at frontend/src/api.ts."""
    assert API_PATH.exists(), "frontend/src/api.ts not found"


def test_api_base_url() -> None:
    """api.ts must configure axios with baseURL http://localhost:8000."""
    content = _read_api()
    assert "http://localhost:8000" in content, "Missing baseURL http://localhost:8000"


def test_api_imports_axios() -> None:
    """api.ts must import axios."""
    content = _read_api()
    assert "import axios" in content or "from 'axios'" in content


def test_api_imports_types() -> None:
    """api.ts must import types from ./types."""
    content = _read_api()
    assert "from './types'" in content or 'from "./types"' in content


def test_api_exports_get_tasks() -> None:
    """api.ts must export a getTasks function."""
    content = _read_api()
    assert "export async function getTasks" in content


def test_api_exports_get_task() -> None:
    """api.ts must export a getTask function."""
    content = _read_api()
    assert "export async function getTask" in content


def test_api_exports_create_task() -> None:
    """api.ts must export a createTask function."""
    content = _read_api()
    assert "export async function createTask" in content


def test_api_exports_update_task() -> None:
    """api.ts must export an updateTask function."""
    content = _read_api()
    assert "export async function updateTask" in content


def test_api_exports_delete_task() -> None:
    """api.ts must export a deleteTask function."""
    content = _read_api()
    assert "export async function deleteTask" in content


def test_api_uses_correct_http_methods() -> None:
    """api.ts must use the correct HTTP methods for each operation."""
    content = _read_api()
    assert "api.get" in content, "Missing GET requests"
    assert "api.post" in content, "Missing POST request"
    assert "api.put" in content, "Missing PUT request"
    assert "api.delete" in content, "Missing DELETE request"


def test_api_get_task_uses_id_parameter() -> None:
    """getTask must interpolate the id into the URL path."""
    content = _read_api()
    assert "/tasks/${id}" in content or "/tasks/" in content
