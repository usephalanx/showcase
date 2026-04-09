"""Tests verifying project file structure and content correctness.

Validates that index.html, tsconfig.json, package.json, vite.config.ts,
src/main.tsx, src/App.tsx, Dockerfile, and docker-compose.yml exist
with the expected content.
"""

import json
import os
from pathlib import Path
from typing import Any, Dict

import pytest

# Resolve the project root (parent of the tests/ directory).
PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent


def _read(relative_path: str) -> str:
    """Read a file relative to the project root and return its text content.

    Args:
        relative_path: Path relative to the project root.

    Returns:
        The file content as a string.
    """
    return (PROJECT_ROOT / relative_path).read_text(encoding="utf-8")


def _read_json(relative_path: str) -> Dict[str, Any]:
    """Read and parse a JSON file relative to the project root.

    Args:
        relative_path: Path relative to the project root.

    Returns:
        Parsed JSON as a dictionary.
    """
    return json.loads(_read(relative_path))


# ---------------------------------------------------------------------------
# File existence tests
# ---------------------------------------------------------------------------


class TestFileExistence:
    """Verify that all required project files exist."""

    @pytest.mark.parametrize(
        "filepath",
        [
            "index.html",
            "tsconfig.json",
            "package.json",
            "vite.config.ts",
            "src/main.tsx",
            "src/App.tsx",
            "Dockerfile",
            "docker-compose.yml",
        ],
    )
    def test_file_exists(self, filepath: str) -> None:
        """Assert that the given file exists in the project root."""
        full_path = PROJECT_ROOT / filepath
        assert full_path.exists(), f"{filepath} does not exist"
        assert full_path.is_file(), f"{filepath} is not a regular file"


# ---------------------------------------------------------------------------
# index.html tests
# ---------------------------------------------------------------------------


class TestIndexHtml:
    """Verify index.html structure and content."""

    def test_has_doctype(self) -> None:
        """index.html must start with <!DOCTYPE html>."""
        content = _read("index.html")
        assert content.strip().startswith("<!DOCTYPE html>")

    def test_has_html_lang(self) -> None:
        """index.html must have an html tag with lang='en'."""
        content = _read("index.html")
        assert 'lang="en"' in content

    def test_has_charset_meta(self) -> None:
        """index.html must include a UTF-8 charset meta tag."""
        content = _read("index.html")
        assert 'charset="UTF-8"' in content

    def test_has_viewport_meta(self) -> None:
        """index.html must include a viewport meta tag."""
        content = _read("index.html")
        assert "viewport" in content

    def test_has_title(self) -> None:
        """index.html must have a <title> of 'Hello World'."""
        content = _read("index.html")
        assert "<title>Hello World</title>" in content

    def test_has_root_div(self) -> None:
        """index.html must contain <div id='root'></div>."""
        content = _read("index.html")
        assert '<div id="root"></div>' in content

    def test_has_script_module(self) -> None:
        """index.html must include a module script pointing to /src/main.tsx."""
        content = _read("index.html")
        assert '<script type="module" src="/src/main.tsx"></script>' in content


# ---------------------------------------------------------------------------
# tsconfig.json tests
# ---------------------------------------------------------------------------


class TestTsconfigJson:
    """Verify tsconfig.json compiler options."""

    def test_valid_json(self) -> None:
        """tsconfig.json must be valid JSON."""
        data = _read_json("tsconfig.json")
        assert isinstance(data, dict)

    def test_target(self) -> None:
        """compilerOptions.target must be 'ES2020'."""
        data = _read_json("tsconfig.json")
        assert data["compilerOptions"]["target"] == "ES2020"

    def test_use_define_for_class_fields(self) -> None:
        """compilerOptions.useDefineForClassFields must be true."""
        data = _read_json("tsconfig.json")
        assert data["compilerOptions"]["useDefineForClassFields"] is True

    def test_lib(self) -> None:
        """compilerOptions.lib must include ES2020, DOM, and DOM.Iterable."""
        data = _read_json("tsconfig.json")
        lib = data["compilerOptions"]["lib"]
        assert "ES2020" in lib
        assert "DOM" in lib
        assert "DOM.Iterable" in lib

    def test_module(self) -> None:
        """compilerOptions.module must be 'ESNext'."""
        data = _read_json("tsconfig.json")
        assert data["compilerOptions"]["module"] == "ESNext"

    def test_module_resolution(self) -> None:
        """compilerOptions.moduleResolution must be 'bundler'."""
        data = _read_json("tsconfig.json")
        assert data["compilerOptions"]["moduleResolution"] == "bundler"

    def test_jsx(self) -> None:
        """compilerOptions.jsx must be 'react-jsx'."""
        data = _read_json("tsconfig.json")
        assert data["compilerOptions"]["jsx"] == "react-jsx"

    def test_strict(self) -> None:
        """compilerOptions.strict must be true."""
        data = _read_json("tsconfig.json")
        assert data["compilerOptions"]["strict"] is True

    def test_skip_lib_check(self) -> None:
        """compilerOptions.skipLibCheck must be true."""
        data = _read_json("tsconfig.json")
        assert data["compilerOptions"]["skipLibCheck"] is True

    def test_include_src(self) -> None:
        """include must contain 'src'."""
        data = _read_json("tsconfig.json")
        assert "src" in data["include"]

    def test_no_emit(self) -> None:
        """compilerOptions.noEmit must be true."""
        data = _read_json("tsconfig.json")
        assert data["compilerOptions"]["noEmit"] is True

    def test_isolated_modules(self) -> None:
        """compilerOptions.isolatedModules must be true."""
        data = _read_json("tsconfig.json")
        assert data["compilerOptions"]["isolatedModules"] is True


# ---------------------------------------------------------------------------
# package.json tests
# ---------------------------------------------------------------------------


class TestPackageJson:
    """Verify package.json metadata and dependencies."""

    def test_valid_json(self) -> None:
        """package.json must be valid JSON."""
        data = _read_json("package.json")
        assert isinstance(data, dict)

    def test_name(self) -> None:
        """package.json name must be 'hello-world-react'."""
        data = _read_json("package.json")
        assert data["name"] == "hello-world-react"

    def test_private(self) -> None:
        """package.json must be marked private."""
        data = _read_json("package.json")
        assert data["private"] is True

    def test_type_module(self) -> None:
        """package.json type must be 'module'."""
        data = _read_json("package.json")
        assert data["type"] == "module"

    def test_has_react_dependency(self) -> None:
        """package.json must list react as a dependency."""
        data = _read_json("package.json")
        assert "react" in data["dependencies"]

    def test_has_react_dom_dependency(self) -> None:
        """package.json must list react-dom as a dependency."""
        data = _read_json("package.json")
        assert "react-dom" in data["dependencies"]

    def test_has_vite_dev_dependency(self) -> None:
        """package.json must list vite as a devDependency."""
        data = _read_json("package.json")
        assert "vite" in data["devDependencies"]

    def test_has_typescript_dev_dependency(self) -> None:
        """package.json must list typescript as a devDependency."""
        data = _read_json("package.json")
        assert "typescript" in data["devDependencies"]

    def test_scripts_dev(self) -> None:
        """package.json scripts.dev must be 'vite'."""
        data = _read_json("package.json")
        assert data["scripts"]["dev"] == "vite"

    def test_scripts_build(self) -> None:
        """package.json scripts.build must be 'tsc && vite build'."""
        data = _read_json("package.json")
        assert data["scripts"]["build"] == "tsc && vite build"

    def test_scripts_preview(self) -> None:
        """package.json scripts.preview must be 'vite preview'."""
        data = _read_json("package.json")
        assert data["scripts"]["preview"] == "vite preview"


# ---------------------------------------------------------------------------
# vite.config.ts tests
# ---------------------------------------------------------------------------


class TestViteConfig:
    """Verify vite.config.ts content."""

    def test_imports_define_config(self) -> None:
        """vite.config.ts must import defineConfig from 'vite'."""
        content = _read("vite.config.ts")
        assert "defineConfig" in content
        assert "from 'vite'" in content

    def test_imports_react_plugin(self) -> None:
        """vite.config.ts must import react from '@vitejs/plugin-react'."""
        content = _read("vite.config.ts")
        assert "@vitejs/plugin-react" in content

    def test_exports_config(self) -> None:
        """vite.config.ts must export a default config."""
        content = _read("vite.config.ts")
        assert "export default defineConfig" in content

    def test_react_plugin_used(self) -> None:
        """vite.config.ts must call react() in plugins."""
        content = _read("vite.config.ts")
        assert "react()" in content

    def test_port_5173(self) -> None:
        """vite.config.ts must set server port to 5173."""
        content = _read("vite.config.ts")
        assert "5173" in content


# ---------------------------------------------------------------------------
# src/main.tsx tests
# ---------------------------------------------------------------------------


class TestMainTsx:
    """Verify src/main.tsx content."""

    def test_imports_react(self) -> None:
        """main.tsx must import React."""
        content = _read("src/main.tsx")
        assert "import React" in content

    def test_imports_react_dom(self) -> None:
        """main.tsx must import from react-dom/client."""
        content = _read("src/main.tsx")
        assert "react-dom/client" in content

    def test_imports_app(self) -> None:
        """main.tsx must import App."""
        content = _read("src/main.tsx")
        assert "import App" in content

    def test_creates_root(self) -> None:
        """main.tsx must call createRoot with getElementById('root')."""
        content = _read("src/main.tsx")
        assert "createRoot" in content
        assert "getElementById('root')" in content

    def test_strict_mode(self) -> None:
        """main.tsx must use React.StrictMode."""
        content = _read("src/main.tsx")
        assert "StrictMode" in content


# ---------------------------------------------------------------------------
# src/App.tsx tests
# ---------------------------------------------------------------------------


class TestAppTsx:
    """Verify src/App.tsx content."""

    def test_exports_app_function(self) -> None:
        """App.tsx must export default App."""
        content = _read("src/App.tsx")
        assert "export default App" in content

    def test_has_hello_world(self) -> None:
        """App.tsx must render 'Hello World'."""
        content = _read("src/App.tsx")
        assert "Hello World" in content

    def test_has_h1_tag(self) -> None:
        """App.tsx must use an h1 element."""
        content = _read("src/App.tsx")
        assert "<h1" in content

    def test_has_app_container_class(self) -> None:
        """App.tsx must have className 'app-container'."""
        content = _read("src/App.tsx")
        assert "app-container" in content

    def test_uses_flex_display(self) -> None:
        """App.tsx must use flex display for centering."""
        content = _read("src/App.tsx")
        assert "flex" in content


# ---------------------------------------------------------------------------
# Dockerfile tests
# ---------------------------------------------------------------------------


class TestDockerfile:
    """Verify Dockerfile content."""

    def test_uses_node_alpine(self) -> None:
        """Dockerfile must use node:20-alpine as the base image."""
        content = _read("Dockerfile")
        assert "node:20-alpine" in content

    def test_has_workdir(self) -> None:
        """Dockerfile must set WORKDIR to /app."""
        content = _read("Dockerfile")
        assert "WORKDIR /app" in content

    def test_copies_package_json(self) -> None:
        """Dockerfile must copy package.json."""
        content = _read("Dockerfile")
        assert "package.json" in content

    def test_runs_npm_install(self) -> None:
        """Dockerfile must run npm install."""
        content = _read("Dockerfile")
        assert "npm install" in content

    def test_exposes_5173(self) -> None:
        """Dockerfile must expose port 5173."""
        content = _read("Dockerfile")
        assert "EXPOSE 5173" in content

    def test_runs_dev(self) -> None:
        """Dockerfile CMD must run 'npm run dev'."""
        content = _read("Dockerfile")
        assert "npm" in content
        assert "dev" in content


# ---------------------------------------------------------------------------
# docker-compose.yml tests
# ---------------------------------------------------------------------------


class TestDockerCompose:
    """Verify docker-compose.yml content."""

    def test_has_services(self) -> None:
        """docker-compose.yml must define services."""
        content = _read("docker-compose.yml")
        assert "services:" in content

    def test_has_app_service(self) -> None:
        """docker-compose.yml must define an 'app' service."""
        content = _read("docker-compose.yml")
        assert "app:" in content

    def test_maps_port_5173(self) -> None:
        """docker-compose.yml must map port 5173."""
        content = _read("docker-compose.yml")
        assert "5173:5173" in content

    def test_has_volume_mount(self) -> None:
        """docker-compose.yml must mount current directory."""
        content = _read("docker-compose.yml")
        assert ".:/app" in content

    def test_has_node_modules_volume(self) -> None:
        """docker-compose.yml must have node_modules anonymous volume."""
        content = _read("docker-compose.yml")
        assert "/app/node_modules" in content
