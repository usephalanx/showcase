"""Structural tests for PLANNING.md.

Validates that the architecture document exists, contains all required
sections, and documents every endpoint / model field / status value.
"""

import os
import pathlib

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent
PLANNING_PATH = ROOT / "PLANNING.md"


@pytest.fixture(scope="module")
def planning_content() -> str:
    """Read PLANNING.md content once for the whole module."""
    assert PLANNING_PATH.exists(), f"PLANNING.md not found at {PLANNING_PATH}"
    return PLANNING_PATH.read_text(encoding="utf-8")


def test_planning_file_exists() -> None:
    """PLANNING.md must exist at the repository root."""
    assert PLANNING_PATH.exists()


@pytest.mark.parametrize(
    "heading",
    [
        "Overview",
        "Folder Structure",
        "Data Models",
        "Pydantic Schemas",
        "API Contract",
        "Error Responses",
        "Component Hierarchy",
        "Frontend Services",
        "Configuration",
        "Development Workflow",
    ],
)
def test_planning_has_all_sections(planning_content: str, heading: str) -> None:
    """Every required section heading must appear in PLANNING.md."""
    assert heading in planning_content, f"Missing section: {heading}"


@pytest.mark.parametrize(
    "endpoint",
    [
        "GET /api/tasks",
        "GET /api/tasks/{task_id}",
        "POST /api/tasks",
        "PUT /api/tasks/{task_id}",
        "PATCH /api/tasks/{task_id}",
        "DELETE /api/tasks/{task_id}",
    ],
)
def test_api_endpoints_defined(planning_content: str, endpoint: str) -> None:
    """All 6 REST endpoints must be documented."""
    assert endpoint in planning_content, f"Missing endpoint: {endpoint}"


@pytest.mark.parametrize(
    "field",
    ["id", "title", "status", "due_date", "created_at", "updated_at"],
)
def test_data_model_fields(planning_content: str, field: str) -> None:
    """The Task data model must document all expected columns."""
    assert field in planning_content, f"Missing model field: {field}"


@pytest.mark.parametrize("value", ["todo", "in-progress", "done"])
def test_status_enum_values(planning_content: str, value: str) -> None:
    """All valid status enum values must be listed."""
    assert value in planning_content, f"Missing status value: {value}"


def test_schemas_defined(planning_content: str) -> None:
    """Pydantic schemas TaskCreate, TaskUpdate, and TaskResponse must be defined."""
    for schema in ["TaskCreate", "TaskUpdate", "TaskResponse"]:
        assert schema in planning_content, f"Missing schema: {schema}"


def test_component_hierarchy(planning_content: str) -> None:
    """Key React components must be listed."""
    for component in ["App", "TaskList", "TaskItem", "TaskForm", "TaskFilter"]:
        assert component in planning_content, f"Missing component: {component}"


def test_folder_structure_paths(planning_content: str) -> None:
    """Key file paths must appear in the folder structure."""
    paths = [
        "backend/main.py",
        "backend/models.py",
        "backend/schemas.py",
        "backend/crud.py",
        "backend/database.py",
        "backend/routers/tasks.py",
        "frontend/src/App.tsx",
        "frontend/src/components/",
        "frontend/src/services/",
        "frontend/src/types/",
    ]
    for p in paths:
        assert p in planning_content, f"Missing path in folder structure: {p}"
