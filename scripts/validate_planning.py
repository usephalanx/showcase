#!/usr/bin/env python3
"""Validation script for PLANNING.md.

Runs structural checks to ensure the architecture document meets
all required criteria. Can be executed directly or via pytest.
"""

import os
import re
import sys
from pathlib import Path

# Determine the repo root (one level up from scripts/)
REPO_ROOT = Path(__file__).resolve().parent.parent
PLANNING_PATH = REPO_ROOT / "PLANNING.md"


def _read_planning() -> str:
    """Read and return the contents of PLANNING.md."""
    if not PLANNING_PATH.exists():
        raise FileNotFoundError(f"PLANNING.md not found at {PLANNING_PATH}")
    return PLANNING_PATH.read_text(encoding="utf-8")


def _get_h2_sections(content: str) -> list[tuple[str, str]]:
    """Parse PLANNING.md and return list of (heading, body) tuples for each H2 section."""
    sections: list[tuple[str, str]] = []
    # Split on H2 markers
    parts = re.split(r"^## ", content, flags=re.MULTILINE)
    for part in parts[1:]:  # skip content before first H2
        lines = part.split("\n", 1)
        heading = lines[0].strip()
        body = lines[1] if len(lines) > 1 else ""
        sections.append((heading, body))
    return sections


def test_planning_md_exists() -> None:
    """Verify PLANNING.md exists at repo root."""
    assert PLANNING_PATH.exists(), f"PLANNING.md not found at {PLANNING_PATH}"


def test_planning_md_minimum_length() -> None:
    """Verify PLANNING.md is at least 500 lines long."""
    content = _read_planning()
    line_count = len(content.splitlines())
    assert line_count >= 500, (
        f"PLANNING.md has {line_count} lines, expected at least 500"
    )


def test_required_sections_present() -> None:
    """Verify all required H2 sections exist in PLANNING.md."""
    content = _read_planning()
    sections = _get_h2_sections(content)
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


def test_api_endpoints_documented() -> None:
    """Verify at least 20 API endpoint definitions are present."""
    content = _read_planning()
    # Match patterns like: | GET    | /api/v1/...
    # or GET /api/v1/...
    endpoint_pattern = re.compile(
        r"(GET|POST|PUT|DELETE|PATCH)\s+\|?\s*/api/v1/", re.IGNORECASE
    )
    matches = endpoint_pattern.findall(content)
    assert len(matches) >= 20, (
        f"Found {len(matches)} API endpoint definitions, expected at least 20"
    )


def test_data_models_documented() -> None:
    """Verify Board, Column, Card, Category, Tag model names appear."""
    content = _read_planning()
    required_models = ["Board", "Column", "Card", "Category", "Tag"]
    for model in required_models:
        assert model in content, (
            f"Data model '{model}' not found in PLANNING.md"
        )


def test_frontend_components_documented() -> None:
    """Verify at least 15 component file paths are listed."""
    content = _read_planning()
    # Match patterns like src/components/... .tsx or src/pages/... .tsx
    component_pattern = re.compile(r"src/(components|pages)/\S+\.tsx")
    matches = component_pattern.findall(content)
    assert len(matches) >= 15, (
        f"Found {len(matches)} component file paths, expected at least 15"
    )


def test_seo_strategy_documented() -> None:
    """Verify Open Graph, canonical, JSON-LD, and React Helmet are mentioned."""
    content = _read_planning()
    seo_terms = ["Open Graph", "canonical", "JSON-LD", "React Helmet"]
    for term in seo_terms:
        assert term in content, (
            f"SEO term '{term}' not found in PLANNING.md"
        )


def test_no_empty_sections() -> None:
    """Verify no H2 section is followed immediately by another H2 (empty section)."""
    content = _read_planning()
    sections = _get_h2_sections(content)
    for heading, body in sections:
        # Strip whitespace and check if body has any meaningful content
        stripped = body.strip()
        assert len(stripped) > 0, (
            f"Section '## {heading}' appears to be empty"
        )


def main() -> int:
    """Run all validation tests and report results."""
    tests = [
        test_planning_md_exists,
        test_planning_md_minimum_length,
        test_required_sections_present,
        test_api_endpoints_documented,
        test_data_models_documented,
        test_frontend_components_documented,
        test_seo_strategy_documented,
        test_no_empty_sections,
    ]

    passed = 0
    failed = 0

    for test_fn in tests:
        name = test_fn.__name__
        try:
            test_fn()
            print(f"  ✓ {name}")
            passed += 1
        except (AssertionError, FileNotFoundError) as e:
            print(f"  ✗ {name}: {e}")
            failed += 1

    print(f"\nResults: {passed} passed, {failed} failed")
    return 1 if failed > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
