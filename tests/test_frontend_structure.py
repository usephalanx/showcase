"""Tests to verify the frontend project structure and file contents.

These tests ensure that all required frontend files exist and contain
the expected configuration and code patterns.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

# Root of the frontend project relative to the repository root.
FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"


class TestPackageJson:
    """Tests for package.json contents."""

    @pytest.fixture()
    def pkg(self) -> dict:
        """Load and return the parsed package.json."""
        path = FRONTEND_DIR / "package.json"
        assert path.exists(), "package.json must exist"
        return json.loads(path.read_text(encoding="utf-8"))

    def test_name(self, pkg: dict) -> None:
        """Package name must be 'hello-world-app'."""
        assert pkg["name"] == "hello-world-app"

    def test_version(self, pkg: dict) -> None:
        """Package version must be '1.0.0'."""
        assert pkg["version"] == "1.0.0"

    def test_has_react_dependency(self, pkg: dict) -> None:
        """React must be listed as a dependency."""
        assert "react" in pkg["dependencies"]

    def test_has_react_dom_dependency(self, pkg: dict) -> None:
        """React-DOM must be listed as a dependency."""
        assert "react-dom" in pkg["dependencies"]

    def test_has_typescript_devdep(self, pkg: dict) -> None:
        """TypeScript must be listed as a devDependency."""
        assert "typescript" in pkg["devDependencies"]

    def test_has_vite_devdep(self, pkg: dict) -> None:
        """Vite must be listed as a devDependency."""
        assert "vite" in pkg["devDependencies"]

    def test_has_vite_react_plugin_devdep(self, pkg: dict) -> None:
        """@vitejs/plugin-react must be listed as a devDependency."""
        assert "@vitejs/plugin-react" in pkg["devDependencies"]

    def test_has_types_react_devdep(self, pkg: dict) -> None:
        """@types/react must be listed as a devDependency."""
        assert "@types/react" in pkg["devDependencies"]

    def test_has_types_react_dom_devdep(self, pkg: dict) -> None:
        """@types/react-dom must be listed as a devDependency."""
        assert "@types/react-dom" in pkg["devDependencies"]

    def test_dev_script(self, pkg: dict) -> None:
        """The 'dev' script must invoke vite."""
        assert pkg["scripts"]["dev"] == "vite"

    def test_build_script(self, pkg: dict) -> None:
        """The 'build' script must run tsc then vite build."""
        assert pkg["scripts"]["build"] == "tsc && vite build"

    def test_preview_script(self, pkg: dict) -> None:
        """The 'preview' script must invoke vite preview."""
        assert pkg["scripts"]["preview"] == "vite preview"


class TestTsConfig:
    """Tests for tsconfig.json contents."""

    @pytest.fixture()
    def tsconfig(self) -> dict:
        """Load and return the parsed tsconfig.json."""
        path = FRONTEND_DIR / "tsconfig.json"
        assert path.exists(), "tsconfig.json must exist"
        return json.loads(path.read_text(encoding="utf-8"))

    def test_strict_enabled(self, tsconfig: dict) -> None:
        """Strict mode must be enabled."""
        assert tsconfig["compilerOptions"]["strict"] is True

    def test_jsx_react_jsx(self, tsconfig: dict) -> None:
        """JSX must be set to 'react-jsx'."""
        assert tsconfig["compilerOptions"]["jsx"] == "react-jsx"

    def test_target(self, tsconfig: dict) -> None:
        """Target must be ES2020."""
        assert tsconfig["compilerOptions"]["target"] == "ES2020"

    def test_module(self, tsconfig: dict) -> None:
        """Module must be ESNext."""
        assert tsconfig["compilerOptions"]["module"] == "ESNext"

    def test_module_resolution(self, tsconfig: dict) -> None:
        """Module resolution must be 'bundler'."""
        assert tsconfig["compilerOptions"]["moduleResolution"] == "bundler"

    def test_include_src(self, tsconfig: dict) -> None:
        """The include array must contain 'src'."""
        assert "src" in tsconfig["include"]

    def test_exclude_node_modules(self, tsconfig: dict) -> None:
        """The exclude array must contain 'node_modules'."""
        assert "node_modules" in tsconfig["exclude"]


class TestViteConfig:
    """Tests for vite.config.ts contents."""

    @pytest.fixture()
    def content(self) -> str:
        """Read and return the vite.config.ts file content."""
        path = FRONTEND_DIR / "vite.config.ts"
        assert path.exists(), "vite.config.ts must exist"
        return path.read_text(encoding="utf-8")

    def test_imports_define_config(self, content: str) -> None:
        """Must import defineConfig from vite."""
        assert "defineConfig" in content

    def test_imports_react_plugin(self, content: str) -> None:
        """Must import the React plugin."""
        assert "@vitejs/plugin-react" in content

    def test_uses_react_plugin(self, content: str) -> None:
        """Must invoke the react() plugin."""
        assert "react()" in content


class TestIndexHtml:
    """Tests for the Vite entry HTML file."""

    @pytest.fixture()
    def content(self) -> str:
        """Read and return the index.html file content."""
        path = FRONTEND_DIR / "index.html"
        assert path.exists(), "index.html must exist"
        return path.read_text(encoding="utf-8")

    def test_has_root_div(self, content: str) -> None:
        """Must contain a div with id='root'."""
        assert 'id="root"' in content

    def test_has_module_script(self, content: str) -> None:
        """Must contain a module script pointing to main.tsx."""
        assert 'type="module"' in content
        assert 'src="/src/main.tsx"' in content

    def test_has_charset(self, content: str) -> None:
        """Must declare UTF-8 charset."""
        assert 'charset="UTF-8"' in content

    def test_has_viewport_meta(self, content: str) -> None:
        """Must include viewport meta tag."""
        assert 'name="viewport"' in content

    def test_has_title(self, content: str) -> None:
        """Must have the correct page title."""
        assert "<title>Hello World App</title>" in content

    def test_lang_attribute(self, content: str) -> None:
        """Must set lang='en' on the html element."""
        assert 'lang="en"' in content


class TestMainTsx:
    """Tests for the React entry point."""

    @pytest.fixture()
    def content(self) -> str:
        """Read and return the main.tsx file content."""
        path = FRONTEND_DIR / "src" / "main.tsx"
        assert path.exists(), "src/main.tsx must exist"
        return path.read_text(encoding="utf-8")

    def test_imports_react(self, content: str) -> None:
        """Must import React."""
        assert "import React" in content

    def test_imports_react_dom(self, content: str) -> None:
        """Must import ReactDOM."""
        assert "import ReactDOM" in content

    def test_imports_app(self, content: str) -> None:
        """Must import the App component."""
        assert "import App" in content

    def test_creates_root(self, content: str) -> None:
        """Must call createRoot."""
        assert "createRoot" in content

    def test_strict_mode(self, content: str) -> None:
        """Must wrap in React.StrictMode."""
        assert "StrictMode" in content

    def test_targets_root_element(self, content: str) -> None:
        """Must target the 'root' DOM element."""
        assert "getElementById('root')" in content


class TestAppTsx:
    """Tests for the App root component."""

    @pytest.fixture()
    def content(self) -> str:
        """Read and return the App.tsx file content."""
        path = FRONTEND_DIR / "src" / "App.tsx"
        assert path.exists(), "src/App.tsx must exist"
        return path.read_text(encoding="utf-8")

    def test_imports_hello_page(self, content: str) -> None:
        """Must import HelloPage component."""
        assert "import HelloPage" in content

    def test_renders_hello_page(self, content: str) -> None:
        """Must render <HelloPage /> in JSX."""
        assert "<HelloPage" in content

    def test_exports_default(self, content: str) -> None:
        """Must have a default export."""
        assert "export default App" in content

    def test_has_app_classname(self, content: str) -> None:
        """Must use className='app' on the wrapper div."""
        assert 'className="app"' in content


class TestHelloPageTsx:
    """Tests for the HelloPage component."""

    @pytest.fixture()
    def content(self) -> str:
        """Read and return the HelloPage.tsx file content."""
        path = FRONTEND_DIR / "src" / "pages" / "HelloPage.tsx"
        assert path.exists(), "src/pages/HelloPage.tsx must exist"
        return path.read_text(encoding="utf-8")

    def test_has_hello_world_text(self, content: str) -> None:
        """Must contain the exact text 'Hello World'."""
        assert "Hello World" in content

    def test_has_data_testid(self, content: str) -> None:
        """Must include data-testid='hello-heading' for testability."""
        assert 'data-testid="hello-heading"' in content

    def test_uses_main_element(self, content: str) -> None:
        """Must use a <main> semantic element."""
        assert "<main>" in content

    def test_uses_h1(self, content: str) -> None:
        """Must use an <h1> heading element."""
        assert "<h1" in content

    def test_exports_default(self, content: str) -> None:
        """Must have a default export."""
        assert "export default HelloPage" in content


class TestAppCss:
    """Tests for the global stylesheet."""

    @pytest.fixture()
    def content(self) -> str:
        """Read and return the App.css file content."""
        path = FRONTEND_DIR / "src" / "App.css"
        assert path.exists(), "src/App.css must exist"
        return path.read_text(encoding="utf-8")

    def test_has_box_sizing(self, content: str) -> None:
        """Must set box-sizing: border-box."""
        assert "box-sizing" in content

    def test_has_font_family(self, content: str) -> None:
        """Must set a font-family on body."""
        assert "font-family" in content

    def test_has_text_align_center(self, content: str) -> None:
        """Must center text in the app container."""
        assert "text-align: center" in content


class TestViteEnvDts:
    """Tests for the Vite type declaration file."""

    @pytest.fixture()
    def content(self) -> str:
        """Read and return the vite-env.d.ts file content."""
        path = FRONTEND_DIR / "src" / "vite-env.d.ts"
        assert path.exists(), "src/vite-env.d.ts must exist"
        return path.read_text(encoding="utf-8")

    def test_references_vite_client(self, content: str) -> None:
        """Must reference vite/client types."""
        assert 'vite/client' in content


class TestDocumentation:
    """Tests for documentation files."""

    def test_architecture_md_exists(self) -> None:
        """ARCHITECTURE.md must exist at the repo root."""
        path = Path(__file__).resolve().parent.parent / "ARCHITECTURE.md"
        assert path.exists(), "ARCHITECTURE.md must exist"

    def test_running_md_exists(self) -> None:
        """RUNNING.md must exist at the repo root."""
        path = Path(__file__).resolve().parent.parent / "RUNNING.md"
        assert path.exists(), "RUNNING.md must exist"

    def test_architecture_mentions_react(self) -> None:
        """ARCHITECTURE.md must mention React."""
        path = Path(__file__).resolve().parent.parent / "ARCHITECTURE.md"
        content = path.read_text(encoding="utf-8")
        assert "React" in content

    def test_architecture_mentions_vite(self) -> None:
        """ARCHITECTURE.md must mention Vite."""
        path = Path(__file__).resolve().parent.parent / "ARCHITECTURE.md"
        content = path.read_text(encoding="utf-8")
        assert "Vite" in content

    def test_running_mentions_npm_install(self) -> None:
        """RUNNING.md must mention npm install."""
        path = Path(__file__).resolve().parent.parent / "RUNNING.md"
        content = path.read_text(encoding="utf-8")
        assert "npm install" in content
