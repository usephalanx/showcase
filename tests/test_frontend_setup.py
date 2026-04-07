"""Tests to verify the frontend project setup files exist and are well-formed."""

import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent


def test_package_json_exists() -> None:
    """package.json must exist at the repository root."""
    assert (ROOT / "package.json").is_file()


def test_package_json_has_required_dependencies() -> None:
    """package.json must list all required dependencies."""
    data = json.loads((ROOT / "package.json").read_text())
    deps = set(data.get("dependencies", {}).keys())
    dev_deps = set(data.get("devDependencies", {}).keys())
    all_deps = deps | dev_deps

    required = {
        "react",
        "react-dom",
        "typescript",
        "vite",
        "@vitejs/plugin-react",
        "vitest",
        "@testing-library/react",
        "@testing-library/jest-dom",
    }
    missing = required - all_deps
    assert not missing, f"Missing dependencies in package.json: {missing}"


def test_vite_config_exists() -> None:
    """vite.config.ts must exist at the repository root."""
    assert (ROOT / "vite.config.ts").is_file()


def test_vite_config_contains_react_plugin() -> None:
    """vite.config.ts must import and use the React plugin."""
    content = (ROOT / "vite.config.ts").read_text()
    assert "@vitejs/plugin-react" in content
    assert "react()" in content


def test_tsconfig_exists() -> None:
    """tsconfig.json must exist at the repository root."""
    assert (ROOT / "tsconfig.json").is_file()


def test_tsconfig_node_exists() -> None:
    """tsconfig.node.json must exist at the repository root."""
    assert (ROOT / "tsconfig.node.json").is_file()


def test_tsconfig_has_jsx() -> None:
    """tsconfig.json must enable JSX for React."""
    data = json.loads((ROOT / "tsconfig.json").read_text())
    jsx = data.get("compilerOptions", {}).get("jsx", "")
    assert "react" in jsx.lower(), f"Expected react-jsx, got: {jsx}"


def test_index_html_exists() -> None:
    """index.html must exist at the repository root."""
    assert (ROOT / "index.html").is_file()


def test_index_html_has_root_div() -> None:
    """index.html must contain a div with id='root'."""
    content = (ROOT / "index.html").read_text()
    assert 'id="root"' in content


def test_index_html_references_main_tsx() -> None:
    """index.html must reference the main.tsx entry point."""
    content = (ROOT / "index.html").read_text()
    assert "src/main.tsx" in content


def test_main_tsx_exists() -> None:
    """src/main.tsx must exist."""
    assert (ROOT / "src" / "main.tsx").is_file()


def test_main_tsx_imports_app() -> None:
    """src/main.tsx must import the App component."""
    content = (ROOT / "src" / "main.tsx").read_text()
    assert "import" in content and "App" in content


def test_main_tsx_uses_createroot() -> None:
    """src/main.tsx must use createRoot for React 18 rendering."""
    content = (ROOT / "src" / "main.tsx").read_text()
    assert "createRoot" in content


def test_app_tsx_exists() -> None:
    """src/App.tsx must exist."""
    assert (ROOT / "src" / "App.tsx").is_file()


def test_app_tsx_imports_todo_page() -> None:
    """src/App.tsx must import TodoPage."""
    content = (ROOT / "src" / "App.tsx").read_text()
    assert "TodoPage" in content


def test_todo_page_exists() -> None:
    """src/pages/TodoPage.tsx must exist."""
    assert (ROOT / "src" / "pages" / "TodoPage.tsx").is_file()


def test_index_css_exists() -> None:
    """src/index.css must exist."""
    assert (ROOT / "src" / "index.css").is_file()


def test_index_css_has_reset() -> None:
    """src/index.css must contain a box-sizing reset."""
    content = (ROOT / "src" / "index.css").read_text()
    assert "box-sizing" in content


def test_setup_tests_exists() -> None:
    """src/setupTests.ts must exist for vitest setup."""
    assert (ROOT / "src" / "setupTests.ts").is_file()


def test_architecture_md_exists() -> None:
    """ARCHITECTURE.md must exist at the repository root."""
    assert (ROOT / "ARCHITECTURE.md").is_file()


def test_architecture_md_has_todo_interface() -> None:
    """ARCHITECTURE.md must define the Todo interface with required fields."""
    content = (ROOT / "ARCHITECTURE.md").read_text()
    assert "id: string" in content or "id:" in content
    assert "text: string" in content or "text:" in content
    assert "completed: boolean" in content or "completed:" in content
    assert "createdAt: number" in content or "createdAt:" in content


def test_architecture_md_has_filter_type() -> None:
    """ARCHITECTURE.md must define the FilterType union."""
    content = (ROOT / "ARCHITECTURE.md").read_text()
    assert "FilterType" in content
    assert "all" in content
    assert "active" in content
    assert "completed" in content


def test_architecture_md_has_file_structure_section() -> None:
    """ARCHITECTURE.md must contain a File Structure section."""
    content = (ROOT / "ARCHITECTURE.md").read_text()
    assert "File Structure" in content
