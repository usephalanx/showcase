"""Structure validation tests.

Verifies that all required project files exist in the repository root.
"""

import os
from pathlib import Path

# Project root is the parent of the tests/ directory.
PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent

REQUIRED_FILES = [
    "package.json",
    "vite.config.ts",
    "src/main.tsx",
    "src/App.tsx",
    "index.html",
    "RUNNING.md",
]


def test_required_files_exist() -> None:
    """Assert that every required project file exists on disk."""
    for relative_path in REQUIRED_FILES:
        full_path = PROJECT_ROOT / relative_path
        assert os.path.exists(full_path), (
            f"Required file missing: {relative_path} "
            f"(looked at {full_path})"
        )
