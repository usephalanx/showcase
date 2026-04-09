"""Tests for supporting files required by main.tsx imports.

Verifies that App.tsx and index.css exist so the entry point can
resolve its imports.
"""

from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent.parent / "src"


def test_app_component_exists() -> None:
    """src/App.tsx must exist (imported by main.tsx)."""
    assert (SRC_DIR / "App.tsx").exists(), "Expected src/App.tsx to exist"


def test_index_css_exists() -> None:
    """src/index.css must exist (imported by main.tsx)."""
    assert (SRC_DIR / "index.css").exists(), "Expected src/index.css to exist"


def test_app_component_exports_default() -> None:
    """src/App.tsx must have a default export."""
    content = (SRC_DIR / "App.tsx").read_text(encoding="utf-8")
    assert "export default" in content, "App.tsx must have a default export"
