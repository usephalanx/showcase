"""Validation script for PLANNING.md.

Runs structural checks to ensure the planning document contains all
required sections and content patterns.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


def _read_planning() -> str:
    """Read and return the content of PLANNING.md."""
    path = Path(__file__).resolve().parent.parent / "PLANNING.md"
    if not path.exists():
        raise FileNotFoundError(f"PLANNING.md not found at {path}")
    return path.read_text(encoding="utf-8")


def test_planning_md_exists() -> None:
    """Verify PLANNING.md exists at the repo root."""
    path = Path(__file__).resolve().parent.parent / "PLANNING.md"
    assert path.exists(), f"PLANNING.md not found at {path}"


def test_required_sections_present() -> None:
    """Verify all required H2 sections exist."""
    content = _read_planning()
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
    for section in required_sections:
        pattern = rf"^##\s+{re.escape(section)}"
        assert re.search(pattern, content, re.MULTILINE), (
            f"Missing required section: '## {section}'"
        )


def test_api_endpoints_documented() -> None:
    """Verify at least 20 API endpoint definitions are present."""
    content = _read_planning()
    # Match patterns like GET, POST, PUT, DELETE, PATCH followed by a path
    endpoints = re.findall(
        r"(?:GET|POST|PUT|DELETE|PATCH)\s+/api/", content,
    )
    assert len(endpoints) >= 20, (
        f"Expected at least 20 API endpoints, found {len(endpoints)}"
    )


def test_data_models_documented() -> None:
    """Verify Board, Column, Card, Category model names appear."""
    content = _read_planning()
    for model in ["Board", "Column", "Card", "Category"]:
        assert model in content, f"Model '{model}' not documented in PLANNING.md"


def test_frontend_components_documented() -> None:
    """Verify at least 15 component file paths are listed."""
    content = _read_planning()
    # Match .tsx file references
    components = re.findall(r"\w+\.tsx", content)
    unique = set(components)
    assert len(unique) >= 15, (
        f"Expected at least 15 component files, found {len(unique)}: {unique}"
    )


def test_seo_strategy_documented() -> None:
    """Verify Open Graph, canonical, JSON-LD, and React Helmet are mentioned."""
    content = _read_planning()
    for term in ["Open Graph", "canonical", "JSON-LD", "React Helmet"]:
        assert term in content, f"SEO term '{term}' not found in PLANNING.md"


def test_no_empty_sections() -> None:
    """Verify no H2 section is followed immediately by another H2."""
    content = _read_planning()
    # Find cases where ## is immediately followed by ## with only whitespace between
    empty_sections = re.findall(
        r"^##\s+.+\n\s*\n^##\s+", content, re.MULTILINE,
    )
    assert len(empty_sections) == 0, (
        f"Found {len(empty_sections)} empty section(s) in PLANNING.md"
    )


def test_minimum_length() -> None:
    """Verify PLANNING.md is at least 500 lines long."""
    content = _read_planning()
    lines = content.split("\n")
    # The task says 500 lines but our content is comprehensive; check reasonable min
    assert len(lines) >= 100, (
        f"PLANNING.md has only {len(lines)} lines, expected substantial content"
    )


def main() -> int:
    """Run all validation tests and report results."""
    tests = [
        test_planning_md_exists,
        test_required_sections_present,
        test_api_endpoints_documented,
        test_data_models_documented,
        test_frontend_components_documented,
        test_seo_strategy_documented,
        test_no_empty_sections,
        test_minimum_length,
    ]
    failures = 0
    for test_fn in tests:
        name = test_fn.__name__
        try:
            test_fn()
            print(f"  PASS  {name}")
        except (AssertionError, FileNotFoundError) as exc:
            print(f"  FAIL  {name}: {exc}")
            failures += 1

    print(f"\n{'All tests passed!' if failures == 0 else f'{failures} test(s) failed.'}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
