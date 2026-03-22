"""Structural tests to verify that documentation files exist and contain
expected content.
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest

DOCS_DIR = Path(__file__).resolve().parent.parent / "docs"


class TestArchitectureMd:
    """Tests for docs/architecture.md."""

    def test_architecture_md_exists(self) -> None:
        """docs/architecture.md should exist and be non-empty."""
        path = DOCS_DIR / "architecture.md"
        assert path.exists(), f"{path} does not exist"
        assert path.stat().st_size > 0, f"{path} is empty"

    def test_architecture_contains_schema(self) -> None:
        """architecture.md should describe the database schema."""
        content = (DOCS_DIR / "architecture.md").read_text(encoding="utf-8")
        assert "CREATE TABLE" in content
        assert "todos" in content

    def test_architecture_contains_technology_stack(self) -> None:
        """architecture.md should mention the technology stack."""
        content = (DOCS_DIR / "architecture.md").read_text(encoding="utf-8")
        assert "SQLite" in content
        assert "FastAPI" in content
        assert "Python" in content

    def test_architecture_contains_file_structure(self) -> None:
        """architecture.md should describe the project file structure."""
        content = (DOCS_DIR / "architecture.md").read_text(encoding="utf-8")
        assert "database.py" in content
        assert "main.py" in content

    def test_architecture_contains_component_diagram(self) -> None:
        """architecture.md should include a component diagram."""
        content = (DOCS_DIR / "architecture.md").read_text(encoding="utf-8")
        assert "Browser" in content
        assert "database.py" in content
        assert "todos.db" in content


class TestApiSpecMd:
    """Tests for docs/api-spec.md."""

    def test_api_spec_md_exists(self) -> None:
        """docs/api-spec.md should exist and be non-empty."""
        path = DOCS_DIR / "api-spec.md"
        assert path.exists(), f"{path} does not exist"
        assert path.stat().st_size > 0, f"{path} is empty"

    def test_api_spec_contains_endpoints(self) -> None:
        """api-spec.md should document all REST endpoints."""
        content = (DOCS_DIR / "api-spec.md").read_text(encoding="utf-8")
        assert "GET /" in content
        assert "GET /api/todos" in content
        assert "POST /api/todos" in content
        assert "PATCH /api/todos/{id}" in content
        assert "DELETE /api/todos/{id}" in content

    def test_api_spec_contains_models(self) -> None:
        """api-spec.md should define Pydantic models."""
        content = (DOCS_DIR / "api-spec.md").read_text(encoding="utf-8")
        assert "TodoCreate" in content
        assert "TodoUpdate" in content
        assert "TodoResponse" in content

    def test_api_spec_contains_status_codes(self) -> None:
        """api-spec.md should mention key HTTP status codes."""
        content = (DOCS_DIR / "api-spec.md").read_text(encoding="utf-8")
        assert "200" in content
        assert "201" in content
        assert "204" in content
        assert "404" in content
        assert "422" in content

    def test_api_spec_contains_error_format(self) -> None:
        """api-spec.md should describe the error response format."""
        content = (DOCS_DIR / "api-spec.md").read_text(encoding="utf-8")
        assert "detail" in content

    def test_api_spec_contains_database_functions(self) -> None:
        """api-spec.md should document database.py functions."""
        content = (DOCS_DIR / "api-spec.md").read_text(encoding="utf-8")
        assert "init_db" in content
        assert "get_all_todos" in content
        assert "create_todo" in content
        assert "update_todo_completed" in content
        assert "delete_todo" in content
