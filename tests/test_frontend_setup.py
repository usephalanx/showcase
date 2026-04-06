"""Tests to validate the frontend project setup.

Verifies that all required frontend files exist, contain the expected
configuration, and that the Task type interface is correctly defined.
"""

import json
import os
import re
from pathlib import Path
from typing import Any, Dict

import pytest

ROOT_DIR: Path = Path(__file__).resolve().parent.parent
FRONTEND_DIR: Path = ROOT_DIR / "frontend"


def _read_text(relative_path: str) -> str:
    """Read and return the text content of a file relative to the frontend directory."""
    file_path = FRONTEND_DIR / relative_path
    assert file_path.exists(), f"Expected file not found: {file_path}"
    return file_path.read_text(encoding="utf-8")


def _load_json(relative_path: str) -> Dict[str, Any]:
    """Load and return parsed JSON from a file relative to the frontend directory."""
    content = _read_text(relative_path)
    return json.loads(content)


class TestPackageJson:
    """Tests for frontend/package.json."""

    def test_package_json_exists(self) -> None:
        """Verify package.json exists in the frontend directory."""
        assert (FRONTEND_DIR / "package.json").exists()

    def test_package_json_is_valid_json(self) -> None:
        """Verify package.json is valid JSON."""
        data = _load_json("package.json")
        assert isinstance(data, dict)

    def test_has_react_dependency(self) -> None:
        """Verify react is listed as a dependency."""
        data = _load_json("package.json")
        assert "react" in data.get("dependencies", {})

    def test_has_react_dom_dependency(self) -> None:
        """Verify react-dom is listed as a dependency."""
        data = _load_json("package.json")
        assert "react-dom" in data.get("dependencies", {})

    def test_has_axios_dependency(self) -> None:
        """Verify axios is listed as a dependency."""
        data = _load_json("package.json")
        assert "axios" in data.get("dependencies", {})

    def test_has_typescript_devdependency(self) -> None:
        """Verify typescript is listed as a dev dependency."""
        data = _load_json("package.json")
        assert "typescript" in data.get("devDependencies", {})

    def test_has_vite_devdependency(self) -> None:
        """Verify vite is listed as a dev dependency."""
        data = _load_json("package.json")
        assert "vite" in data.get("devDependencies", {})

    def test_has_vitejs_plugin_react_devdependency(self) -> None:
        """Verify @vitejs/plugin-react is listed as a dev dependency."""
        data = _load_json("package.json")
        assert "@vitejs/plugin-react" in data.get("devDependencies", {})

    def test_has_dev_script(self) -> None:
        """Verify a 'dev' script is defined."""
        data = _load_json("package.json")
        scripts = data.get("scripts", {})
        assert "dev" in scripts
        assert "vite" in scripts["dev"]

    def test_has_build_script(self) -> None:
        """Verify a 'build' script is defined."""
        data = _load_json("package.json")
        scripts = data.get("scripts", {})
        assert "build" in scripts


class TestViteConfig:
    """Tests for frontend/vite.config.ts."""

    def test_vite_config_exists(self) -> None:
        """Verify vite.config.ts exists."""
        assert (FRONTEND_DIR / "vite.config.ts").exists()

    def test_vite_config_imports_react_plugin(self) -> None:
        """Verify vite config imports the React plugin."""
        content = _read_text("vite.config.ts")
        assert "@vitejs/plugin-react" in content

    def test_vite_config_uses_react_plugin(self) -> None:
        """Verify vite config activates the React plugin."""
        content = _read_text("vite.config.ts")
        assert "react()" in content

    def test_vite_config_has_proxy_to_backend(self) -> None:
        """Verify vite config proxies /api to localhost:8000."""
        content = _read_text("vite.config.ts")
        assert "localhost:8000" in content or "127.0.0.1:8000" in content
        assert "/api" in content

    def test_vite_config_has_proxy_section(self) -> None:
        """Verify vite config contains a proxy configuration block."""
        content = _read_text("vite.config.ts")
        assert "proxy" in content


class TestTsconfig:
    """Tests for frontend/tsconfig.json."""

    def test_tsconfig_exists(self) -> None:
        """Verify tsconfig.json exists."""
        assert (FRONTEND_DIR / "tsconfig.json").exists()

    def test_tsconfig_is_valid_json(self) -> None:
        """Verify tsconfig.json is valid JSON."""
        data = _load_json("tsconfig.json")
        assert isinstance(data, dict)

    def test_tsconfig_has_compiler_options(self) -> None:
        """Verify tsconfig contains compilerOptions."""
        data = _load_json("tsconfig.json")
        assert "compilerOptions" in data

    def test_tsconfig_jsx_react_jsx(self) -> None:
        """Verify tsconfig sets jsx to react-jsx."""
        data = _load_json("tsconfig.json")
        compiler = data.get("compilerOptions", {})
        assert compiler.get("jsx") == "react-jsx"

    def test_tsconfig_strict_mode(self) -> None:
        """Verify tsconfig enables strict mode."""
        data = _load_json("tsconfig.json")
        compiler = data.get("compilerOptions", {})
        assert compiler.get("strict") is True

    def test_tsconfig_includes_src(self) -> None:
        """Verify tsconfig includes the src directory."""
        data = _load_json("tsconfig.json")
        include = data.get("include", [])
        assert "src" in include


class TestIndexHtml:
    """Tests for frontend/index.html."""

    def test_index_html_exists(self) -> None:
        """Verify index.html exists."""
        assert (FRONTEND_DIR / "index.html").exists()

    def test_index_html_has_root_div(self) -> None:
        """Verify index.html has a root div element."""
        content = _read_text("index.html")
        assert 'id="root"' in content

    def test_index_html_references_main_tsx(self) -> None:
        """Verify index.html references src/main.tsx as entry point."""
        content = _read_text("index.html")
        assert "src/main.tsx" in content

    def test_index_html_has_module_script(self) -> None:
        """Verify the script tag uses type=module."""
        content = _read_text("index.html")
        assert 'type="module"' in content

    def test_index_html_has_doctype(self) -> None:
        """Verify index.html starts with DOCTYPE."""
        content = _read_text("index.html")
        assert content.strip().startswith("<!DOCTYPE html>")


class TestMainTsx:
    """Tests for frontend/src/main.tsx."""

    def test_main_tsx_exists(self) -> None:
        """Verify src/main.tsx exists."""
        assert (FRONTEND_DIR / "src" / "main.tsx").exists()

    def test_main_tsx_imports_react(self) -> None:
        """Verify main.tsx imports React."""
        content = _read_text("src/main.tsx")
        assert "import React" in content or "from 'react'" in content

    def test_main_tsx_imports_react_dom(self) -> None:
        """Verify main.tsx imports ReactDOM."""
        content = _read_text("src/main.tsx")
        assert "react-dom" in content

    def test_main_tsx_creates_root(self) -> None:
        """Verify main.tsx calls createRoot."""
        content = _read_text("src/main.tsx")
        assert "createRoot" in content

    def test_main_tsx_uses_strict_mode(self) -> None:
        """Verify main.tsx renders inside React.StrictMode."""
        content = _read_text("src/main.tsx")
        assert "StrictMode" in content


class TestTypesTs:
    """Tests for frontend/src/types.ts."""

    def test_types_ts_exists(self) -> None:
        """Verify src/types.ts exists."""
        assert (FRONTEND_DIR / "src" / "types.ts").exists()

    def test_types_ts_defines_task_interface(self) -> None:
        """Verify types.ts exports a Task interface."""
        content = _read_text("src/types.ts")
        assert "export interface Task" in content

    def test_task_has_id_field(self) -> None:
        """Verify Task interface has an id field."""
        content = _read_text("src/types.ts")
        assert re.search(r"id\s*:\s*number", content)

    def test_task_has_title_field(self) -> None:
        """Verify Task interface has a title field."""
        content = _read_text("src/types.ts")
        assert re.search(r"title\s*:\s*string", content)

    def test_task_has_status_field(self) -> None:
        """Verify Task interface has a status field."""
        content = _read_text("src/types.ts")
        assert "status" in content

    def test_task_status_includes_pending(self) -> None:
        """Verify Task status type includes 'pending'."""
        content = _read_text("src/types.ts")
        assert "pending" in content

    def test_task_status_includes_in_progress(self) -> None:
        """Verify Task status type includes 'in_progress'."""
        content = _read_text("src/types.ts")
        assert "in_progress" in content

    def test_task_status_includes_completed(self) -> None:
        """Verify Task status type includes 'completed'."""
        content = _read_text("src/types.ts")
        assert "completed" in content

    def test_task_has_due_date_field(self) -> None:
        """Verify Task interface has a due_date field."""
        content = _read_text("src/types.ts")
        assert "due_date" in content

    def test_task_due_date_is_nullable(self) -> None:
        """Verify Task due_date field allows null."""
        content = _read_text("src/types.ts")
        assert re.search(r"due_date\s*:.*null", content)
