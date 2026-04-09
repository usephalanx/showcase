"""Structural tests for the Hello World React project.

Verifies that all required files exist with the expected content,
dependencies are correctly declared, and the project follows the
specified architecture.
"""

import json
import os
from pathlib import Path
from typing import Any, Dict

import pytest

# Root of the repository (parent of the tests/ directory).
ROOT: Path = Path(__file__).resolve().parent.parent


def _load_json(relative_path: str) -> Dict[str, Any]:
    """Load and parse a JSON file relative to the project root.

    Args:
        relative_path: Path to the JSON file relative to ROOT.

    Returns:
        Parsed JSON content as a dictionary.
    """
    filepath = ROOT / relative_path
    with open(filepath, encoding="utf-8") as fh:
        return json.load(fh)


def _read_text(relative_path: str) -> str:
    """Read a text file relative to the project root.

    Args:
        relative_path: Path to the file relative to ROOT.

    Returns:
        The file contents as a string.
    """
    filepath = ROOT / relative_path
    return filepath.read_text(encoding="utf-8")


# ------------------------------------------------------------------
# File existence
# ------------------------------------------------------------------


class TestRequiredFilesExist:
    """Ensure every required project file is present."""

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
        """Verify that the file at *filepath* exists in the project root."""
        full = ROOT / filepath
        assert full.exists(), f"Required file missing: {filepath}"
        assert full.is_file(), f"Expected a file but got a directory: {filepath}"


# ------------------------------------------------------------------
# package.json
# ------------------------------------------------------------------


class TestPackageJson:
    """Validate package.json dependencies and metadata."""

    @pytest.fixture(autouse=True)
    def _load_package(self) -> None:
        """Load package.json once for every test in this class."""
        self.pkg: Dict[str, Any] = _load_json("package.json")

    def test_package_json_has_react_18(self) -> None:
        """React must be listed as a dependency with a version containing '18'."""
        deps = self.pkg.get("dependencies", {})
        assert "react" in deps, "'react' missing from dependencies"
        assert "18" in deps["react"], f"Expected react 18.x, got {deps['react']}"

    def test_package_json_has_react_dom_18(self) -> None:
        """react-dom must be listed as a dependency with a version containing '18'."""
        deps = self.pkg.get("dependencies", {})
        assert "react-dom" in deps, "'react-dom' missing from dependencies"
        assert "18" in deps["react-dom"], (
            f"Expected react-dom 18.x, got {deps['react-dom']}"
        )

    def test_package_json_has_vite_5(self) -> None:
        """Vite must be listed as a dev dependency with a version containing '5'."""
        dev_deps = self.pkg.get("devDependencies", {})
        assert "vite" in dev_deps, "'vite' missing from devDependencies"
        assert "5" in dev_deps["vite"], (
            f"Expected vite 5.x, got {dev_deps['vite']}"
        )

    def test_package_json_has_typescript(self) -> None:
        """TypeScript must be listed as a dev dependency."""
        dev_deps = self.pkg.get("devDependencies", {})
        assert "typescript" in dev_deps, "'typescript' missing from devDependencies"

    def test_package_json_has_vitejs_plugin_react(self) -> None:
        """@vitejs/plugin-react must be listed as a dev dependency."""
        dev_deps = self.pkg.get("devDependencies", {})
        assert "@vitejs/plugin-react" in dev_deps, (
            "'@vitejs/plugin-react' missing from devDependencies"
        )

    def test_package_json_has_types_react(self) -> None:
        """@types/react must be listed as a dev dependency."""
        dev_deps = self.pkg.get("devDependencies", {})
        assert "@types/react" in dev_deps, (
            "'@types/react' missing from devDependencies"
        )

    def test_package_json_has_types_react_dom(self) -> None:
        """@types/react-dom must be listed as a dev dependency."""
        dev_deps = self.pkg.get("devDependencies", {})
        assert "@types/react-dom" in dev_deps, (
            "'@types/react-dom' missing from devDependencies"
        )

    def test_package_json_scripts_dev(self) -> None:
        """The 'dev' script must invoke vite."""
        scripts = self.pkg.get("scripts", {})
        assert "dev" in scripts, "'dev' script missing"
        assert "vite" in scripts["dev"]

    def test_package_json_scripts_build(self) -> None:
        """The 'build' script must invoke tsc and vite build."""
        scripts = self.pkg.get("scripts", {})
        assert "build" in scripts, "'build' script missing"
        assert "tsc" in scripts["build"]
        assert "vite build" in scripts["build"]

    def test_package_json_private(self) -> None:
        """package.json must be marked as private."""
        assert self.pkg.get("private") is True

    def test_no_forbidden_dependencies(self) -> None:
        """Ensure no router, state management, or UI framework is declared."""
        all_deps = {}
        all_deps.update(self.pkg.get("dependencies", {}))
        all_deps.update(self.pkg.get("devDependencies", {}))

        forbidden = [
            "react-router",
            "react-router-dom",
            "redux",
            "@reduxjs/toolkit",
            "mobx",
            "zustand",
            "@mui/material",
            "@chakra-ui/react",
            "antd",
            "tailwindcss",
        ]
        for dep in forbidden:
            assert dep not in all_deps, (
                f"Forbidden dependency '{dep}' found in package.json"
            )


# ------------------------------------------------------------------
# index.html
# ------------------------------------------------------------------


class TestIndexHtml:
    """Validate the Vite entry HTML file."""

    @pytest.fixture(autouse=True)
    def _load_html(self) -> None:
        """Read index.html once for every test in this class."""
        self.html: str = _read_text("index.html")

    def test_has_doctype(self) -> None:
        """index.html must start with a DOCTYPE declaration."""
        assert self.html.strip().startswith("<!DOCTYPE html>")

    def test_has_lang_en(self) -> None:
        """The <html> tag must specify lang='en'."""
        assert 'lang="en"' in self.html

    def test_has_charset_utf8(self) -> None:
        """A meta charset=UTF-8 tag must be present."""
        assert 'charset="UTF-8"' in self.html

    def test_has_viewport_meta(self) -> None:
        """A viewport meta tag must be present."""
        assert "viewport" in self.html

    def test_has_title(self) -> None:
        """The page title must be 'Hello World React'."""
        assert "<title>Hello World React</title>" in self.html

    def test_has_root_div(self) -> None:
        """A <div id='root'></div> element must be present."""
        assert '<div id="root"></div>' in self.html

    def test_has_module_script(self) -> None:
        """A script tag with type='module' pointing to /src/main.tsx must exist."""
        assert 'type="module"' in self.html
        assert 'src="/src/main.tsx"' in self.html


# ------------------------------------------------------------------
# src/main.tsx
# ------------------------------------------------------------------


class TestMainTsx:
    """Validate the React entry point."""

    @pytest.fixture(autouse=True)
    def _load_main(self) -> None:
        """Read src/main.tsx once for every test in this class."""
        self.main: str = _read_text("src/main.tsx")

    def test_imports_react(self) -> None:
        """main.tsx must import React."""
        assert "import React" in self.main

    def test_imports_react_dom_client(self) -> None:
        """main.tsx must import from 'react-dom/client'."""
        assert "react-dom/client" in self.main

    def test_imports_app(self) -> None:
        """main.tsx must import App from './App'."""
        assert "import App from './App'" in self.main

    def test_uses_createroot(self) -> None:
        """main.tsx must call ReactDOM.createRoot."""
        assert "createRoot" in self.main

    def test_targets_root_element(self) -> None:
        """main.tsx must target the element with id 'root'."""
        assert "getElementById('root')" in self.main or 'getElementById("root")' in self.main

    def test_uses_strict_mode(self) -> None:
        """main.tsx must wrap App in React.StrictMode."""
        assert "StrictMode" in self.main

    def test_renders_app(self) -> None:
        """main.tsx must render <App />."""
        assert "<App />" in self.main


# ------------------------------------------------------------------
# src/App.tsx
# ------------------------------------------------------------------


class TestAppTsx:
    """Validate the root App component."""

    @pytest.fixture(autouse=True)
    def _load_app(self) -> None:
        """Read src/App.tsx once for every test in this class."""
        self.app: str = _read_text("src/App.tsx")

    def test_defines_app_function(self) -> None:
        """App.tsx must define a function named App."""
        assert "function App" in self.app or "const App" in self.app

    def test_exports_default(self) -> None:
        """App.tsx must have a default export."""
        assert "export default" in self.app

    def test_renders_hello_world(self) -> None:
        """App.tsx must render the text 'Hello World'."""
        assert "Hello World" in self.app

    def test_uses_h1_element(self) -> None:
        """App.tsx must use an <h1> element."""
        assert "<h1>" in self.app


# ------------------------------------------------------------------
# tsconfig.json
# ------------------------------------------------------------------


class TestTsConfig:
    """Validate the TypeScript configuration."""

    @pytest.fixture(autouse=True)
    def _load_tsconfig(self) -> None:
        """Load tsconfig.json once for every test in this class."""
        self.tsconfig: Dict[str, Any] = _load_json("tsconfig.json")

    def test_strict_enabled(self) -> None:
        """strict mode must be enabled."""
        opts = self.tsconfig.get("compilerOptions", {})
        assert opts.get("strict") is True

    def test_jsx_react_jsx(self) -> None:
        """jsx must be set to 'react-jsx'."""
        opts = self.tsconfig.get("compilerOptions", {})
        assert opts.get("jsx") == "react-jsx"

    def test_includes_src(self) -> None:
        """The include array must contain 'src'."""
        includes = self.tsconfig.get("include", [])
        assert "src" in includes

    def test_target_es2020(self) -> None:
        """Target must be ES2020."""
        opts = self.tsconfig.get("compilerOptions", {})
        assert opts.get("target") == "ES2020"

    def test_module_esnext(self) -> None:
        """Module must be ESNext."""
        opts = self.tsconfig.get("compilerOptions", {})
        assert opts.get("module") == "ESNext"

    def test_module_resolution_bundler(self) -> None:
        """moduleResolution must be 'bundler'."""
        opts = self.tsconfig.get("compilerOptions", {})
        assert opts.get("moduleResolution") == "bundler"


# ------------------------------------------------------------------
# vite.config.ts
# ------------------------------------------------------------------


class TestViteConfig:
    """Validate the Vite configuration file."""

    @pytest.fixture(autouse=True)
    def _load_vite(self) -> None:
        """Read vite.config.ts once for every test in this class."""
        self.vite: str = _read_text("vite.config.ts")

    def test_imports_define_config(self) -> None:
        """vite.config.ts must import defineConfig from 'vite'."""
        assert "defineConfig" in self.vite
        assert "from 'vite'" in self.vite

    def test_imports_react_plugin(self) -> None:
        """vite.config.ts must import the React plugin."""
        assert "@vitejs/plugin-react" in self.vite

    def test_uses_react_plugin(self) -> None:
        """vite.config.ts must call react() in the plugins array."""
        assert "react()" in self.vite

    def test_sets_port_3000(self) -> None:
        """vite.config.ts must configure the dev server on port 3000."""
        assert "3000" in self.vite


# ------------------------------------------------------------------
# RUNNING.md
# ------------------------------------------------------------------


class TestRunningMd:
    """Validate that RUNNING.md exists and has useful content."""

    @pytest.fixture(autouse=True)
    def _load_running(self) -> None:
        """Read RUNNING.md once for every test in this class."""
        self.running: str = _read_text("RUNNING.md")

    def test_mentions_npm_install(self) -> None:
        """RUNNING.md must mention npm install."""
        assert "npm install" in self.running

    def test_mentions_npm_run_dev(self) -> None:
        """RUNNING.md must mention npm run dev."""
        assert "npm run dev" in self.running

    def test_mentions_npm_run_build(self) -> None:
        """RUNNING.md must mention npm run build."""
        assert "npm run build" in self.running
