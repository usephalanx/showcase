"""Structural tests for the Hello World React App.

Validates that all required project files exist and contain the expected
content markers.  These tests do NOT require Node.js or npm install —
they only inspect the source files on disk.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

import pytest

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

ROOT: Path = Path(__file__).resolve().parent.parent


def _read(relative_path: str) -> str:
    """Read and return the text content of a file relative to the project root.

    Args:
        relative_path: Path relative to the repository root.

    Returns:
        The file contents as a string.
    """
    return (ROOT / relative_path).read_text(encoding="utf-8")


def _load_package_json() -> Dict[str, Any]:
    """Parse and return the package.json at the project root.

    Returns:
        A dictionary representing the parsed JSON.
    """
    return json.loads(_read("package.json"))


# ---------------------------------------------------------------------------
# package.json tests
# ---------------------------------------------------------------------------


class TestPackageJson:
    """Tests for package.json existence and content."""

    def test_exists(self) -> None:
        """package.json must exist at the repository root."""
        assert (ROOT / "package.json").is_file()

    def test_has_react_dependency(self) -> None:
        """react must be listed as a production dependency."""
        pkg = _load_package_json()
        assert "react" in pkg.get("dependencies", {})

    def test_has_react_dom_dependency(self) -> None:
        """react-dom must be listed as a production dependency."""
        pkg = _load_package_json()
        assert "react-dom" in pkg.get("dependencies", {})

    def test_has_vite_dev_dependency(self) -> None:
        """vite must be listed as a dev dependency."""
        pkg = _load_package_json()
        assert "vite" in pkg.get("devDependencies", {})

    def test_has_typescript_dev_dependency(self) -> None:
        """typescript must be listed as a dev dependency."""
        pkg = _load_package_json()
        assert "typescript" in pkg.get("devDependencies", {})

    def test_has_vitejs_plugin_react(self) -> None:
        """@vitejs/plugin-react must be listed as a dev dependency."""
        pkg = _load_package_json()
        assert "@vitejs/plugin-react" in pkg.get("devDependencies", {})

    def test_has_types_react(self) -> None:
        """@types/react must be listed as a dev dependency."""
        pkg = _load_package_json()
        assert "@types/react" in pkg.get("devDependencies", {})

    def test_has_types_react_dom(self) -> None:
        """@types/react-dom must be listed as a dev dependency."""
        pkg = _load_package_json()
        assert "@types/react-dom" in pkg.get("devDependencies", {})

    def test_dev_script(self) -> None:
        """The dev script must invoke vite."""
        pkg = _load_package_json()
        assert pkg.get("scripts", {}).get("dev") == "vite"

    def test_build_script(self) -> None:
        """The build script must invoke tsc and vite build."""
        pkg = _load_package_json()
        assert pkg.get("scripts", {}).get("build") == "tsc && vite build"

    def test_type_module(self) -> None:
        """package.json must set type to module for ESM support."""
        pkg = _load_package_json()
        assert pkg.get("type") == "module"

    def test_name(self) -> None:
        """package.json must have a name field."""
        pkg = _load_package_json()
        assert "name" in pkg
        assert len(pkg["name"]) > 0

    def test_private(self) -> None:
        """package.json should mark the project as private."""
        pkg = _load_package_json()
        assert pkg.get("private") is True


# ---------------------------------------------------------------------------
# vite.config.ts tests
# ---------------------------------------------------------------------------


class TestViteConfig:
    """Tests for vite.config.ts existence and content."""

    def test_exists(self) -> None:
        """vite.config.ts must exist at the repository root."""
        assert (ROOT / "vite.config.ts").is_file()

    def test_imports_react_plugin(self) -> None:
        """vite.config.ts must import @vitejs/plugin-react."""
        content = _read("vite.config.ts")
        assert "@vitejs/plugin-react" in content

    def test_imports_define_config(self) -> None:
        """vite.config.ts must import defineConfig from vite."""
        content = _read("vite.config.ts")
        assert "defineConfig" in content

    def test_uses_react_plugin(self) -> None:
        """vite.config.ts must call the react() plugin."""
        content = _read("vite.config.ts")
        assert "react()" in content


# ---------------------------------------------------------------------------
# tsconfig.json tests
# ---------------------------------------------------------------------------


class TestTsConfig:
    """Tests for tsconfig.json existence and content."""

    def test_exists(self) -> None:
        """tsconfig.json must exist at the repository root."""
        assert (ROOT / "tsconfig.json").is_file()

    def test_valid_json(self) -> None:
        """tsconfig.json must be valid JSON."""
        content = _read("tsconfig.json")
        parsed = json.loads(content)
        assert "compilerOptions" in parsed

    def test_jsx_react_jsx(self) -> None:
        """tsconfig.json must set jsx to react-jsx."""
        parsed = json.loads(_read("tsconfig.json"))
        assert parsed["compilerOptions"].get("jsx") == "react-jsx"

    def test_strict_mode(self) -> None:
        """tsconfig.json must enable strict mode."""
        parsed = json.loads(_read("tsconfig.json"))
        assert parsed["compilerOptions"].get("strict") is True

    def test_includes_src(self) -> None:
        """tsconfig.json must include the src directory."""
        parsed = json.loads(_read("tsconfig.json"))
        assert "src" in parsed.get("include", [])


# ---------------------------------------------------------------------------
# index.html tests
# ---------------------------------------------------------------------------


class TestIndexHtml:
    """Tests for index.html existence and content."""

    def test_exists(self) -> None:
        """index.html must exist at the repository root."""
        assert (ROOT / "index.html").is_file()

    def test_has_root_div(self) -> None:
        """index.html must contain a div with id='root'."""
        content = _read("index.html")
        assert 'id="root"' in content

    def test_has_module_script(self) -> None:
        """index.html must reference the main.tsx entry point as a module."""
        content = _read("index.html")
        assert 'type="module"' in content
        assert "src/main.tsx" in content

    def test_has_doctype(self) -> None:
        """index.html must start with a DOCTYPE declaration."""
        content = _read("index.html")
        assert content.strip().startswith("<!DOCTYPE html>")

    def test_has_title(self) -> None:
        """index.html must contain a title element."""
        content = _read("index.html")
        assert "<title>" in content

    def test_has_centering_styles(self) -> None:
        """index.html must include CSS for centering content."""
        content = _read("index.html")
        assert "justify-content" in content
        assert "align-items" in content

    def test_has_charset(self) -> None:
        """index.html must declare UTF-8 charset."""
        content = _read("index.html")
        assert 'charset="UTF-8"' in content

    def test_has_viewport_meta(self) -> None:
        """index.html must include a viewport meta tag."""
        content = _read("index.html")
        assert "viewport" in content


# ---------------------------------------------------------------------------
# src/main.tsx tests
# ---------------------------------------------------------------------------


class TestMainTsx:
    """Tests for src/main.tsx existence and content."""

    def test_exists(self) -> None:
        """src/main.tsx must exist."""
        assert (ROOT / "src" / "main.tsx").is_file()

    def test_imports_react(self) -> None:
        """src/main.tsx must import React."""
        content = _read("src/main.tsx")
        assert "import React" in content

    def test_imports_react_dom(self) -> None:
        """src/main.tsx must import from react-dom/client."""
        content = _read("src/main.tsx")
        assert "react-dom/client" in content

    def test_imports_app(self) -> None:
        """src/main.tsx must import the App component."""
        content = _read("src/main.tsx")
        assert "import App" in content

    def test_uses_create_root(self) -> None:
        """src/main.tsx must call createRoot."""
        content = _read("src/main.tsx")
        assert "createRoot" in content

    def test_uses_strict_mode(self) -> None:
        """src/main.tsx must wrap the app in StrictMode."""
        content = _read("src/main.tsx")
        assert "StrictMode" in content

    def test_targets_root_element(self) -> None:
        """src/main.tsx must target the 'root' DOM element."""
        content = _read("src/main.tsx")
        assert "getElementById('root')" in content or 'getElementById("root")' in content


# ---------------------------------------------------------------------------
# src/App.tsx tests
# ---------------------------------------------------------------------------


class TestAppTsx:
    """Tests for src/App.tsx existence and content."""

    def test_exists(self) -> None:
        """src/App.tsx must exist."""
        assert (ROOT / "src" / "App.tsx").is_file()

    def test_has_hello_world(self) -> None:
        """src/App.tsx must render the text 'Hello World'."""
        content = _read("src/App.tsx")
        assert "Hello World" in content

    def test_defines_app_function(self) -> None:
        """src/App.tsx must define an App function."""
        content = _read("src/App.tsx")
        assert "function App" in content

    def test_exports_default(self) -> None:
        """src/App.tsx must have a default export."""
        content = _read("src/App.tsx")
        assert "export default App" in content

    def test_returns_h1(self) -> None:
        """src/App.tsx must return an h1 element."""
        content = _read("src/App.tsx")
        assert "<h1>" in content


# ---------------------------------------------------------------------------
# RUNNING.md tests
# ---------------------------------------------------------------------------


class TestRunningMd:
    """Tests for RUNNING.md existence and content."""

    def test_exists(self) -> None:
        """RUNNING.md must exist at the repository root."""
        assert (ROOT / "RUNNING.md").is_file()

    def test_has_team_brief(self) -> None:
        """RUNNING.md must contain a TEAM_BRIEF section."""
        content = _read("RUNNING.md")
        assert "## TEAM_BRIEF" in content

    def test_team_brief_stack(self) -> None:
        """TEAM_BRIEF must declare the stack."""
        content = _read("RUNNING.md")
        assert "stack:" in content

    def test_team_brief_test_runner(self) -> None:
        """TEAM_BRIEF must declare the test runner."""
        content = _read("RUNNING.md")
        assert "test_runner:" in content
        assert "pytest" in content

    def test_mentions_npm_install(self) -> None:
        """RUNNING.md must mention npm install for setup."""
        content = _read("RUNNING.md")
        assert "npm install" in content

    def test_mentions_npm_run_dev(self) -> None:
        """RUNNING.md must mention npm run dev for development."""
        content = _read("RUNNING.md")
        assert "npm run dev" in content

    def test_mentions_localhost_5173(self) -> None:
        """RUNNING.md must mention the default Vite port."""
        content = _read("RUNNING.md")
        assert "localhost:5173" in content

    def test_mentions_npm_run_build(self) -> None:
        """RUNNING.md must mention npm run build."""
        content = _read("RUNNING.md")
        assert "npm run build" in content

    def test_mentions_pytest(self) -> None:
        """RUNNING.md must mention pytest for running tests."""
        content = _read("RUNNING.md")
        assert "pytest tests/" in content

    def test_mentions_node_prerequisite(self) -> None:
        """RUNNING.md must mention Node.js >= 18 as a prerequisite."""
        content = _read("RUNNING.md")
        assert "Node.js" in content
        assert "18" in content

    def test_has_project_title(self) -> None:
        """RUNNING.md must contain the project title."""
        content = _read("RUNNING.md")
        assert "Hello World React App" in content
