"""Tests to verify that all expected project files and directories exist.

Uses pytest and pathlib to check the presence of every file required
by the React + Vite + TypeScript Todo application.
"""

from pathlib import Path

import pytest

# The project root is the parent of the 'tests/' directory.
PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent


# -- Expected files ----------------------------------------------------------

EXPECTED_FILES = [
    "package.json",
    "vite.config.ts",
    "tsconfig.json",
    "index.html",
    "src/main.tsx",
    "src/App.tsx",
    "src/App.css",
    "src/index.css",
    "src/types.ts",
    "src/components/TodoInput.tsx",
    "src/components/TodoItem.tsx",
    "src/components/TodoList.tsx",
]


@pytest.mark.parametrize("relative_path", EXPECTED_FILES)
def test_file_exists(relative_path: str) -> None:
    """Verify that the expected project file exists at the given path."""
    full_path: Path = PROJECT_ROOT / relative_path
    assert full_path.exists(), f"Expected file not found: {relative_path}"
    assert full_path.is_file(), f"Path exists but is not a file: {relative_path}"


# -- Expected directories ----------------------------------------------------

EXPECTED_DIRECTORIES = [
    "src",
    "src/components",
]


@pytest.mark.parametrize("relative_dir", EXPECTED_DIRECTORIES)
def test_directory_exists(relative_dir: str) -> None:
    """Verify that the expected project directory exists at the given path."""
    full_path: Path = PROJECT_ROOT / relative_dir
    assert full_path.exists(), f"Expected directory not found: {relative_dir}"
    assert full_path.is_dir(), f"Path exists but is not a directory: {relative_dir}"
