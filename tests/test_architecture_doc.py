"""Tests for ARCHITECTURE.md documentation structure.

Verifies that the architecture document exists, contains all required
sections, documents all API endpoints, and references all frontend
components.
"""

from __future__ import annotations

from pathlib import Path

import pytest

ARCHITECTURE_PATH = Path(__file__).resolve().parent.parent / "ARCHITECTURE.md"


@pytest.fixture()
def architecture_content() -> str:
    """Read and return the ARCHITECTURE.md file content."""
    assert ARCHITECTURE_PATH.exists(), f"{ARCHITECTURE_PATH} does not exist"
    return ARCHITECTURE_PATH.read_text(encoding="utf-8")


def test_architecture_md_exists() -> None:
    """ARCHITECTURE.md should exist at the repository root."""
    assert ARCHITECTURE_PATH.exists()


def test_architecture_md_has_required_sections(architecture_content: str) -> None:
    """ARCHITECTURE.md should contain all 8 required section headings."""
    required_sections = [
        "## 1. Overview",
        "## 2. Backend Architecture",
        "## 3. Database Schema",
        "## 4. API Endpoints",
        "## 5. Frontend Architecture",
        "## 6. File Structure",
        "## 7. CORS Configuration",
        "## 8. Development Workflow",
    ]
    for section in required_sections:
        assert section in architecture_content, (
            f"Missing section: {section}"
        )


def test_architecture_md_has_all_endpoints(architecture_content: str) -> None:
    """ARCHITECTURE.md should document all five REST endpoints."""
    endpoints = [
        "GET /tasks",
        "GET /tasks/{id}",
        "POST /tasks",
        "PUT /tasks/{id}",
        "DELETE /tasks/{id}",
    ]
    for endpoint in endpoints:
        assert endpoint in architecture_content, (
            f"Missing endpoint: {endpoint}"
        )


def test_architecture_md_has_all_components(architecture_content: str) -> None:
    """ARCHITECTURE.md should reference all frontend components."""
    components = [
        "App",
        "HomePage",
        "TaskList",
        "TaskCard",
        "StatusBadge",
        "TaskForm",
    ]
    for component in components:
        assert component in architecture_content, (
            f"Missing component: {component}"
        )


def test_architecture_md_has_status_values(architecture_content: str) -> None:
    """ARCHITECTURE.md should document all three status values."""
    for status in ["todo", "in-progress", "done"]:
        assert status in architecture_content, (
            f"Missing status value: {status}"
        )


def test_architecture_md_cors_uses_http(architecture_content: str) -> None:
    """CORS origin should use http (not https) for localhost."""
    assert "http://localhost:5173" in architecture_content


def test_architecture_md_mentions_due_date_nullable(
    architecture_content: str,
) -> None:
    """ARCHITECTURE.md should indicate due_date is nullable."""
    lower = architecture_content.lower()
    assert "nullable" in lower or "optional" in lower or "null" in lower
