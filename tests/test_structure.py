"""Tests verifying the project file structure and content correctness.

Validates that all required files exist and contain the expected content
for the Hello World React application.
"""

import os
import re
from pathlib import Path
from typing import List

import pytest

# Resolve the project root (one level above 'tests/')
PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent


class TestProjectFiles:
    """Ensure every required project file exists."""

    REQUIRED_FILES: List[str] = [
        "src/App.tsx",
        "src/main.tsx",
        "index.html",
        "package.json",
        "tsconfig.json",
        "vite.config.ts",
        "Dockerfile",
        "docker-compose.yml",
    ]

    @pytest.mark.parametrize("filepath", REQUIRED_FILES)
    def test_file_exists(self, filepath: str) -> None:
        """Verify that a required file exists in the project root."""
        full_path = PROJECT_ROOT / filepath
        assert full_path.exists(), f"Missing required file: {filepath}"

    @pytest.mark.parametrize("filepath", REQUIRED_FILES)
    def test_file_not_empty(self, filepath: str) -> None:
        """Verify that each required file is not empty."""
        full_path = PROJECT_ROOT / filepath
        assert full_path.stat().st_size > 0, f"File is empty: {filepath}"


class TestAppComponent:
    """Validate the App.tsx component content."""

    @pytest.fixture()
    def app_content(self) -> str:
        """Read and return the contents of src/App.tsx."""
        return (PROJECT_ROOT / "src" / "App.tsx").read_text(encoding="utf-8")

    def test_contains_hello_world(self, app_content: str) -> None:
        """App.tsx must render the text 'Hello World'."""
        assert "Hello World" in app_content

    def test_default_export(self, app_content: str) -> None:
        """App.tsx must have a default export."""
        assert "export default" in app_content

    def test_function_app_defined(self, app_content: str) -> None:
        """App.tsx must define a function named App."""
        assert re.search(r"function\s+App", app_content) is not None

    def test_display_flex(self, app_content: str) -> None:
        """App.tsx must use display flex for centering."""
        assert "display" in app_content
        assert "flex" in app_content

    def test_justify_content_center(self, app_content: str) -> None:
        """App.tsx must use justifyContent center."""
        assert "justifyContent" in app_content
        assert "center" in app_content

    def test_align_items_center(self, app_content: str) -> None:
        """App.tsx must use alignItems center."""
        assert "alignItems" in app_content

    def test_height_100vh(self, app_content: str) -> None:
        """App.tsx must set height to 100vh."""
        assert "100vh" in app_content

    def test_margin_zero(self, app_content: str) -> None:
        """App.tsx must set margin to 0."""
        assert re.search(r"margin\s*:\s*0", app_content) is not None

    def test_font_family_sans_serif(self, app_content: str) -> None:
        """App.tsx must set fontFamily to sans-serif."""
        assert "fontFamily" in app_content
        assert "sans-serif" in app_content

    def test_font_size_2rem(self, app_content: str) -> None:
        """App.tsx must set fontSize to 2rem."""
        assert "fontSize" in app_content
        assert "2rem" in app_content

    def test_no_props(self, app_content: str) -> None:
        """App component should not accept props."""
        # The function signature should be App() with no parameters
        assert re.search(r"function\s+App\s*\(\)", app_content) is not None

    def test_no_usestate_import(self, app_content: str) -> None:
        """App.tsx should not import or use useState."""
        assert "useState" not in app_content

    def test_no_useeffect_import(self, app_content: str) -> None:
        """App.tsx should not import or use useEffect."""
        assert "useEffect" not in app_content

    def test_inline_style_object(self, app_content: str) -> None:
        """App.tsx must use inline style via style={{ ... }}."""
        assert "style={{" in app_content or "style={\n" in app_content or "style={" in app_content


class TestMainEntry:
    """Validate the main.tsx entry point."""

    @pytest.fixture()
    def main_content(self) -> str:
        """Read and return the contents of src/main.tsx."""
        return (PROJECT_ROOT / "src" / "main.tsx").read_text(encoding="utf-8")

    def test_imports_react(self, main_content: str) -> None:
        """main.tsx must import React."""
        assert "import React" in main_content or "from 'react'" in main_content

    def test_imports_react_dom(self, main_content: str) -> None:
        """main.tsx must import from react-dom/client."""
        assert "react-dom/client" in main_content

    def test_imports_app(self, main_content: str) -> None:
        """main.tsx must import the App component."""
        assert "import App" in main_content

    def test_create_root(self, main_content: str) -> None:
        """main.tsx must call createRoot."""
        assert "createRoot" in main_content

    def test_strict_mode(self, main_content: str) -> None:
        """main.tsx must wrap App in StrictMode."""
        assert "StrictMode" in main_content

    def test_root_element(self, main_content: str) -> None:
        """main.tsx must reference the 'root' DOM element."""
        assert "root" in main_content


class TestIndexHtml:
    """Validate the index.html entry file."""

    @pytest.fixture()
    def html_content(self) -> str:
        """Read and return the contents of index.html."""
        return (PROJECT_ROOT / "index.html").read_text(encoding="utf-8")

    def test_doctype(self, html_content: str) -> None:
        """index.html must start with DOCTYPE."""
        assert "<!DOCTYPE html>" in html_content

    def test_root_div(self, html_content: str) -> None:
        """index.html must have a div with id 'root'."""
        assert 'id="root"' in html_content

    def test_script_module(self, html_content: str) -> None:
        """index.html must include a module script pointing to main.tsx."""
        assert 'type="module"' in html_content
        assert "src=\"/src/main.tsx\"" in html_content

    def test_charset_utf8(self, html_content: str) -> None:
        """index.html must declare UTF-8 charset."""
        assert "UTF-8" in html_content

    def test_viewport_meta(self, html_content: str) -> None:
        """index.html must have a viewport meta tag."""
        assert "viewport" in html_content

    def test_title(self, html_content: str) -> None:
        """index.html must have a title element."""
        assert "<title>" in html_content


class TestPackageJson:
    """Validate package.json content."""

    @pytest.fixture()
    def pkg_content(self) -> str:
        """Read and return the contents of package.json."""
        return (PROJECT_ROOT / "package.json").read_text(encoding="utf-8")

    def test_has_react_dependency(self, pkg_content: str) -> None:
        """package.json must list react as a dependency."""
        assert '"react"' in pkg_content

    def test_has_react_dom_dependency(self, pkg_content: str) -> None:
        """package.json must list react-dom as a dependency."""
        assert '"react-dom"' in pkg_content

    def test_has_vite_devdep(self, pkg_content: str) -> None:
        """package.json must list vite as a dev dependency."""
        assert '"vite"' in pkg_content

    def test_has_typescript_devdep(self, pkg_content: str) -> None:
        """package.json must list typescript as a dev dependency."""
        assert '"typescript"' in pkg_content

    def test_has_dev_script(self, pkg_content: str) -> None:
        """package.json must have a 'dev' script."""
        assert '"dev"' in pkg_content

    def test_has_build_script(self, pkg_content: str) -> None:
        """package.json must have a 'build' script."""
        assert '"build"' in pkg_content

    def test_is_private(self, pkg_content: str) -> None:
        """package.json must be marked as private."""
        assert '"private": true' in pkg_content

    def test_module_type(self, pkg_content: str) -> None:
        """package.json must set type to module."""
        assert '"type": "module"' in pkg_content


class TestTsConfig:
    """Validate tsconfig.json content."""

    @pytest.fixture()
    def ts_content(self) -> str:
        """Read and return the contents of tsconfig.json."""
        return (PROJECT_ROOT / "tsconfig.json").read_text(encoding="utf-8")

    def test_strict_mode(self, ts_content: str) -> None:
        """tsconfig.json must enable strict mode."""
        assert '"strict": true' in ts_content

    def test_react_jsx(self, ts_content: str) -> None:
        """tsconfig.json must set jsx to react-jsx."""
        assert '"react-jsx"' in ts_content

    def test_target_es2020(self, ts_content: str) -> None:
        """tsconfig.json must target ES2020."""
        assert '"ES2020"' in ts_content

    def test_include_src(self, ts_content: str) -> None:
        """tsconfig.json must include the src directory."""
        assert '"src"' in ts_content


class TestViteConfig:
    """Validate vite.config.ts content."""

    @pytest.fixture()
    def vite_content(self) -> str:
        """Read and return the contents of vite.config.ts."""
        return (PROJECT_ROOT / "vite.config.ts").read_text(encoding="utf-8")

    def test_imports_define_config(self, vite_content: str) -> None:
        """vite.config.ts must import defineConfig."""
        assert "defineConfig" in vite_content

    def test_imports_react_plugin(self, vite_content: str) -> None:
        """vite.config.ts must import the React plugin."""
        assert "@vitejs/plugin-react" in vite_content

    def test_uses_react_plugin(self, vite_content: str) -> None:
        """vite.config.ts must invoke the react() plugin."""
        assert "react()" in vite_content

    def test_port_5173(self, vite_content: str) -> None:
        """vite.config.ts must configure port 5173."""
        assert "5173" in vite_content


class TestDockerfile:
    """Validate the Dockerfile content."""

    @pytest.fixture()
    def dockerfile_content(self) -> str:
        """Read and return the contents of Dockerfile."""
        return (PROJECT_ROOT / "Dockerfile").read_text(encoding="utf-8")

    def test_from_node(self, dockerfile_content: str) -> None:
        """Dockerfile must use a Node base image."""
        assert "FROM node:" in dockerfile_content

    def test_workdir(self, dockerfile_content: str) -> None:
        """Dockerfile must set a WORKDIR."""
        assert "WORKDIR" in dockerfile_content

    def test_npm_install(self, dockerfile_content: str) -> None:
        """Dockerfile must run npm install."""
        assert "npm install" in dockerfile_content

    def test_expose_5173(self, dockerfile_content: str) -> None:
        """Dockerfile must expose port 5173."""
        assert "EXPOSE 5173" in dockerfile_content

    def test_cmd(self, dockerfile_content: str) -> None:
        """Dockerfile must have a CMD instruction."""
        assert "CMD" in dockerfile_content


class TestDockerCompose:
    """Validate docker-compose.yml content."""

    @pytest.fixture()
    def compose_content(self) -> str:
        """Read and return the contents of docker-compose.yml."""
        return (PROJECT_ROOT / "docker-compose.yml").read_text(encoding="utf-8")

    def test_has_services(self, compose_content: str) -> None:
        """docker-compose.yml must define services."""
        assert "services:" in compose_content

    def test_port_mapping(self, compose_content: str) -> None:
        """docker-compose.yml must map port 5173."""
        assert "5173:5173" in compose_content

    def test_volumes(self, compose_content: str) -> None:
        """docker-compose.yml must define volumes for hot reload."""
        assert "volumes:" in compose_content

    def test_node_modules_volume(self, compose_content: str) -> None:
        """docker-compose.yml must include node_modules anonymous volume."""
        assert "/app/node_modules" in compose_content
