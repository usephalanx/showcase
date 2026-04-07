"""Tests to verify the PLANNING.md document exists and is complete."""

from __future__ import annotations

from pathlib import Path

PLANNING_PATH = Path("PLANNING.md")


def _read_planning() -> str:
    """Read and return the content of PLANNING.md.

    Returns:
        The full text content of the planning document.
    """
    return PLANNING_PATH.read_text(encoding="utf-8")


def test_planning_md_exists() -> None:
    """PLANNING.md must exist at the repository root."""
    assert PLANNING_PATH.exists(), "PLANNING.md not found at repository root"


def test_planning_md_contains_all_sections() -> None:
    """PLANNING.md must contain all required section headings."""
    content = _read_planning()
    required_sections = [
        "Overview",
        "Project Structure",
        "Data Model",
        "Pydantic Schemas",
        "API Endpoints",
        "Storage",
        "Error Handling",
    ]
    for section in required_sections:
        assert section in content, f"Missing section: {section}"


def test_planning_md_contains_all_endpoints() -> None:
    """PLANNING.md must document all five CRUD endpoints."""
    content = _read_planning()
    expected_endpoints = [
        "GET",
        "POST",
        "PUT",
        "DELETE",
        "/todos",
        "/todos/{id}",
    ]
    for endpoint in expected_endpoints:
        assert endpoint in content, f"Missing endpoint reference: {endpoint}"


def test_planning_md_contains_pydantic_schemas() -> None:
    """PLANNING.md must reference all three Pydantic schemas."""
    content = _read_planning()
    for schema in ["TodoCreate", "TodoUpdate", "TodoResponse"]:
        assert schema in content, f"Missing schema reference: {schema}"


def test_planning_md_contains_data_model_fields() -> None:
    """PLANNING.md must document all four data model fields."""
    content = _read_planning()
    for field in ["id", "title", "description", "completed"]:
        assert field in content, f"Missing data model field: {field}"
