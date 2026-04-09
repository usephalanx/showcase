"""Structural tests for the Vite + React + TypeScript project scaffold.

Validates that all required configuration files exist at the expected
paths and contain the mandatory content markers.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

import pytest

ROOT: Path = Path(__file__).resolve().parent.parent


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _read_text(relative_path: str) -> str:
    """Read a file relative to the repository root and return its text content."""
    path = ROOT / relative_path
    assert path.exists(), f"{relative_path} does not exist"
    return path.read_text(encoding="utf-8")


def _load_package_json() -> Dict[str, Any]:
    """Parse and return the top-level package.json as a dictionary."""
    content = _read_text("package.json")
    return json.loads(content)


# ---------------------------------------------------------------------------
# package.json tests
# ---------------------------------------------------------------------------


class TestPackageJson:
    """Tests for package.json structure and content."""

    def test_package_json_exists(self) -> None:
        """package.json must exist at repository root."""
        assert (ROOT / "package.json").exists()

    def test_package_json_valid_json(self) -> None:
        """package.json must be valid JSON."""
        pkg = _load_package_json()
        assert isinstance(pkg, dict)

    def test_has_name(self) -> None:
        """package.json must have a name field."""
        pkg = _load_package_json()
        assert "name" in pkg
        assert isinstance(pkg["name"], str)
        assert len(pkg["name"]) > 0

    def test_type_module(self) -> None:
        """package.json must set type to module for ESM."""
        pkg = _load_package_json()
        assert pkg.get("type") == "module"

    def test_has_react_dependency(self) -> None:
        """react must be listed in dependencies."""
        pkg = _load_package_json()
        deps = pkg.get("dependencies", {})
        assert "react" in deps

    def test_has_react_dom_dependency(self) -> None:
        """react-dom must be listed in dependencies."""
        pkg = _load_package_json()
        deps = pkg.get("dependencies", {})
        assert "react-dom" in deps

    def test_has_vite_dev_dependency(self) -> None:
        """vite must be listed in devDependencies."""
        pkg = _load_package_json()
        dev_deps = pkg.get("devDependencies", {})
        assert "vite" in dev_deps

    def test_has_vitejs_plugin_react_dev_dependency(self) -> None:
        """@vitejs/plugin-react must be listed in devDependencies."""
        pkg = _load_package_json()
        dev_deps = pkg.get("devDependencies", {})
        assert "@vitejs/plugin-react" in dev_deps

    def test_has_typescript_dev_dependency(self) -> None:
        """typescript must be listed in devDependencies."""
        pkg = _load_package_json()
        dev_deps = pkg.get("devDependencies", {})
        assert "typescript" in dev_deps

    def test_has_types_react_dev_dependency(self) -> None:
        """@types/react must be listed in devDependencies."""
        pkg = _load_package_json()
        dev_deps = pkg.get("devDependencies", {})
        assert "@types/react" in dev_deps

    def test_has_types_react_dom_dev_dependency(self) -> None:
        """@types/react-dom must be listed in devDependencies."""
        pkg = _load_package_json()
        dev_deps = pkg.get("devDependencies", {})
        assert "@types/react-dom" in dev_deps

    def test_dev_script(self) -> None:
        """scripts.dev must be 'vite'."""
        pkg = _load_package_json()
        scripts = pkg.get("scripts", {})
        assert scripts.get("dev") == "vite"

    def test_build_script(self) -> None:
        """scripts.build must include tsc and vite build."""
        pkg = _load_package_json()
        scripts = pkg.get("scripts", {})
        build_cmd = scripts.get("build", "")
        assert "tsc" in build_cmd
        assert "vite build" in build_cmd

    def test_preview_script(self) -> None:
        """scripts.preview must be 'vite preview'."""
        pkg = _load_package_json()
        scripts = pkg.get("scripts", {})
        assert scripts.get("preview") == "vite preview"


# ---------------------------------------------------------------------------
# vite.config.ts tests
# ---------------------------------------------------------------------------


class TestViteConfig:
    """Tests for vite.config.ts existence and content."""

    def test_vite_config_exists(self) -> None:
        """vite.config.ts must exist at repository root."""
        assert (ROOT / "vite.config.ts").exists()

    def test_imports_react_plugin(self) -> None:
        """vite.config.ts must import from @vitejs/plugin-react."""
        content = _read_text("vite.config.ts")
        assert "@vitejs/plugin-react" in content

    def test_imports_define_config(self) -> None:
        """vite.config.ts must import defineConfig from vite."""
        content = _read_text("vite.config.ts")
        assert "defineConfig" in content

    def test_uses_react_plugin(self) -> None:
        """vite.config.ts must call react() in the plugins array."""
        content = _read_text("vite.config.ts")
        assert "plugins" in content
        assert "react()" in content


# ---------------------------------------------------------------------------
# tsconfig.json tests
# ---------------------------------------------------------------------------


class TestTsConfig:
    """Tests for tsconfig.json existence and content."""

    def test_tsconfig_exists(self) -> None:
        """tsconfig.json must exist at repository root."""
        assert (ROOT / "tsconfig.json").exists()

    def test_tsconfig_valid_json(self) -> None:
        """tsconfig.json must be valid JSON."""
        content = _read_text("tsconfig.json")
        data = json.loads(content)
        assert isinstance(data, dict)

    def test_jsx_react_jsx(self) -> None:
        """compilerOptions.jsx must be 'react-jsx'."""
        content = _read_text("tsconfig.json")
        data = json.loads(content)
        compiler = data.get("compilerOptions", {})
        assert compiler.get("jsx") == "react-jsx"

    def test_strict_mode(self) -> None:
        """compilerOptions.strict must be true."""
        content = _read_text("tsconfig.json")
        data = json.loads(content)
        compiler = data.get("compilerOptions", {})
        assert compiler.get("strict") is True

    def test_target_esnext_or_es2020(self) -> None:
        """compilerOptions.target must be ESNext or ES2020."""
        content = _read_text("tsconfig.json")
        data = json.loads(content)
        compiler = data.get("compilerOptions", {})
        target = compiler.get("target", "").upper()
        assert target in ("ESNEXT", "ES2020")

    def test_module_esnext(self) -> None:
        """compilerOptions.module must be ESNext."""
        content = _read_text("tsconfig.json")
        data = json.loads(content)
        compiler = data.get("compilerOptions", {})
        assert compiler.get("module", "").upper() == "ESNEXT"

    def test_include_src(self) -> None:
        """tsconfig.json must include the 'src' directory."""
        content = _read_text("tsconfig.json")
        data = json.loads(content)
        include = data.get("include", [])
        assert "src" in include


# ---------------------------------------------------------------------------
# index.html tests
# ---------------------------------------------------------------------------


class TestIndexHtml:
    """Tests for index.html existence and content."""

    def test_index_html_exists(self) -> None:
        """index.html must exist at repository root."""
        assert (ROOT / "index.html").exists()

    def test_has_doctype(self) -> None:
        """index.html must start with a DOCTYPE declaration."""
        content = _read_text("index.html")
        assert content.strip().lower().startswith("<!doctype html>")

    def test_has_root_div(self) -> None:
        """index.html must contain a div with id='root'."""
        content = _read_text("index.html")
        assert 'id="root"' in content

    def test_has_module_script(self) -> None:
        """index.html must include a script tag with type='module'."""
        content = _read_text("index.html")
        assert 'type="module"' in content

    def test_script_points_to_main_tsx(self) -> None:
        """index.html script tag must reference /src/main.tsx."""
        content = _read_text("index.html")
        assert '/src/main.tsx' in content

    def test_has_charset_meta(self) -> None:
        """index.html must declare charset UTF-8."""
        content = _read_text("index.html")
        assert 'charset="UTF-8"' in content or 'charset="utf-8"' in content

    def test_has_viewport_meta(self) -> None:
        """index.html must include a viewport meta tag."""
        content = _read_text("index.html")
        assert "viewport" in content

    def test_has_title(self) -> None:
        """index.html must have a <title> tag."""
        content = _read_text("index.html")
        assert "<title>" in content.lower()


# ---------------------------------------------------------------------------
# Source entry-point tests
# ---------------------------------------------------------------------------


class TestSourceFiles:
    """Tests for the React source entry files."""

    def test_main_tsx_exists(self) -> None:
        """src/main.tsx must exist."""
        assert (ROOT / "src" / "main.tsx").exists()

    def test_main_tsx_imports_react_dom(self) -> None:
        """src/main.tsx must import from react-dom/client."""
        content = _read_text("src/main.tsx")
        assert "react-dom/client" in content

    def test_main_tsx_creates_root(self) -> None:
        """src/main.tsx must call createRoot."""
        content = _read_text("src/main.tsx")
        assert "createRoot" in content

    def test_main_tsx_references_root_element(self) -> None:
        """src/main.tsx must reference the 'root' DOM element."""
        content = _read_text("src/main.tsx")
        assert "root" in content

    def test_app_tsx_exists(self) -> None:
        """src/App.tsx must exist."""
        assert (ROOT / "src" / "App.tsx").exists()

    def test_app_tsx_exports_default(self) -> None:
        """src/App.tsx must have a default export."""
        content = _read_text("src/App.tsx")
        assert "export default" in content

    def test_app_tsx_contains_hello_world(self) -> None:
        """src/App.tsx must render 'Hello World'."""
        content = _read_text("src/App.tsx")
        assert "Hello World" in content
