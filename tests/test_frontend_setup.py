"""Tests to validate the frontend project scaffolding.

These tests verify that all required configuration files exist, contain
the expected content, and are structurally correct.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

import pytest

# Resolve project root (one level up from tests/)
PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent


def _read_text(relative_path: str) -> str:
    """Read a file relative to the project root and return its text."""
    full_path = PROJECT_ROOT / relative_path
    assert full_path.exists(), f"{relative_path} does not exist"
    return full_path.read_text(encoding="utf-8")


def _load_json(relative_path: str) -> Dict[str, Any]:
    """Load and parse a JSON file relative to the project root."""
    content = _read_text(relative_path)
    return json.loads(content)


# ---------------------------------------------------------------------------
# package.json
# ---------------------------------------------------------------------------


class TestPackageJson:
    """Validate package.json structure and content."""

    @pytest.fixture()
    def pkg(self) -> Dict[str, Any]:
        """Load package.json as a dictionary."""
        return _load_json("package.json")

    def test_name(self, pkg: Dict[str, Any]) -> None:
        """Package name should be 'hello-world-app'."""
        assert pkg["name"] == "hello-world-app"

    def test_version(self, pkg: Dict[str, Any]) -> None:
        """Package version should be '1.0.0'."""
        assert pkg["version"] == "1.0.0"

    def test_private(self, pkg: Dict[str, Any]) -> None:
        """Package should be marked private."""
        assert pkg["private"] is True

    def test_type_module(self, pkg: Dict[str, Any]) -> None:
        """Package type should be 'module' for ESM."""
        assert pkg["type"] == "module"

    def test_scripts_dev(self, pkg: Dict[str, Any]) -> None:
        """'dev' script should run vite."""
        assert pkg["scripts"]["dev"] == "vite"

    def test_scripts_build(self, pkg: Dict[str, Any]) -> None:
        """'build' script should type-check then build."""
        assert pkg["scripts"]["build"] == "tsc && vite build"

    def test_scripts_preview(self, pkg: Dict[str, Any]) -> None:
        """'preview' script should run vite preview."""
        assert pkg["scripts"]["preview"] == "vite preview"

    def test_react_dependency(self, pkg: Dict[str, Any]) -> None:
        """React should be listed as a dependency."""
        assert "react" in pkg["dependencies"]

    def test_react_dom_dependency(self, pkg: Dict[str, Any]) -> None:
        """React DOM should be listed as a dependency."""
        assert "react-dom" in pkg["dependencies"]

    def test_typescript_dev_dependency(self, pkg: Dict[str, Any]) -> None:
        """TypeScript should be a dev dependency."""
        assert "typescript" in pkg["devDependencies"]

    def test_vite_dev_dependency(self, pkg: Dict[str, Any]) -> None:
        """Vite should be a dev dependency."""
        assert "vite" in pkg["devDependencies"]

    def test_vitejs_plugin_react(self, pkg: Dict[str, Any]) -> None:
        """@vitejs/plugin-react should be a dev dependency."""
        assert "@vitejs/plugin-react" in pkg["devDependencies"]

    def test_types_react(self, pkg: Dict[str, Any]) -> None:
        """@types/react should be a dev dependency."""
        assert "@types/react" in pkg["devDependencies"]

    def test_types_react_dom(self, pkg: Dict[str, Any]) -> None:
        """@types/react-dom should be a dev dependency."""
        assert "@types/react-dom" in pkg["devDependencies"]


# ---------------------------------------------------------------------------
# tsconfig.json
# ---------------------------------------------------------------------------


class TestTsconfigJson:
    """Validate tsconfig.json structure and content."""

    @pytest.fixture()
    def tsconfig(self) -> Dict[str, Any]:
        """Load tsconfig.json as a dictionary."""
        return _load_json("tsconfig.json")

    def test_target(self, tsconfig: Dict[str, Any]) -> None:
        """Target should be ES2020."""
        assert tsconfig["compilerOptions"]["target"] == "ES2020"

    def test_module(self, tsconfig: Dict[str, Any]) -> None:
        """Module should be ESNext."""
        assert tsconfig["compilerOptions"]["module"] == "ESNext"

    def test_module_resolution(self, tsconfig: Dict[str, Any]) -> None:
        """Module resolution should be 'bundler'."""
        assert tsconfig["compilerOptions"]["moduleResolution"] == "bundler"

    def test_jsx(self, tsconfig: Dict[str, Any]) -> None:
        """JSX should be 'react-jsx'."""
        assert tsconfig["compilerOptions"]["jsx"] == "react-jsx"

    def test_strict(self, tsconfig: Dict[str, Any]) -> None:
        """Strict mode should be enabled."""
        assert tsconfig["compilerOptions"]["strict"] is True

    def test_skip_lib_check(self, tsconfig: Dict[str, Any]) -> None:
        """skipLibCheck should be true."""
        assert tsconfig["compilerOptions"]["skipLibCheck"] is True

    def test_include(self, tsconfig: Dict[str, Any]) -> None:
        """Include should contain 'src'."""
        assert "src" in tsconfig["include"]

    def test_references(self, tsconfig: Dict[str, Any]) -> None:
        """References should include tsconfig.node.json."""
        paths = [ref["path"] for ref in tsconfig["references"]]
        assert "./tsconfig.node.json" in paths


# ---------------------------------------------------------------------------
# tsconfig.node.json
# ---------------------------------------------------------------------------


class TestTsconfigNodeJson:
    """Validate tsconfig.node.json structure and content."""

    @pytest.fixture()
    def tsconfig_node(self) -> Dict[str, Any]:
        """Load tsconfig.node.json as a dictionary."""
        return _load_json("tsconfig.node.json")

    def test_composite(self, tsconfig_node: Dict[str, Any]) -> None:
        """Composite should be true."""
        assert tsconfig_node["compilerOptions"]["composite"] is True

    def test_include_vite_config(self, tsconfig_node: Dict[str, Any]) -> None:
        """Include should contain 'vite.config.ts'."""
        assert "vite.config.ts" in tsconfig_node["include"]


# ---------------------------------------------------------------------------
# vite.config.ts
# ---------------------------------------------------------------------------


class TestViteConfig:
    """Validate vite.config.ts content."""

    @pytest.fixture()
    def content(self) -> str:
        """Read vite.config.ts content."""
        return _read_text("vite.config.ts")

    def test_imports_define_config(self, content: str) -> None:
        """Should import defineConfig from vite."""
        assert "defineConfig" in content
        assert "from 'vite'" in content

    def test_imports_react_plugin(self, content: str) -> None:
        """Should import react plugin."""
        assert "@vitejs/plugin-react" in content

    def test_uses_react_plugin(self, content: str) -> None:
        """Should use react() in plugins array."""
        assert "react()" in content

    def test_server_port(self, content: str) -> None:
        """Should configure server port to 5173."""
        assert "5173" in content


# ---------------------------------------------------------------------------
# index.html
# ---------------------------------------------------------------------------


class TestIndexHtml:
    """Validate index.html content."""

    @pytest.fixture()
    def content(self) -> str:
        """Read index.html content."""
        return _read_text("index.html")

    def test_doctype(self, content: str) -> None:
        """Should start with HTML5 doctype."""
        assert content.strip().lower().startswith("<!doctype html>")

    def test_lang_en(self, content: str) -> None:
        """Should have lang='en' attribute."""
        assert 'lang="en"' in content

    def test_charset(self, content: str) -> None:
        """Should set charset to UTF-8."""
        assert 'charset="UTF-8"' in content

    def test_viewport(self, content: str) -> None:
        """Should include a viewport meta tag."""
        assert "viewport" in content

    def test_title(self, content: str) -> None:
        """Title should be 'Hello World'."""
        assert "<title>Hello World</title>" in content

    def test_root_div(self, content: str) -> None:
        """Should have a div with id='root'."""
        assert 'id="root"' in content

    def test_script_module(self, content: str) -> None:
        """Should have a module script tag pointing to /src/main.tsx."""
        assert 'type="module"' in content
        assert 'src="/src/main.tsx"' in content


# ---------------------------------------------------------------------------
# src/main.tsx
# ---------------------------------------------------------------------------


class TestMainTsx:
    """Validate src/main.tsx content."""

    @pytest.fixture()
    def content(self) -> str:
        """Read src/main.tsx content."""
        return _read_text("src/main.tsx")

    def test_imports_react(self, content: str) -> None:
        """Should import React."""
        assert "import React" in content

    def test_imports_react_dom(self, content: str) -> None:
        """Should import ReactDOM."""
        assert "import ReactDOM" in content or "react-dom/client" in content

    def test_imports_app(self, content: str) -> None:
        """Should import App component."""
        assert "import App" in content

    def test_create_root(self, content: str) -> None:
        """Should call createRoot."""
        assert "createRoot" in content

    def test_root_element(self, content: str) -> None:
        """Should target the 'root' element."""
        assert "getElementById('root')" in content or 'getElementById("root")' in content

    def test_strict_mode(self, content: str) -> None:
        """Should use React.StrictMode."""
        assert "StrictMode" in content


# ---------------------------------------------------------------------------
# src/App.tsx
# ---------------------------------------------------------------------------


class TestAppTsx:
    """Validate src/App.tsx content."""

    @pytest.fixture()
    def content(self) -> str:
        """Read src/App.tsx content."""
        return _read_text("src/App.tsx")

    def test_imports_css(self, content: str) -> None:
        """Should import App.css."""
        assert "./App.css" in content

    def test_function_component(self, content: str) -> None:
        """Should define an App function component."""
        assert "function App" in content

    def test_hello_world(self, content: str) -> None:
        """Should render 'Hello World'."""
        assert "Hello World" in content

    def test_export_default(self, content: str) -> None:
        """Should export App as default."""
        assert "export default App" in content

    def test_class_name_app(self, content: str) -> None:
        """Should have className='app'."""
        assert 'className="app"' in content or "className='app'" in content


# ---------------------------------------------------------------------------
# src/App.css
# ---------------------------------------------------------------------------


class TestAppCss:
    """Validate src/App.css content."""

    @pytest.fixture()
    def content(self) -> str:
        """Read src/App.css content."""
        return _read_text("src/App.css")

    def test_app_selector(self, content: str) -> None:
        """Should have a .app selector."""
        assert ".app" in content

    def test_flex_display(self, content: str) -> None:
        """Should use flexbox for centering."""
        assert "display: flex" in content

    def test_justify_content_center(self, content: str) -> None:
        """Should center horizontally."""
        assert "justify-content: center" in content

    def test_align_items_center(self, content: str) -> None:
        """Should center vertically."""
        assert "align-items: center" in content

    def test_min_height(self, content: str) -> None:
        """Should have min-height: 100vh."""
        assert "min-height: 100vh" in content

    def test_font_family(self, content: str) -> None:
        """Should set font-family to sans-serif."""
        assert "font-family: sans-serif" in content


# ---------------------------------------------------------------------------
# src/vite-env.d.ts
# ---------------------------------------------------------------------------


class TestViteEnvDts:
    """Validate src/vite-env.d.ts content."""

    @pytest.fixture()
    def content(self) -> str:
        """Read src/vite-env.d.ts content."""
        return _read_text("src/vite-env.d.ts")

    def test_triple_slash_reference(self, content: str) -> None:
        """Should have a triple-slash reference to vite/client."""
        assert '/// <reference types="vite/client" />' in content


# ---------------------------------------------------------------------------
# File existence checks
# ---------------------------------------------------------------------------


class TestFileExistence:
    """Ensure all scaffolding files exist."""

    @pytest.mark.parametrize(
        "path",
        [
            "package.json",
            "tsconfig.json",
            "tsconfig.node.json",
            "vite.config.ts",
            "index.html",
            "src/main.tsx",
            "src/App.tsx",
            "src/App.css",
            "src/vite-env.d.ts",
            "ARCHITECTURE.md",
        ],
    )
    def test_file_exists(self, path: str) -> None:
        """Verify that the scaffolding file exists."""
        full_path = PROJECT_ROOT / path
        assert full_path.exists(), f"Expected file not found: {path}"
