"""Tests verifying project file structure and content correctness.

Validates that all required files exist with the expected content,
including package.json fields, vite.config.ts setup, tsconfig.json
options, index.html structure, React components, and Docker files.
"""

import json
import os
from pathlib import Path
from typing import Any, Dict

import pytest

# Root of the project is one level up from the tests/ directory
ROOT: Path = Path(__file__).resolve().parent.parent


def _read(relative_path: str) -> str:
    """Read and return the full text content of a file relative to project root."""
    return (ROOT / relative_path).read_text(encoding="utf-8")


def _load_json(relative_path: str) -> Dict[str, Any]:
    """Read and parse a JSON file relative to project root."""
    return json.loads(_read(relative_path))


# ---------------------------------------------------------------------------
# File existence
# ---------------------------------------------------------------------------


class TestFileExistence:
    """Verify that every required project file exists."""

    @pytest.mark.parametrize(
        "filepath",
        [
            "package.json",
            "vite.config.ts",
            "tsconfig.json",
            "index.html",
            "src/main.tsx",
            "src/App.tsx",
            "Dockerfile",
            "docker-compose.yml",
        ],
    )
    def test_file_exists(self, filepath: str) -> None:
        """Assert that the given file path exists in the project root."""
        full_path = ROOT / filepath
        assert full_path.exists(), f"{filepath} does not exist"
        assert full_path.is_file(), f"{filepath} is not a file"


# ---------------------------------------------------------------------------
# package.json
# ---------------------------------------------------------------------------


class TestPackageJson:
    """Validate package.json structure and content."""

    @pytest.fixture(autouse=True)
    def _load(self) -> None:
        """Load package.json once for every test in this class."""
        self.pkg: Dict[str, Any] = _load_json("package.json")

    def test_name(self) -> None:
        """Name should be hello-world-react."""
        assert self.pkg["name"] == "hello-world-react"

    def test_private(self) -> None:
        """Package must be marked as private."""
        assert self.pkg["private"] is True

    def test_type_module(self) -> None:
        """Package type must be 'module'."""
        assert self.pkg["type"] == "module"

    def test_scripts_dev(self) -> None:
        """dev script should invoke vite."""
        assert self.pkg["scripts"]["dev"] == "vite"

    def test_scripts_build(self) -> None:
        """build script should invoke tsc && vite build."""
        assert "vite build" in self.pkg["scripts"]["build"]

    def test_scripts_preview(self) -> None:
        """preview script should invoke vite preview."""
        assert self.pkg["scripts"]["preview"] == "vite preview"

    def test_dependency_react(self) -> None:
        """react must be listed as a dependency with ^18."""
        assert "react" in self.pkg["dependencies"]
        assert self.pkg["dependencies"]["react"].startswith("^18")

    def test_dependency_react_dom(self) -> None:
        """react-dom must be listed as a dependency with ^18."""
        assert "react-dom" in self.pkg["dependencies"]
        assert self.pkg["dependencies"]["react-dom"].startswith("^18")

    def test_devdep_vite(self) -> None:
        """vite must be listed as a dev dependency."""
        assert "vite" in self.pkg["devDependencies"]

    def test_devdep_plugin_react(self) -> None:
        """@vitejs/plugin-react must be a dev dependency."""
        assert "@vitejs/plugin-react" in self.pkg["devDependencies"]

    def test_devdep_typescript(self) -> None:
        """typescript must be a dev dependency."""
        assert "typescript" in self.pkg["devDependencies"]

    def test_devdep_types_react(self) -> None:
        """@types/react must be a dev dependency."""
        assert "@types/react" in self.pkg["devDependencies"]

    def test_devdep_types_react_dom(self) -> None:
        """@types/react-dom must be a dev dependency."""
        assert "@types/react-dom" in self.pkg["devDependencies"]


# ---------------------------------------------------------------------------
# vite.config.ts
# ---------------------------------------------------------------------------


class TestViteConfig:
    """Validate vite.config.ts content."""

    @pytest.fixture(autouse=True)
    def _load(self) -> None:
        """Read vite.config.ts."""
        self.content: str = _read("vite.config.ts")

    def test_imports_define_config(self) -> None:
        """Must import defineConfig from vite."""
        assert "defineConfig" in self.content
        assert "from 'vite'" in self.content

    def test_imports_react_plugin(self) -> None:
        """Must import react from @vitejs/plugin-react."""
        assert "from '@vitejs/plugin-react'" in self.content

    def test_exports_define_config(self) -> None:
        """Must export defineConfig call."""
        assert "export default defineConfig" in self.content

    def test_plugins_react(self) -> None:
        """Must include react() in plugins array."""
        assert "plugins:" in self.content or "plugins" in self.content
        assert "react()" in self.content

    def test_server_port(self) -> None:
        """Must configure server port 5173."""
        assert "5173" in self.content


# ---------------------------------------------------------------------------
# tsconfig.json
# ---------------------------------------------------------------------------


class TestTsConfig:
    """Validate tsconfig.json content."""

    @pytest.fixture(autouse=True)
    def _load(self) -> None:
        """Load tsconfig.json."""
        self.cfg: Dict[str, Any] = _load_json("tsconfig.json")

    def test_target(self) -> None:
        """Compiler target should be ES2020."""
        assert self.cfg["compilerOptions"]["target"] == "ES2020"

    def test_jsx(self) -> None:
        """jsx option should be react-jsx."""
        assert self.cfg["compilerOptions"]["jsx"] == "react-jsx"

    def test_strict(self) -> None:
        """strict mode should be enabled."""
        assert self.cfg["compilerOptions"]["strict"] is True

    def test_module(self) -> None:
        """module should be ESNext."""
        assert self.cfg["compilerOptions"]["module"] == "ESNext"

    def test_module_resolution(self) -> None:
        """moduleResolution should be bundler."""
        assert self.cfg["compilerOptions"]["moduleResolution"] == "bundler"

    def test_include_src(self) -> None:
        """include should contain 'src'."""
        assert "src" in self.cfg["include"]

    def test_lib_contains_dom(self) -> None:
        """lib should include DOM."""
        assert "DOM" in self.cfg["compilerOptions"]["lib"]

    def test_skip_lib_check(self) -> None:
        """skipLibCheck should be true."""
        assert self.cfg["compilerOptions"]["skipLibCheck"] is True


# ---------------------------------------------------------------------------
# index.html
# ---------------------------------------------------------------------------


class TestIndexHtml:
    """Validate index.html content."""

    @pytest.fixture(autouse=True)
    def _load(self) -> None:
        """Read index.html."""
        self.content: str = _read("index.html")

    def test_doctype(self) -> None:
        """Must have HTML5 doctype."""
        assert "<!DOCTYPE html>" in self.content

    def test_lang_en(self) -> None:
        """html tag should have lang=en."""
        assert 'lang="en"' in self.content

    def test_charset(self) -> None:
        """Must set charset to UTF-8."""
        assert 'charset="UTF-8"' in self.content

    def test_viewport(self) -> None:
        """Must include viewport meta tag."""
        assert "viewport" in self.content

    def test_title(self) -> None:
        """Title should be Hello World."""
        assert "<title>Hello World</title>" in self.content

    def test_root_div(self) -> None:
        """Must have a div with id root."""
        assert 'id="root"' in self.content

    def test_script_module(self) -> None:
        """Must have a module script pointing to /src/main.tsx."""
        assert 'type="module"' in self.content
        assert 'src="/src/main.tsx"' in self.content


# ---------------------------------------------------------------------------
# src/main.tsx
# ---------------------------------------------------------------------------


class TestMainTsx:
    """Validate src/main.tsx content."""

    @pytest.fixture(autouse=True)
    def _load(self) -> None:
        """Read src/main.tsx."""
        self.content: str = _read("src/main.tsx")

    def test_imports_react(self) -> None:
        """Must import React."""
        assert "import React" in self.content

    def test_imports_react_dom(self) -> None:
        """Must import from react-dom/client."""
        assert "react-dom/client" in self.content

    def test_imports_app(self) -> None:
        """Must import App component."""
        assert "import App" in self.content

    def test_create_root(self) -> None:
        """Must call createRoot."""
        assert "createRoot" in self.content

    def test_strict_mode(self) -> None:
        """Must use React.StrictMode."""
        assert "StrictMode" in self.content

    def test_root_element(self) -> None:
        """Must target the root element."""
        assert "getElementById('root')" in self.content


# ---------------------------------------------------------------------------
# src/App.tsx
# ---------------------------------------------------------------------------


class TestAppTsx:
    """Validate src/App.tsx content."""

    @pytest.fixture(autouse=True)
    def _load(self) -> None:
        """Read src/App.tsx."""
        self.content: str = _read("src/App.tsx")

    def test_exports_default_function(self) -> None:
        """Must export a default function App."""
        assert "export default function App" in self.content

    def test_hello_world_text(self) -> None:
        """Must render 'Hello World' in an h1."""
        assert "Hello World" in self.content
        assert "<h1" in self.content

    def test_app_container_class(self) -> None:
        """Must use app-container className."""
        assert "app-container" in self.content

    def test_flex_center(self) -> None:
        """Must center content with flexbox."""
        assert "display: 'flex'" in self.content
        assert "justifyContent: 'center'" in self.content
        assert "alignItems: 'center'" in self.content

    def test_min_height(self) -> None:
        """Must set minHeight to 100vh."""
        assert "minHeight: '100vh'" in self.content


# ---------------------------------------------------------------------------
# Dockerfile
# ---------------------------------------------------------------------------


class TestDockerfile:
    """Validate Dockerfile content."""

    @pytest.fixture(autouse=True)
    def _load(self) -> None:
        """Read Dockerfile."""
        self.content: str = _read("Dockerfile")

    def test_base_image(self) -> None:
        """Must use node:20-alpine as base image."""
        assert "FROM node:20-alpine" in self.content

    def test_workdir(self) -> None:
        """Must set WORKDIR to /app."""
        assert "WORKDIR /app" in self.content

    def test_npm_install(self) -> None:
        """Must run npm install."""
        assert "npm install" in self.content

    def test_expose(self) -> None:
        """Must expose port 5173."""
        assert "EXPOSE 5173" in self.content

    def test_cmd(self) -> None:
        """Must run npm run dev as default command."""
        assert "npm" in self.content
        assert "dev" in self.content


# ---------------------------------------------------------------------------
# docker-compose.yml
# ---------------------------------------------------------------------------


class TestDockerCompose:
    """Validate docker-compose.yml content."""

    @pytest.fixture(autouse=True)
    def _load(self) -> None:
        """Read docker-compose.yml."""
        self.content: str = _read("docker-compose.yml")

    def test_has_services(self) -> None:
        """Must define services section."""
        assert "services:" in self.content

    def test_has_app_service(self) -> None:
        """Must define app service."""
        assert "app:" in self.content

    def test_port_mapping(self) -> None:
        """Must map port 5173."""
        assert "5173:5173" in self.content

    def test_volume_mount(self) -> None:
        """Must mount current directory."""
        assert ".:/app" in self.content

    def test_node_modules_volume(self) -> None:
        """Must have anonymous volume for node_modules."""
        assert "/app/node_modules" in self.content
