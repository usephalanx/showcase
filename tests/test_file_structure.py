"""Test suite for validating the expected project file structure.

Verifies that all required files and directories exist, that the
src/components/ directory contains exactly the expected component files,
that package.json references the correct dependencies, and that
src/types.ts contains the expected type definitions.
"""

import os
from pathlib import Path
from typing import List

import pytest

# Root of the repository is one level above the tests/ directory.
ROOT: Path = Path(__file__).resolve().parent.parent


# ------------------------------------------------------------------
# Individual file-existence tests
# ------------------------------------------------------------------

EXPECTED_FILES: List[str] = [
    "package.json",
    "vite.config.ts",
    "tsconfig.json",
    "index.html",
    "src/main.tsx",
    "src/App.tsx",
    "src/App.css",
    "src/types.ts",
    "src/vite-env.d.ts",
    "src/components/TodoInput.tsx",
    "src/components/TodoItem.tsx",
    "src/components/TodoList.tsx",
    "RUNNING.md",
    "ARCHITECTURE.md",
]


@pytest.mark.parametrize("relative_path", EXPECTED_FILES)
def test_file_exists(relative_path: str) -> None:
    """Verify that each expected project file exists on disk."""
    full_path: Path = ROOT / relative_path
    assert full_path.exists(), f"Expected file not found: {relative_path}"
    assert full_path.is_file(), f"Path exists but is not a file: {relative_path}"


@pytest.mark.parametrize("relative_path", EXPECTED_FILES)
def test_file_exists_os_path(relative_path: str) -> None:
    """Verify file existence using os.path.exists as a secondary check."""
    full_path: str = os.path.join(str(ROOT), relative_path)
    assert os.path.exists(full_path), f"os.path.exists failed for: {relative_path}"


# ------------------------------------------------------------------
# Components directory structure
# ------------------------------------------------------------------


def test_components_directory_contains_exactly_three_files() -> None:
    """Verify src/components/ contains exactly the 3 expected component files."""
    components_dir: Path = ROOT / "src" / "components"
    assert components_dir.exists(), "src/components/ directory does not exist"
    assert components_dir.is_dir(), "src/components is not a directory"

    expected_component_files = {
        "TodoInput.tsx",
        "TodoItem.tsx",
        "TodoList.tsx",
    }

    actual_files = {f.name for f in components_dir.iterdir() if f.is_file()}

    assert actual_files == expected_component_files, (
        f"Expected exactly {expected_component_files} in src/components/, "
        f"but found {actual_files}"
    )


# ------------------------------------------------------------------
# package.json content validation
# ------------------------------------------------------------------


def test_package_json_contains_required_dependencies() -> None:
    """Verify package.json contains 'react', 'typescript', and 'vite' as substrings."""
    package_json_path: Path = ROOT / "package.json"
    assert package_json_path.exists(), "package.json does not exist"

    content: str = package_json_path.read_text(encoding="utf-8")

    assert "react" in content, "package.json does not contain 'react'"
    assert "typescript" in content, "package.json does not contain 'typescript'"
    assert "vite" in content, "package.json does not contain 'vite'"


# ------------------------------------------------------------------
# src/types.ts content validation
# ------------------------------------------------------------------


def test_types_ts_contains_todo_and_completed() -> None:
    """Verify src/types.ts contains 'Todo' and 'completed'."""
    types_path: Path = ROOT / "src" / "types.ts"
    assert types_path.exists(), "src/types.ts does not exist"

    content: str = types_path.read_text(encoding="utf-8")

    assert "Todo" in content, "src/types.ts does not contain 'Todo'"
    assert "completed" in content, "src/types.ts does not contain 'completed'"
