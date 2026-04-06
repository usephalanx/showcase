"""Tests for the ARCHITECTURE.md documentation file.

Validates that the architecture document exists, contains all required
sections, references every API endpoint, and mentions all frontend
components.
"""

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
ARCHITECTURE_PATH = REPO_ROOT / "ARCHITECTURE.md"


def _read_architecture() -> str:
    """Read and return the full content of ARCHITECTURE.md."""
    return ARCHITECTURE_PATH.read_text(encoding="utf-8")


def test_architecture_md_exists() -> None:
    """ARCHITECTURE.md must exist at the repository root."""
    assert ARCHITECTURE_PATH.exists(), "ARCHITECTURE.md not found at repo root"


def test_architecture_md_has_required_sections() -> None:
    """ARCHITECTURE.md must contain all eight section headings."""
    content = _read_architecture()
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
        assert section in content, f"Missing section: {section}"


def test_architecture_md_has_all_endpoints() -> None:
    """ARCHITECTURE.md must document every REST endpoint."""
    content = _read_architecture()
    endpoints = [
        "GET /tasks",
        "GET /tasks/{id}",
        "POST /tasks",
        "PUT /tasks/{id}",
        "DELETE /tasks/{id}",
    ]
    for endpoint in endpoints:
        assert endpoint in content, f"Missing endpoint: {endpoint}"


def test_architecture_md_has_all_components() -> None:
    """ARCHITECTURE.md must mention all planned React components."""
    content = _read_architecture()
    components = [
        "App",
        "HomePage",
        "TaskList",
        "TaskCard",
        "TaskForm",
        "StatusBadge",
    ]
    for component in components:
        assert component in content, f"Missing component: {component}"


def test_architecture_md_status_values() -> None:
    """ARCHITECTURE.md must reference all three status values."""
    content = _read_architecture()
    for status in ["todo", "in-progress", "done"]:
        assert status in content, f"Missing status value: {status}"


def test_architecture_md_cors_origin() -> None:
    """CORS origin must use http (not https) for localhost."""
    content = _read_architecture()
    assert "http://localhost:5173" in content, "Missing CORS origin http://localhost:5173"


def test_architecture_md_due_date_nullable() -> None:
    """due_date must be documented as nullable."""
    content = _read_architecture()
    assert "NULLABLE" in content or "null" in content, "due_date nullable documentation missing"
