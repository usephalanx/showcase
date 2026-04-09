"""Tests for src/main.tsx — application entry point.

Verifies that main.tsx exists and contains the required imports and
render call.
"""

from pathlib import Path

MAIN_FILE = Path(__file__).resolve().parent.parent / "src" / "main.tsx"


def test_main_file_exists() -> None:
    """src/main.tsx must exist."""
    assert MAIN_FILE.exists(), f"Expected {MAIN_FILE} to exist"


def test_main_imports_react() -> None:
    """main.tsx must import React."""
    content = MAIN_FILE.read_text(encoding="utf-8")
    assert "import React" in content or "from 'react'" in content, (
        "main.tsx must import React"
    )


def test_main_imports_react_dom() -> None:
    """main.tsx must import ReactDOM from react-dom/client."""
    content = MAIN_FILE.read_text(encoding="utf-8")
    assert "react-dom/client" in content, (
        "main.tsx must import from 'react-dom/client'"
    )


def test_main_imports_app() -> None:
    """main.tsx must import the App component."""
    content = MAIN_FILE.read_text(encoding="utf-8")
    assert "import App" in content or "import { App }" in content, (
        "main.tsx must import App component"
    )


def test_main_imports_index_css() -> None:
    """main.tsx must import index.css."""
    content = MAIN_FILE.read_text(encoding="utf-8")
    assert "index.css" in content, "main.tsx must import index.css"


def test_main_renders_app_into_root() -> None:
    """main.tsx must call createRoot with the 'root' element and render App."""
    content = MAIN_FILE.read_text(encoding="utf-8")
    assert "createRoot" in content, "main.tsx must use createRoot"
    assert "getElementById('root')" in content or 'getElementById("root")' in content, (
        "main.tsx must target the 'root' DOM element"
    )
    assert "<App" in content, "main.tsx must render <App />"
