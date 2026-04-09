"""Structural tests for the Hello World React + Vite project.

These tests validate that every required file exists, contains the
expected content, and that the overall project layout is correct.
No Node.js runtime or npm install is needed.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any

import pytest

# Resolve project root (two levels up from this test file).
PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent


def _read(relative_path: str) -> str:
    """Read a project file and return its content as a string.

    Args:
        relative_path: Path relative to the project root.

    Returns:
        The full text content of the file.
    """
    return (PROJECT_ROOT / relative_path).read_text(encoding="utf-8")


def _load_json(relative_path: str) -> Dict[str, Any]:
    """Read and parse a JSON file from the project.

    Args:
        relative_path: Path relative to the project root.

    Returns:
        Parsed JSON as a dictionary.
    """
    return json.loads(_read(relative_path))


# ------------------------------------------------------------------
# File existence
# ------------------------------------------------------------------


class TestFileExistence:
    """Verify that all required project files exist."""

    REQUIRED_FILES = [
        "package.json",
        "tsconfig.json",
        "vite.config.ts",
        "index.html",
        "src/main.tsx",
        "src/App.tsx",
        "Dockerfile",
        "docker-compose.yml",
        "RUNNING.md",
    ]

    @pytest.mark.parametrize("filepath", REQUIRED_FILES)
    def test_file_exists(self, filepath: str) -> None:
        """Assert that a required project file exists."""
        full_path = PROJECT_ROOT / filepath
        assert full_path.exists(), f"Missing required file: {filepath}"
        assert full_path.is_file(), f"{filepath} should be a regular file"


# ------------------------------------------------------------------
# package.json
# ------------------------------------------------------------------


class TestPackageJson:
    """Validate package.json content and structure."""

    @pytest.fixture(autouse=True)
    def _load(self) -> None:
        """Load package.json once for all methods in this class."""
        self.pkg: Dict[str, Any] = _load_json("package.json")

    def test_name(self) -> None:
        """Project name should be 'hello-world-react'."""
        assert self.pkg.get("name") == "hello-world-react"

    def test_private(self) -> None:
        """Package should be marked private."""
        assert self.pkg.get("private") is True

    def test_type_module(self) -> None:
        """Package type should be 'module' for ESM."""
        assert self.pkg.get("type") == "module"

    def test_scripts_dev(self) -> None:
        """The 'dev' script should invoke vite."""
        scripts = self.pkg.get("scripts", {})
        assert "dev" in scripts
        assert "vite" in scripts["dev"]

    def test_scripts_build(self) -> None:
        """The 'build' script should exist."""
        scripts = self.pkg.get("scripts", {})
        assert "build" in scripts

    def test_scripts_preview(self) -> None:
        """The 'preview' script should exist."""
        scripts = self.pkg.get("scripts", {})
        assert "preview" in scripts

    def test_react_dependency(self) -> None:
        """React should be listed as a dependency."""
        deps = self.pkg.get("dependencies", {})
        assert "react" in deps
        assert "react-dom" in deps

    def test_vite_dev_dependency(self) -> None:
        """Vite should be listed as a dev dependency."""
        dev_deps = self.pkg.get("devDependencies", {})
        assert "vite" in dev_deps

    def test_typescript_dev_dependency(self) -> None:
        """TypeScript should be listed as a dev dependency."""
        dev_deps = self.pkg.get("devDependencies", {})
        assert "typescript" in dev_deps

    def test_vitejs_plugin_react(self) -> None:
        """@vitejs/plugin-react should be listed as a dev dependency."""
        dev_deps = self.pkg.get("devDependencies", {})
        assert "@vitejs/plugin-react" in dev_deps

    def test_react_type_definitions(self) -> None:
        """React type definitions should be present."""
        dev_deps = self.pkg.get("devDependencies", {})
        assert "@types/react" in dev_deps
        assert "@types/react-dom" in dev_deps


# ------------------------------------------------------------------
# tsconfig.json
# ------------------------------------------------------------------


class TestTsconfigJson:
    """Validate tsconfig.json content."""

    @pytest.fixture(autouse=True)
    def _load(self) -> None:
        """Load tsconfig.json once for all methods in this class."""
        self.tsconfig: Dict[str, Any] = _load_json("tsconfig.json")

    def test_strict_mode(self) -> None:
        """Strict mode should be enabled."""
        opts = self.tsconfig.get("compilerOptions", {})
        assert opts.get("strict") is True

    def test_jsx_react_jsx(self) -> None:
        """JSX should be set to 'react-jsx'."""
        opts = self.tsconfig.get("compilerOptions", {})
        assert opts.get("jsx") == "react-jsx"

    def test_target(self) -> None:
        """Target should be ES2020."""
        opts = self.tsconfig.get("compilerOptions", {})
        assert opts.get("target") == "ES2020"

    def test_module(self) -> None:
        """Module should be ESNext."""
        opts = self.tsconfig.get("compilerOptions", {})
        assert opts.get("module") == "ESNext"

    def test_include_src(self) -> None:
        """Include should contain 'src'."""
        include = self.tsconfig.get("include", [])
        assert "src" in include

    def test_skip_lib_check(self) -> None:
        """skipLibCheck should be true."""
        opts = self.tsconfig.get("compilerOptions", {})
        assert opts.get("skipLibCheck") is True


# ------------------------------------------------------------------
# vite.config.ts
# ------------------------------------------------------------------


class TestViteConfig:
    """Validate vite.config.ts content."""

    @pytest.fixture(autouse=True)
    def _load(self) -> None:
        """Read vite.config.ts."""
        self.content: str = _read("vite.config.ts")

    def test_imports_define_config(self) -> None:
        """Should import defineConfig from vite."""
        assert "defineConfig" in self.content
        assert "from 'vite'" in self.content

    def test_imports_react_plugin(self) -> None:
        """Should import the React plugin."""
        assert "@vitejs/plugin-react" in self.content

    def test_uses_react_plugin(self) -> None:
        """Should use react() in the plugins array."""
        assert "react()" in self.content

    def test_port_5173(self) -> None:
        """Should configure port 5173."""
        assert "5173" in self.content


# ------------------------------------------------------------------
# index.html
# ------------------------------------------------------------------


class TestIndexHtml:
    """Validate the Vite entry HTML file."""

    @pytest.fixture(autouse=True)
    def _load(self) -> None:
        """Read index.html."""
        self.content: str = _read("index.html")

    def test_doctype(self) -> None:
        """Should have an HTML5 doctype."""
        assert "<!DOCTYPE html>" in self.content

    def test_lang_en(self) -> None:
        """Should set lang to 'en'."""
        assert 'lang="en"' in self.content

    def test_charset_utf8(self) -> None:
        """Should declare UTF-8 charset."""
        assert 'charset="UTF-8"' in self.content

    def test_viewport_meta(self) -> None:
        """Should include a viewport meta tag."""
        assert "viewport" in self.content

    def test_title(self) -> None:
        """Title should be 'Hello World'."""
        assert "<title>Hello World</title>" in self.content

    def test_root_div(self) -> None:
        """Should have a root div for React mounting."""
        assert 'id="root"' in self.content

    def test_script_module(self) -> None:
        """Should have a module script pointing to src/main.tsx."""
        assert 'type="module"' in self.content
        assert 'src="/src/main.tsx"' in self.content


# ------------------------------------------------------------------
# src/main.tsx
# ------------------------------------------------------------------


class TestMainTsx:
    """Validate the React entry point."""

    @pytest.fixture(autouse=True)
    def _load(self) -> None:
        """Read src/main.tsx."""
        self.content: str = _read("src/main.tsx")

    def test_imports_react(self) -> None:
        """Should import React."""
        assert "import React" in self.content

    def test_imports_react_dom(self) -> None:
        """Should import ReactDOM from react-dom/client."""
        assert "react-dom/client" in self.content

    def test_imports_app(self) -> None:
        """Should import the App component."""
        assert "import App" in self.content

    def test_create_root(self) -> None:
        """Should call createRoot."""
        assert "createRoot" in self.content

    def test_strict_mode(self) -> None:
        """Should wrap App in StrictMode."""
        assert "StrictMode" in self.content

    def test_root_element(self) -> None:
        """Should target the 'root' element."""
        assert "root" in self.content


# ------------------------------------------------------------------
# src/App.tsx
# ------------------------------------------------------------------


class TestAppTsx:
    """Validate the App component."""

    @pytest.fixture(autouse=True)
    def _load(self) -> None:
        """Read src/App.tsx."""
        self.content: str = _read("src/App.tsx")

    def test_function_component(self) -> None:
        """Should define a function called App."""
        assert "function App" in self.content

    def test_export_default(self) -> None:
        """Should have a default export."""
        assert "export default App" in self.content

    def test_hello_world_text(self) -> None:
        """Should render 'Hello World' in an h1 tag."""
        assert "Hello World" in self.content
        assert "<h1" in self.content

    def test_flex_centering(self) -> None:
        """Should use flexbox centering styles."""
        assert "display" in self.content
        assert "flex" in self.content
        assert "justifyContent" in self.content
        assert "alignItems" in self.content

    def test_min_height_100vh(self) -> None:
        """Should use minHeight: '100vh' for full viewport."""
        assert "minHeight" in self.content
        assert "100vh" in self.content

    def test_app_container_class(self) -> None:
        """Should use 'app-container' className."""
        assert "app-container" in self.content


# ------------------------------------------------------------------
# Dockerfile
# ------------------------------------------------------------------


class TestDockerfile:
    """Validate the Dockerfile."""

    @pytest.fixture(autouse=True)
    def _load(self) -> None:
        """Read Dockerfile."""
        self.content: str = _read("Dockerfile")

    def test_base_image(self) -> None:
        """Should use a node alpine base image."""
        assert "node:" in self.content
        assert "alpine" in self.content

    def test_workdir(self) -> None:
        """Should set WORKDIR to /app."""
        assert "WORKDIR /app" in self.content

    def test_npm_install(self) -> None:
        """Should run npm install."""
        assert "npm install" in self.content

    def test_expose_5173(self) -> None:
        """Should expose port 5173."""
        assert "EXPOSE 5173" in self.content

    def test_cmd_dev(self) -> None:
        """Should default CMD to npm run dev."""
        assert "npm" in self.content
        assert "dev" in self.content


# ------------------------------------------------------------------
# docker-compose.yml
# ------------------------------------------------------------------


class TestDockerCompose:
    """Validate the docker-compose.yml."""

    @pytest.fixture(autouse=True)
    def _load(self) -> None:
        """Read docker-compose.yml."""
        self.content: str = _read("docker-compose.yml")

    def test_services_key(self) -> None:
        """Should define services."""
        assert "services:" in self.content

    def test_app_service(self) -> None:
        """Should define an 'app' service."""
        assert "app:" in self.content

    def test_port_mapping(self) -> None:
        """Should map port 5173."""
        assert "5173:5173" in self.content

    def test_build_context(self) -> None:
        """Should have a build directive."""
        assert "build" in self.content

    def test_volumes(self) -> None:
        """Should mount volumes for hot reload."""
        assert "volumes:" in self.content
        assert "/app/node_modules" in self.content


# ------------------------------------------------------------------
# RUNNING.md
# ------------------------------------------------------------------


class TestRunningMd:
    """Validate the RUNNING.md documentation."""

    @pytest.fixture(autouse=True)
    def _load(self) -> None:
        """Read RUNNING.md."""
        self.content: str = _read("RUNNING.md")

    def test_title(self) -> None:
        """Should have a main heading."""
        assert "# Hello World React App" in self.content

    def test_team_brief_section(self) -> None:
        """Should include TEAM_BRIEF section."""
        assert "## TEAM_BRIEF" in self.content

    def test_team_brief_stack(self) -> None:
        """Should specify the stack."""
        assert "TypeScript/React+Vite" in self.content

    def test_team_brief_test_runner(self) -> None:
        """Should specify the test runner."""
        assert "pytest tests/" in self.content

    def test_prerequisites_node(self) -> None:
        """Should mention Node.js prerequisite."""
        assert "Node.js" in self.content

    def test_prerequisites_npm(self) -> None:
        """Should mention npm prerequisite."""
        assert "npm" in self.content

    def test_npm_install_command(self) -> None:
        """Should include npm install command."""
        assert "npm install" in self.content

    def test_npm_run_dev_command(self) -> None:
        """Should include npm run dev command."""
        assert "npm run dev" in self.content

    def test_localhost_url(self) -> None:
        """Should include the localhost URL."""
        assert "http://localhost:5173" in self.content

    def test_docker_instructions(self) -> None:
        """Should include Docker instructions."""
        assert "docker compose up" in self.content
