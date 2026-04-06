"""Structural validation tests for PLANNING.md."""

from __future__ import annotations

from pathlib import Path

import pytest

PLANNING_PATH = Path(__file__).resolve().parents[2] / "PLANNING.md"


@pytest.fixture()
def planning_content() -> str:
    """Read and return the contents of PLANNING.md."""
    assert PLANNING_PATH.exists(), f"PLANNING.md not found at {PLANNING_PATH}"
    return PLANNING_PATH.read_text(encoding="utf-8")


class TestPlanningFileExists:
    """Verify PLANNING.md exists at the repository root."""

    def test_planning_file_exists(self) -> None:
        """PLANNING.md must be present."""
        assert PLANNING_PATH.exists()


class TestPlanningHasAllSections:
    """Verify that required section headings are present."""

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
    def test_section_exists(self, planning_content: str, heading: str) -> None:
        """Each expected heading should appear in the document."""
        assert heading in planning_content, f"Missing section: {heading}"


class TestApiEndpointsDefined:
    """Verify all 6 endpoints are documented."""

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
    def test_endpoint_documented(self, planning_content: str, endpoint: str) -> None:
        """Each REST endpoint should be mentioned."""
        assert endpoint in planning_content, f"Missing endpoint: {endpoint}"


class TestDataModelFields:
    """Verify all Task model fields are documented."""

    @pytest.mark.parametrize(
        "field",
        ["id", "title", "status", "due_date", "created_at", "updated_at"],
    )
    def test_field_documented(self, planning_content: str, field: str) -> None:
        """Each field of the Task model should appear in the plan."""
        assert field in planning_content, f"Missing field: {field}"


class TestStatusEnumValues:
    """Verify all three status values are listed."""

    @pytest.mark.parametrize("value", ["todo", "in-progress", "done"])
    def test_status_value_listed(self, planning_content: str, value: str) -> None:
        """Each status enum value should appear in the plan."""
        assert value in planning_content, f"Missing status value: {value}"
