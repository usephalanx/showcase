"""Tests for backend/requirements.txt contents.

Ensures the requirements file exists and declares the expected
core dependencies.
"""

from __future__ import annotations

from pathlib import Path

import pytest

REQUIREMENTS_PATH = Path(__file__).resolve().parent.parent / "backend" / "requirements.txt"


def _read_requirements() -> str:
    """Read and return the raw contents of requirements.txt."""
    assert REQUIREMENTS_PATH.exists(), f"{REQUIREMENTS_PATH} does not exist"
    return REQUIREMENTS_PATH.read_text(encoding="utf-8")


def test_requirements_file_exists() -> None:
    """backend/requirements.txt must exist."""
    assert REQUIREMENTS_PATH.is_file()


@pytest.mark.parametrize(
    "package",
    ["fastapi", "uvicorn", "sqlalchemy", "pydantic"],
)
def test_requirements_contains_package(package: str) -> None:
    """Each core dependency must appear in requirements.txt."""
    contents = _read_requirements().lower()
    assert package in contents, f"{package} not found in requirements.txt"
