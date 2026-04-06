"""Tests for frontend/src/main.tsx.

Verifies that the React entry point file exists and renders the App
component with the expected setup.
"""

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
MAIN_PATH = REPO_ROOT / "frontend" / "src" / "main.tsx"


def _read_main() -> str:
    """Read and return the full content of main.tsx."""
    return MAIN_PATH.read_text(encoding="utf-8")


def test_main_file_exists() -> None:
    """main.tsx must exist at frontend/src/main.tsx."""
    assert MAIN_PATH.exists(), "frontend/src/main.tsx not found"


def test_main_imports_react() -> None:
    """main.tsx must import React."""
    content = _read_main()
    assert "import React" in content


def test_main_imports_react_dom() -> None:
    """main.tsx must import ReactDOM."""
    content = _read_main()
    assert "import ReactDOM" in content or "from 'react-dom" in content


def test_main_imports_app() -> None:
    """main.tsx must import the App component."""
    content = _read_main()
    assert "import App" in content


def test_main_uses_create_root() -> None:
    """main.tsx must use React 18 createRoot API."""
    content = _read_main()
    assert "createRoot" in content


def test_main_uses_strict_mode() -> None:
    """main.tsx must wrap App in React.StrictMode."""
    content = _read_main()
    assert "StrictMode" in content


def test_main_targets_root_element() -> None:
    """main.tsx must mount into an element with id 'root'."""
    content = _read_main()
    assert "getElementById('root')" in content or 'getElementById("root")' in content
