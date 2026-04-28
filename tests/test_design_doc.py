"""Tests to validate that docs/design.md contains all required specification elements.

These tests read the design document from disk and assert that every
required section and value is present, ensuring the document remains
complete and accurate as a source-of-truth for implementation.
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest

# Resolve the path to docs/design.md relative to the repository root.
# The tests directory sits at <root>/tests/, so we go one level up.
_REPO_ROOT: Path = Path(__file__).resolve().parent.parent
_DESIGN_DOC_PATH: Path = _REPO_ROOT / "docs" / "design.md"


@pytest.fixture(scope="module")
def design_doc_content() -> str:
    """Read and return the full text content of docs/design.md."""
    assert _DESIGN_DOC_PATH.exists(), f"Design doc not found at {_DESIGN_DOC_PATH}"
    return _DESIGN_DOC_PATH.read_text(encoding="utf-8")


def test_design_doc_exists() -> None:
    """Assert that docs/design.md exists on disk and is non-empty."""
    assert _DESIGN_DOC_PATH.exists(), f"Expected file at {_DESIGN_DOC_PATH}"
    assert _DESIGN_DOC_PATH.stat().st_size > 0, "Design doc is empty"


def test_design_doc_contains_route(design_doc_content: str) -> None:
    """Assert that the exact route string 'GET /api/hello' appears in the document."""
    assert "GET /api/hello" in design_doc_content


def test_design_doc_contains_response_body(design_doc_content: str) -> None:
    """Assert that the response body key-value '"message": "hello"' appears in the document."""
    assert '"message": "hello"' in design_doc_content


def test_design_doc_contains_status_code(design_doc_content: str) -> None:
    """Assert that HTTP status code 200 is documented."""
    assert "200" in design_doc_content


def test_design_doc_contains_technology_stack(design_doc_content: str) -> None:
    """Assert that both 'Flask' and 'Python' are named in the technology stack."""
    assert "Flask" in design_doc_content
    assert "Python" in design_doc_content


def test_design_doc_contains_error_handling(design_doc_content: str) -> None:
    """Assert that 404 error handling is documented with a JSON error body."""
    assert "404" in design_doc_content
    assert '"error"' in design_doc_content


def test_design_doc_contains_project_structure(design_doc_content: str) -> None:
    """Assert that the expected project files are listed in the document."""
    assert "app.py" in design_doc_content
    assert "requirements.txt" in design_doc_content


def test_design_doc_contains_content_type(design_doc_content: str) -> None:
    """Assert that Content-Type application/json is explicitly stated."""
    assert "application/json" in design_doc_content


def test_design_doc_contains_curl_example(design_doc_content: str) -> None:
    """Assert that a curl request example is included."""
    assert "curl" in design_doc_content


def test_design_doc_contains_overview_section(design_doc_content: str) -> None:
    """Assert that the Overview section heading exists."""
    assert "## Overview" in design_doc_content


def test_design_doc_contains_error_handling_section(design_doc_content: str) -> None:
    """Assert that the Error Handling section heading exists."""
    assert "## Error Handling" in design_doc_content


def test_design_doc_contains_future_considerations_section(design_doc_content: str) -> None:
    """Assert that the Future Considerations section heading exists."""
    assert "## Future Considerations" in design_doc_content
