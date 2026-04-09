"""Tests that verify the project scaffold structure and content.

These tests validate that all required files exist, that package.json
contains the correct dependencies and scripts, that tsconfig.json is
properly configured, and that source files contain expected content.
"""

import json
import os
from pathlib import Path
from typing import Any, Dict

import pytest

# Repository root is the parent of the tests/ directory.
ROOT: Path = Path(__file__).resolve().parent.parent


def _load_json(filename: str) -> Dict[str, Any]:
    """Load and parse a JSON file from the repository root.

    Args:
        filename: Name of the JSON file relative to the repo root.

    Returns:
        Parsed JSON content as a dictionary.
    """
    filepath = ROOT / filename
    with open(filepath, encoding="utf-8") as fh:
        return json.load(fh)


def _read_text(filepath: str) -> str:
    """Read the full text content of a file relative to the repo root.

    Args:
        filepath: Relative path from the repo root.

    Returns:
        The file content as a string.
    """
    return (ROOT / filepath).read_text(encoding="utf-8")


# ------------------------------------------------------------------
# File existence
# ------------------------------------------------------------------


class TestRequiredFilesExist:
    """Ensure every required file is present in the repository."""

    @pytest.mark.parametrize(
        "filepath",
        [
            "package.json",
            "vite.config.ts",
            "tsconfig.json",
            "index.html",
            "src/main.tsx",
            "src/App.tsx",
            "RUNNING.md",
        ],
    )
    def test_required_files_exist(self, filepath: str) -> None:
        """Assert that {filepath} exists in the project root."""
        full_path = ROOT / filepath
        assert full_path.exists(), f"Required file missing: {filepath}"
        assert full_path.is_file(), f"Expected a file but got directory: {filepath}"


# ------------------------------------------------------------------
# package.json — dependencies
# ------------------------------------------------------------------


class TestPackageJsonDependencies:
    """Validate the dependencies declared in package.json."""

    @pytest.fixture()
    def pkg(self) -> Dict[str, Any]:
        """Return parsed package.json content."""
        return _load_json("package.json")

    def test_package_json_has_react_18(self, pkg: Dict[str, Any]) -> None:
        """React 18.x must be listed as a dependency."""
        deps = pkg.get("dependencies", {})
        assert "react" in deps, "'react' missing from dependencies"
        assert "18" in deps["react"], f"Expected React 18, got {deps['react']}"

    def test_package_json_has_react_dom_18(self, pkg: Dict[str, Any]) -> None:
        """React-dom 18.x must be listed as a dependency."""
        deps = pkg.get("dependencies", {})
        assert "react-dom" in deps, "'react-dom' missing from dependencies"
        assert "18" in deps["react-dom"], f"Expected react-dom 18, got {deps['react-dom']}"

    def test_package_json_has_vite_5(self, pkg: Dict[str, Any]) -> None:
        """Vite 5.x must be listed as a devDependency."""
        dev_deps = pkg.get("devDependencies", {})
        assert "vite" in dev_deps, "'vite' missing from devDependencies"
        assert "5" in dev_deps["vite"], f"Expected Vite 5, got {dev_deps['vite']}"

    def test_package_json_has_typescript(self, pkg: Dict[str, Any]) -> None:
        """TypeScript must be listed as a devDependency."""
        dev_deps = pkg.get("devDependencies", {})
        assert "typescript" in dev_deps, "'typescript' missing from devDependencies"

    def test_package_json_has_vitejs_plugin_react(self, pkg: Dict[str, Any]) -> None:
        """@vitejs/plugin-react must be listed as a devDependency."""
        dev_deps = pkg.get("devDependencies", {})
        assert "@vitejs/plugin-react" in dev_deps, (
            "'@vitejs/plugin-react' missing from devDependencies"
        )

    def test_package_json_has_types_react(self, pkg: Dict[str, Any]) -> None:
        """@types/react must be listed as a devDependency."""
        dev_deps = pkg.get("devDependencies", {})
        assert "@types/react" in dev_deps, "'@types/react' missing from devDependencies"

    def test_package_json_has_types_react_dom(self, pkg: Dict[str, Any]) -> None:
        """@types/react-dom must be listed as a devDependency."""
        dev_deps = pkg.get("devDependencies", {})
        assert "@types/react-dom" in dev_deps, (
            "'@types/react-dom' missing from devDependencies"
        )


# ------------------------------------------------------------------
# package.json — scripts
# ------------------------------------------------------------------


class TestPackageJsonScripts:
    """Validate the npm scripts declared in package.json."""

    @pytest.fixture()
    def scripts(self) -> Dict[str, str]:
        """Return the scripts section of package.json."""
        pkg = _load_json("package.json")
        return pkg.get("scripts", {})

    def test_dev_script(self, scripts: Dict[str, str]) -> None:
        """The 'dev' script must run vite."""
        assert "dev" in scripts, "'dev' script missing"
        assert scripts["dev"] == "vite", f"Expected 'vite', got '{scripts['dev']}'"

    def test_build_script(self, scripts: Dict[str, str]) -> None:
        """The 'build' script must run tsc && vite build."""
        assert "build" in scripts, "'build' script missing"
        assert scripts["build"] == "tsc && vite build", (
            f"Expected 'tsc && vite build', got '{scripts['build']}'"
        )

    def test_preview_script(self, scripts: Dict[str, str]) -> None:
        """The 'preview' script must run vite preview."""
        assert "preview" in scripts, "'preview' script missing"
        assert scripts["preview"] == "vite preview", (
            f"Expected 'vite preview', got '{scripts['preview']}'"
        )


# ------------------------------------------------------------------
# package.json — metadata
# ------------------------------------------------------------------


class TestPackageJsonMetadata:
    """Validate top-level metadata in package.json."""

    @pytest.fixture()
    def pkg(self) -> Dict[str, Any]:
        """Return parsed package.json content."""
        return _load_json("package.json")

    def test_name(self, pkg: Dict[str, Any]) -> None:
        """Package name must be 'hello-world-react'."""
        assert pkg.get("name") == "hello-world-react"

    def test_private(self, pkg: Dict[str, Any]) -> None:
        """Package must be private."""
        assert pkg.get("private") is True

    def test_version(self, pkg: Dict[str, Any]) -> None:
        """Package must have a version string."""
        assert "version" in pkg
        assert isinstance(pkg["version"], str)


# ------------------------------------------------------------------
# package.json — no forbidden dependencies
# ------------------------------------------------------------------


class TestNoForbiddenDependencies:
    """Ensure no unnecessary dependencies are declared."""

    FORBIDDEN = [
        "react-router",
        "react-router-dom",
        "redux",
        "@reduxjs/toolkit",
        "zustand",
        "mobx",
        "@mui/material",
        "@chakra-ui/react",
        "tailwindcss",
        "styled-components",
        "axios",
        "next",
    ]

    @pytest.fixture()
    def all_deps(self) -> Dict[str, str]:
        """Return the union of dependencies and devDependencies."""
        pkg = _load_json("package.json")
        deps: Dict[str, str] = {}
        deps.update(pkg.get("dependencies", {}))
        deps.update(pkg.get("devDependencies", {}))
        return deps

    @pytest.mark.parametrize("dep", FORBIDDEN)
    def test_forbidden_dep_absent(self, all_deps: Dict[str, str], dep: str) -> None:
        """Assert that {dep} is NOT present in the project."""
        assert dep not in all_deps, f"Unexpected dependency found: {dep}"


# ------------------------------------------------------------------
# tsconfig.json
# ------------------------------------------------------------------


class TestTsconfigJson:
    """Validate tsconfig.json compiler options."""

    @pytest.fixture()
    def tsconfig(self) -> Dict[str, Any]:
        """Return parsed tsconfig.json content."""
        return _load_json("tsconfig.json")

    def test_strict_mode_enabled(self, tsconfig: Dict[str, Any]) -> None:
        """TypeScript strict mode must be enabled."""
        opts = tsconfig.get("compilerOptions", {})
        assert opts.get("strict") is True, "strict mode is not enabled"

    def test_jsx_react_jsx(self, tsconfig: Dict[str, Any]) -> None:
        """JSX setting must be 'react-jsx'."""
        opts = tsconfig.get("compilerOptions", {})
        assert opts.get("jsx") == "react-jsx", (
            f"Expected jsx 'react-jsx', got '{opts.get('jsx')}'"
        )

    def test_target_es2020(self, tsconfig: Dict[str, Any]) -> None:
        """Target must be ES2020."""
        opts = tsconfig.get("compilerOptions", {})
        assert opts.get("target") == "ES2020"

    def test_module_esnext(self, tsconfig: Dict[str, Any]) -> None:
        """Module must be ESNext."""
        opts = tsconfig.get("compilerOptions", {})
        assert opts.get("module") == "ESNext"

    def test_module_resolution_bundler(self, tsconfig: Dict[str, Any]) -> None:
        """Module resolution must be 'bundler'."""
        opts = tsconfig.get("compilerOptions", {})
        assert opts.get("moduleResolution") == "bundler"

    def test_include_src(self, tsconfig: Dict[str, Any]) -> None:
        """The include array must contain 'src'."""
        include = tsconfig.get("include", [])
        assert "src" in include, f"Expected 'src' in include, got {include}"

    def test_lib_contains_dom(self, tsconfig: Dict[str, Any]) -> None:
        """The lib array must contain 'DOM'."""
        opts = tsconfig.get("compilerOptions", {})
        lib = opts.get("lib", [])
        assert "DOM" in lib, f"Expected 'DOM' in lib, got {lib}"

    def test_lib_contains_es2020(self, tsconfig: Dict[str, Any]) -> None:
        """The lib array must contain 'ES2020'."""
        opts = tsconfig.get("compilerOptions", {})
        lib = opts.get("lib", [])
        assert "ES2020" in lib, f"Expected 'ES2020' in lib, got {lib}"


# ------------------------------------------------------------------
# vite.config.ts
# ------------------------------------------------------------------


class TestViteConfig:
    """Validate vite.config.ts content."""

    @pytest.fixture()
    def content(self) -> str:
        """Return the raw content of vite.config.ts."""
        return _read_text("vite.config.ts")

    def test_imports_define_config(self, content: str) -> None:
        """Must import defineConfig from 'vite'."""
        assert "defineConfig" in content
        assert "from 'vite'" in content or 'from "vite"' in content

    def test_imports_react_plugin(self, content: str) -> None:
        """Must import the React plugin from @vitejs/plugin-react."""
        assert "@vitejs/plugin-react" in content

    def test_uses_react_plugin(self, content: str) -> None:
        """Must call react() in plugins array."""
        assert "react()" in content

    def test_exports_default_config(self, content: str) -> None:
        """Must export default a defineConfig call."""
        assert "export default defineConfig" in content

    def test_server_port_3000(self, content: str) -> None:
        """Development server port must be set to 3000."""
        assert "3000" in content


# ------------------------------------------------------------------
# index.html
# ------------------------------------------------------------------


class TestIndexHtml:
    """Validate the Vite entry HTML file."""

    @pytest.fixture()
    def content(self) -> str:
        """Return the raw content of index.html."""
        return _read_text("index.html")

    def test_has_doctype(self, content: str) -> None:
        """Must start with an HTML5 doctype."""
        assert "<!DOCTYPE html>" in content or "<!doctype html>" in content.lower()

    def test_lang_attribute(self, content: str) -> None:
        """Must include lang='en' attribute."""
        assert 'lang="en"' in content or "lang='en'" in content

    def test_has_root_div(self, content: str) -> None:
        """Must contain a div with id='root'."""
        assert 'id="root"' in content or "id='root'" in content

    def test_script_module_src(self, content: str) -> None:
        """Must include a module script pointing to /src/main.tsx."""
        assert 'type="module"' in content or "type='module'" in content
        assert "/src/main.tsx" in content

    def test_meta_charset(self, content: str) -> None:
        """Must include meta charset UTF-8."""
        assert "UTF-8" in content or "utf-8" in content

    def test_viewport_meta(self, content: str) -> None:
        """Must include a viewport meta tag."""
        assert "viewport" in content

    def test_title(self, content: str) -> None:
        """Title must be 'Hello World React'."""
        assert "<title>Hello World React</title>" in content


# ------------------------------------------------------------------
# src/main.tsx
# ------------------------------------------------------------------


class TestMainTsx:
    """Validate the React application entry point."""

    @pytest.fixture()
    def content(self) -> str:
        """Return the raw content of src/main.tsx."""
        return _read_text("src/main.tsx")

    def test_imports_react(self, content: str) -> None:
        """Must import React."""
        assert "import React" in content

    def test_imports_react_dom_client(self, content: str) -> None:
        """Must import from react-dom/client."""
        assert "react-dom/client" in content

    def test_imports_app(self, content: str) -> None:
        """Must import the App component."""
        assert "import App" in content

    def test_creates_root(self, content: str) -> None:
        """Must call createRoot."""
        assert "createRoot" in content

    def test_uses_strict_mode(self, content: str) -> None:
        """Must use React.StrictMode."""
        assert "StrictMode" in content

    def test_targets_root_element(self, content: str) -> None:
        """Must target the #root element."""
        assert "getElementById('root')" in content or 'getElementById("root")' in content


# ------------------------------------------------------------------
# src/App.tsx
# ------------------------------------------------------------------


class TestAppTsx:
    """Validate the root App component."""

    @pytest.fixture()
    def content(self) -> str:
        """Return the raw content of src/App.tsx."""
        return _read_text("src/App.tsx")

    def test_defines_app_function(self, content: str) -> None:
        """Must define a function named App."""
        assert "function App" in content

    def test_exports_default_app(self, content: str) -> None:
        """Must export App as default."""
        assert "export default App" in content or "export default function App" in content

    def test_renders_hello_world(self, content: str) -> None:
        """Must render the text 'Hello World'."""
        assert "Hello World" in content

    def test_uses_h1_tag(self, content: str) -> None:
        """Must use an <h1> element."""
        assert "<h1>" in content


# ------------------------------------------------------------------
# RUNNING.md
# ------------------------------------------------------------------


class TestRunningMd:
    """Validate the RUNNING.md documentation file."""

    @pytest.fixture()
    def content(self) -> str:
        """Return the raw content of RUNNING.md."""
        return _read_text("RUNNING.md")

    def test_contains_npm_install(self, content: str) -> None:
        """Must document the npm install step."""
        assert "npm install" in content

    def test_contains_npm_run_dev(self, content: str) -> None:
        """Must document the dev script."""
        assert "npm run dev" in content

    def test_contains_npm_run_build(self, content: str) -> None:
        """Must document the build script."""
        assert "npm run build" in content

    def test_contains_npm_run_preview(self, content: str) -> None:
        """Must document the preview script."""
        assert "npm run preview" in content

    def test_mentions_port_3000(self, content: str) -> None:
        """Must mention port 3000."""
        assert "3000" in content
