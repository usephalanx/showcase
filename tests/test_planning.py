"""Tests to validate PLANNING.md architecture document.

These tests mirror the validation checks in scripts/validate_planning.py
but are structured as proper pytest tests for CI integration.
"""

import re
from pathlib import Path
from typing import List, Tuple

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
PLANNING_PATH = REPO_ROOT / "PLANNING.md"


@pytest.fixture()
def planning_content() -> str:
    """Load and return the contents of PLANNING.md."""
    assert PLANNING_PATH.exists(), f"PLANNING.md not found at {PLANNING_PATH}"
    return PLANNING_PATH.read_text(encoding="utf-8")


def _get_h2_sections(content: str) -> List[Tuple[str, str]]:
    """Parse PLANNING.md and return list of (heading, body) tuples for each H2 section."""
    sections: List[Tuple[str, str]] = []
    parts = re.split(r"^## ", content, flags=re.MULTILINE)
    for part in parts[1:]:
        lines = part.split("\n", 1)
        heading = lines[0].strip()
        body = lines[1] if len(lines) > 1 else ""
        sections.append((heading, body))
    return sections


def test_planning_md_exists() -> None:
    """Verify PLANNING.md exists at repo root."""
    assert PLANNING_PATH.exists(), f"PLANNING.md not found at {PLANNING_PATH}"


def test_planning_md_minimum_length(planning_content: str) -> None:
    """Verify PLANNING.md is at least 500 lines long."""
    line_count = len(planning_content.splitlines())
    assert line_count >= 500, (
        f"PLANNING.md has {line_count} lines, expected at least 500"
    )


def test_required_sections_present(planning_content: str) -> None:
    """Verify all required H2 sections exist in PLANNING.md."""
    sections = _get_h2_sections(planning_content)
    section_names = [name for name, _ in sections]

    required_sections = [
        "Tech Stack",
        "Project Structure",
        "Data Models",
        "API Endpoints",
        "URL Structure",
        "Frontend Components",
        "Meta Tag Strategy",
        "State Management",
        "Database Indexes",
        "Docker Setup",
    ]

    for required in required_sections:
        assert required in section_names, (
            f"Required section '## {required}' not found. "
            f"Found sections: {section_names}"
        )


def test_api_endpoints_documented(planning_content: str) -> None:
    """Verify at least 20 API endpoint definitions are present."""
    endpoint_pattern = re.compile(
        r"(GET|POST|PUT|DELETE|PATCH)\s+\|?\s*/api/v1/", re.IGNORECASE
    )
    matches = endpoint_pattern.findall(planning_content)
    assert len(matches) >= 20, (
        f"Found {len(matches)} API endpoint definitions, expected at least 20"
    )


def test_data_models_documented(planning_content: str) -> None:
    """Verify Board, Column, Card, Category, Tag model names appear."""
    required_models = ["Board", "Column", "Card", "Category", "Tag"]
    for model in required_models:
        assert model in planning_content, (
            f"Data model '{model}' not found in PLANNING.md"
        )


def test_frontend_components_documented(planning_content: str) -> None:
    """Verify at least 15 component file paths are listed."""
    component_pattern = re.compile(r"src/(components|pages)/\S+\.tsx")
    matches = component_pattern.findall(planning_content)
    assert len(matches) >= 15, (
        f"Found {len(matches)} component file paths, expected at least 15"
    )


def test_seo_strategy_documented(planning_content: str) -> None:
    """Verify Open Graph, canonical, JSON-LD, and React Helmet are mentioned."""
    seo_terms = ["Open Graph", "canonical", "JSON-LD", "React Helmet"]
    for term in seo_terms:
        assert term in planning_content, (
            f"SEO term '{term}' not found in PLANNING.md"
        )


def test_no_empty_sections(planning_content: str) -> None:
    """Verify no H2 section is followed immediately by another H2 (empty section)."""
    sections = _get_h2_sections(planning_content)
    for heading, body in sections:
        stripped = body.strip()
        assert len(stripped) > 0, (
            f"Section '## {heading}' appears to be empty"
        )


def test_slug_strategy_documented(planning_content: str) -> None:
    """Verify slug generation and collision strategy is documented."""
    assert "slug" in planning_content.lower()
    assert "collision" in planning_content.lower() or "Collision" in planning_content


def test_cascade_behavior_documented(planning_content: str) -> None:
    """Verify cascade delete behavior is documented."""
    assert "cascade" in planning_content.lower()


def test_performance_limits_documented(planning_content: str) -> None:
    """Verify performance limits are documented."""
    content_lower = planning_content.lower()
    assert "maximum" in content_lower or "limit" in content_lower or "max" in content_lower
