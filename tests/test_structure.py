"""Tests verifying file structure and content correctness of the React project.

These tests validate that every required source file exists, contains the
expected imports / content, and that configuration files are well-formed.
"""

import json
from pathlib import Path
from typing import List

import pytest

# Resolve project root (one level up from tests/)
PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent


def _read(relative_path: str) -> str:
    """Read a project file and return its content as a string.

    Args:
        relative_path: Path relative to the project root.

    Returns:
        The file content.
    """
    return (PROJECT_ROOT / relative_path).read_text(encoding="utf-8")


# ------------------------------------------------------------------
# File existence checks
# ------------------------------------------------------------------

_REQUIRED_FILES: List[str] = [
    "src/main.tsx",
    "src/App.tsx",
    "index.html",
    "package.json",
    "tsconfig.json",
    "vite.config.ts",
    "Dockerfile",
    "docker-compose.yml",
]


@pytest.mark.parametrize("filepath", _REQUIRED_FILES)
def test_required_file_exists(filepath: str) -> None:
    """Ensure every required project file is present."""
    assert (PROJECT_ROOT / filepath).is_file(), f"{filepath} must exist"


# ------------------------------------------------------------------
# src/main.tsx
# ------------------------------------------------------------------


class TestMainTsx:
    """Tests for the React entry point src/main.tsx."""

    def test_imports_react(self) -> None:
        """main.tsx must import React."""
        content = _read("src/main.tsx")
        assert "import React from 'react'" in content

    def test_imports_react_dom_client(self) -> None:
        """main.tsx must import ReactDOM from 'react-dom/client'."""
        content = _read("src/main.tsx")
        assert "import ReactDOM from 'react-dom/client'" in content

    def test_imports_app(self) -> None:
        """main.tsx must import App from './App'."""
        content = _read("src/main.tsx")
        assert "import App from './App'" in content

    def test_creates_root(self) -> None:
        """main.tsx must call ReactDOM.createRoot with the root element."""
        content = _read("src/main.tsx")
        assert "ReactDOM.createRoot(document.getElementById('root')!)" in content

    def test_strict_mode(self) -> None:
        """main.tsx must render inside React.StrictMode."""
        content = _read("src/main.tsx")
        assert "<React.StrictMode>" in content
        assert "</React.StrictMode>" in content

    def test_renders_app(self) -> None:
        """main.tsx must render the <App /> component."""
        content = _read("src/main.tsx")
        assert "<App />" in content


# ------------------------------------------------------------------
# src/App.tsx
# ------------------------------------------------------------------


class TestAppTsx:
    """Tests for the main App component."""

    def test_exports_default_function(self) -> None:
        """App.tsx must export a default function App."""
        content = _read("src/App.tsx")
        assert "function App()" in content
        assert "export default App" in content

    def test_hello_world_heading(self) -> None:
        """App.tsx must contain an h1 with 'Hello World'."""
        content = _read("src/App.tsx")
        assert "Hello World" in content
        assert "<h1" in content

    def test_app_container_classname(self) -> None:
        """App.tsx wrapper div must have className 'app-container'."""
        content = _read("src/App.tsx")
        assert 'className="app-container"' in content

    def test_flex_centering(self) -> None:
        """App.tsx must use flex centering styles."""
        content = _read("src/App.tsx")
        assert "display: 'flex'" in content
        assert "justifyContent: 'center'" in content
        assert "alignItems: 'center'" in content
        assert "minHeight: '100vh'" in content


# ------------------------------------------------------------------
# index.html
# ------------------------------------------------------------------


class TestIndexHtml:
    """Tests for the Vite entry HTML file."""

    def test_has_root_div(self) -> None:
        """index.html must contain a <div id='root'>."""
        content = _read("index.html")
        assert '<div id="root"></div>' in content

    def test_references_main_tsx(self) -> None:
        """index.html must reference /src/main.tsx as a module script."""
        content = _read("index.html")
        assert 'src="/src/main.tsx"' in content
        assert 'type="module"' in content

    def test_has_doctype(self) -> None:
        """index.html must start with <!DOCTYPE html>."""
        content = _read("index.html")
        assert content.strip().startswith("<!DOCTYPE html>")

    def test_has_title(self) -> None:
        """index.html must have a title of 'Hello World'."""
        content = _read("index.html")
        assert "<title>Hello World</title>" in content

    def test_has_charset_meta(self) -> None:
        """index.html must declare UTF-8 charset."""
        content = _read("index.html")
        assert 'charset="UTF-8"' in content

    def test_has_viewport_meta(self) -> None:
        """index.html must contain a viewport meta tag."""
        content = _read("index.html")
        assert 'name="viewport"' in content

    def test_lang_attribute(self) -> None:
        """index.html must set lang='en'."""
        content = _read("index.html")
        assert 'lang="en"' in content


# ------------------------------------------------------------------
# package.json
# ------------------------------------------------------------------


class TestPackageJson:
    """Tests for the package.json configuration."""

    @pytest.fixture()
    def pkg(self) -> dict:
        """Parse and return package.json as a dict."""
        return json.loads(_read("package.json"))

    def test_name(self, pkg: dict) -> None:
        """package.json must have name 'hello-world-react'."""
        assert pkg["name"] == "hello-world-react"

    def test_private(self, pkg: dict) -> None:
        """package.json must be private."""
        assert pkg["private"] is True

    def test_type_module(self, pkg: dict) -> None:
        """package.json must set type to 'module'."""
        assert pkg["type"] == "module"

    def test_has_react_dependency(self, pkg: dict) -> None:
        """package.json must list react as a dependency."""
        assert "react" in pkg["dependencies"]

    def test_has_react_dom_dependency(self, pkg: dict) -> None:
        """package.json must list react-dom as a dependency."""
        assert "react-dom" in pkg["dependencies"]

    def test_has_vite_devdep(self, pkg: dict) -> None:
        """package.json must list vite as a dev dependency."""
        assert "vite" in pkg["devDependencies"]

    def test_has_typescript_devdep(self, pkg: dict) -> None:
        """package.json must list typescript as a dev dependency."""
        assert "typescript" in pkg["devDependencies"]

    def test_has_plugin_react_devdep(self, pkg: dict) -> None:
        """package.json must list @vitejs/plugin-react as a dev dependency."""
        assert "@vitejs/plugin-react" in pkg["devDependencies"]

    def test_dev_script(self, pkg: dict) -> None:
        """package.json dev script must run vite."""
        assert pkg["scripts"]["dev"] == "vite"

    def test_build_script(self, pkg: dict) -> None:
        """package.json build script must run tsc && vite build."""
        assert pkg["scripts"]["build"] == "tsc && vite build"

    def test_preview_script(self, pkg: dict) -> None:
        """package.json preview script must run vite preview."""
        assert pkg["scripts"]["preview"] == "vite preview"


# ------------------------------------------------------------------
# tsconfig.json
# ------------------------------------------------------------------


class TestTsconfig:
    """Tests for the TypeScript configuration."""

    @pytest.fixture()
    def tsconfig(self) -> dict:
        """Parse and return tsconfig.json as a dict."""
        return json.loads(_read("tsconfig.json"))

    def test_target(self, tsconfig: dict) -> None:
        """tsconfig must target ES2020."""
        assert tsconfig["compilerOptions"]["target"] == "ES2020"

    def test_jsx(self, tsconfig: dict) -> None:
        """tsconfig must set jsx to 'react-jsx'."""
        assert tsconfig["compilerOptions"]["jsx"] == "react-jsx"

    def test_strict(self, tsconfig: dict) -> None:
        """tsconfig must enable strict mode."""
        assert tsconfig["compilerOptions"]["strict"] is True

    def test_include_src(self, tsconfig: dict) -> None:
        """tsconfig must include the 'src' directory."""
        assert "src" in tsconfig["include"]

    def test_module(self, tsconfig: dict) -> None:
        """tsconfig must set module to ESNext."""
        assert tsconfig["compilerOptions"]["module"] == "ESNext"

    def test_module_resolution(self, tsconfig: dict) -> None:
        """tsconfig must set moduleResolution to bundler."""
        assert tsconfig["compilerOptions"]["moduleResolution"] == "bundler"

    def test_skip_lib_check(self, tsconfig: dict) -> None:
        """tsconfig must set skipLibCheck to true."""
        assert tsconfig["compilerOptions"]["skipLibCheck"] is True


# ------------------------------------------------------------------
# vite.config.ts
# ------------------------------------------------------------------


class TestViteConfig:
    """Tests for the Vite configuration file."""

    def test_imports_define_config(self) -> None:
        """vite.config.ts must import defineConfig."""
        content = _read("vite.config.ts")
        assert "defineConfig" in content

    def test_imports_react_plugin(self) -> None:
        """vite.config.ts must import the React plugin."""
        content = _read("vite.config.ts")
        assert "@vitejs/plugin-react" in content

    def test_uses_react_plugin(self) -> None:
        """vite.config.ts must use react() in plugins."""
        content = _read("vite.config.ts")
        assert "react()" in content

    def test_port_5173(self) -> None:
        """vite.config.ts must configure port 5173."""
        content = _read("vite.config.ts")
        assert "5173" in content

    def test_host_true(self) -> None:
        """vite.config.ts must set host to true."""
        content = _read("vite.config.ts")
        assert "host: true" in content


# ------------------------------------------------------------------
# Dockerfile
# ------------------------------------------------------------------


class TestDockerfile:
    """Tests for the Dockerfile."""

    def test_base_image(self) -> None:
        """Dockerfile must use node:20-alpine."""
        content = _read("Dockerfile")
        assert "node:20-alpine" in content

    def test_workdir(self) -> None:
        """Dockerfile must set WORKDIR to /app."""
        content = _read("Dockerfile")
        assert "WORKDIR /app" in content

    def test_npm_install(self) -> None:
        """Dockerfile must run npm install."""
        content = _read("Dockerfile")
        assert "npm install" in content

    def test_exposes_5173(self) -> None:
        """Dockerfile must expose port 5173."""
        content = _read("Dockerfile")
        assert "EXPOSE 5173" in content

    def test_cmd(self) -> None:
        """Dockerfile must have CMD for npm run dev."""
        content = _read("Dockerfile")
        assert "npm" in content
        assert "dev" in content


# ------------------------------------------------------------------
# docker-compose.yml
# ------------------------------------------------------------------


class TestDockerCompose:
    """Tests for the docker-compose.yml file."""

    def test_port_mapping(self) -> None:
        """docker-compose.yml must map port 5173:5173."""
        content = _read("docker-compose.yml")
        assert "5173:5173" in content

    def test_volume_mount(self) -> None:
        """docker-compose.yml must mount current dir as volume."""
        content = _read("docker-compose.yml")
        assert ".:/app" in content

    def test_node_modules_volume(self) -> None:
        """docker-compose.yml must use anonymous volume for node_modules."""
        content = _read("docker-compose.yml")
        assert "/app/node_modules" in content
