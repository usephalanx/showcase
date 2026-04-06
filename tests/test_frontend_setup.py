"""Tests to validate the frontend project setup.

Verifies that all required configuration files exist with correct content,
dependencies are listed, and the entry points are properly structured.
"""

import json
import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
FRONTEND_DIR = REPO_ROOT / "frontend"


class TestPackageJson:
    """Tests for package.json configuration."""

    @pytest.fixture()
    def package_json(self) -> dict:
        """Load and return parsed package.json."""
        path = FRONTEND_DIR / "package.json"
        assert path.exists(), "frontend/package.json not found"
        return json.loads(path.read_text(encoding="utf-8"))

    def test_package_json_exists(self) -> None:
        """Verify package.json exists."""
        assert (FRONTEND_DIR / "package.json").exists()

    def test_has_name(self, package_json: dict) -> None:
        """Verify package.json has a name field."""
        assert "name" in package_json

    def test_has_required_dependencies(self, package_json: dict) -> None:
        """Verify all required runtime dependencies are listed."""
        deps = package_json.get("dependencies", {})
        required = [
            "react",
            "react-dom",
            "react-router-dom",
            "react-helmet-async",
            "@dnd-kit/core",
            "@dnd-kit/sortable",
        ]
        for dep in required:
            assert dep in deps, f"Missing dependency: {dep}"

    def test_has_required_dev_dependencies(self, package_json: dict) -> None:
        """Verify all required dev dependencies are listed."""
        dev_deps = package_json.get("devDependencies", {})
        required = [
            "typescript",
            "vite",
            "@vitejs/plugin-react",
        ]
        for dep in required:
            assert dep in dev_deps, f"Missing devDependency: {dep}"

    def test_has_scripts(self, package_json: dict) -> None:
        """Verify essential scripts are defined."""
        scripts = package_json.get("scripts", {})
        assert "dev" in scripts, "Missing 'dev' script"
        assert "build" in scripts, "Missing 'build' script"


class TestViteConfig:
    """Tests for vite.config.ts."""

    def test_vite_config_exists(self) -> None:
        """Verify vite.config.ts exists."""
        assert (FRONTEND_DIR / "vite.config.ts").exists()

    def test_vite_config_has_react_plugin(self) -> None:
        """Verify vite config imports and uses the React plugin."""
        content = (FRONTEND_DIR / "vite.config.ts").read_text(encoding="utf-8")
        assert "@vitejs/plugin-react" in content
        assert "react()" in content

    def test_vite_config_has_proxy(self) -> None:
        """Verify vite config has API proxy configuration."""
        content = (FRONTEND_DIR / "vite.config.ts").read_text(encoding="utf-8")
        assert "proxy" in content
        assert "/api" in content
        assert "localhost:8000" in content or "127.0.0.1:8000" in content


class TestTsConfig:
    """Tests for TypeScript configuration."""

    def test_tsconfig_exists(self) -> None:
        """Verify tsconfig.json exists."""
        assert (FRONTEND_DIR / "tsconfig.json").exists()

    def test_tsconfig_valid_json(self) -> None:
        """Verify tsconfig.json is valid JSON."""
        path = FRONTEND_DIR / "tsconfig.json"
        content = path.read_text(encoding="utf-8")
        parsed = json.loads(content)
        assert "compilerOptions" in parsed

    def test_tsconfig_strict_mode(self) -> None:
        """Verify strict mode is enabled."""
        path = FRONTEND_DIR / "tsconfig.json"
        parsed = json.loads(path.read_text(encoding="utf-8"))
        assert parsed["compilerOptions"].get("strict") is True

    def test_tsconfig_jsx_react(self) -> None:
        """Verify JSX is configured for React."""
        path = FRONTEND_DIR / "tsconfig.json"
        parsed = json.loads(path.read_text(encoding="utf-8"))
        jsx = parsed["compilerOptions"].get("jsx", "")
        assert "react" in jsx.lower()

    def test_tsconfig_node_exists(self) -> None:
        """Verify tsconfig.node.json exists."""
        assert (FRONTEND_DIR / "tsconfig.node.json").exists()


class TestIndexHtml:
    """Tests for index.html."""

    @pytest.fixture()
    def index_html(self) -> str:
        """Load and return index.html content."""
        path = FRONTEND_DIR / "index.html"
        assert path.exists(), "frontend/index.html not found"
        return path.read_text(encoding="utf-8")

    def test_index_html_exists(self) -> None:
        """Verify index.html exists."""
        assert (FRONTEND_DIR / "index.html").exists()

    def test_has_doctype(self, index_html: str) -> None:
        """Verify HTML5 doctype is present."""
        assert "<!doctype html>" in index_html.lower() or "<!DOCTYPE html>" in index_html

    def test_has_lang_attribute(self, index_html: str) -> None:
        """Verify html tag has lang attribute."""
        assert 'lang="en"' in index_html

    def test_has_charset(self, index_html: str) -> None:
        """Verify charset meta tag is present."""
        assert 'charset="UTF-8"' in index_html or 'charset="utf-8"' in index_html

    def test_has_viewport(self, index_html: str) -> None:
        """Verify viewport meta tag is present."""
        assert 'name="viewport"' in index_html

    def test_has_description(self, index_html: str) -> None:
        """Verify description meta tag is present."""
        assert 'name="description"' in index_html

    def test_has_og_tags(self, index_html: str) -> None:
        """Verify Open Graph meta tags are present."""
        assert 'property="og:title"' in index_html
        assert 'property="og:description"' in index_html
        assert 'property="og:type"' in index_html

    def test_has_root_div(self, index_html: str) -> None:
        """Verify root div for React mounting exists."""
        assert 'id="root"' in index_html

    def test_has_module_script(self, index_html: str) -> None:
        """Verify module script tag pointing to main.tsx exists."""
        assert 'type="module"' in index_html
        assert "src/main.tsx" in index_html

    def test_has_noscript(self, index_html: str) -> None:
        """Verify noscript fallback is present."""
        assert "<noscript>" in index_html

    def test_has_canonical_link(self, index_html: str) -> None:
        """Verify canonical link tag is present."""
        assert 'rel="canonical"' in index_html


class TestMainTsx:
    """Tests for src/main.tsx entry point."""

    @pytest.fixture()
    def main_tsx(self) -> str:
        """Load and return main.tsx content."""
        path = FRONTEND_DIR / "src" / "main.tsx"
        assert path.exists(), "frontend/src/main.tsx not found"
        return path.read_text(encoding="utf-8")

    def test_main_tsx_exists(self) -> None:
        """Verify src/main.tsx exists."""
        assert (FRONTEND_DIR / "src" / "main.tsx").exists()

    def test_imports_react(self, main_tsx: str) -> None:
        """Verify React is imported."""
        assert "import React" in main_tsx or "from 'react'" in main_tsx

    def test_imports_react_dom(self, main_tsx: str) -> None:
        """Verify ReactDOM is imported."""
        assert "react-dom" in main_tsx

    def test_imports_browser_router(self, main_tsx: str) -> None:
        """Verify BrowserRouter is imported."""
        assert "BrowserRouter" in main_tsx

    def test_imports_helmet_provider(self, main_tsx: str) -> None:
        """Verify HelmetProvider is imported."""
        assert "HelmetProvider" in main_tsx

    def test_uses_browser_router(self, main_tsx: str) -> None:
        """Verify BrowserRouter wraps the app."""
        assert "<BrowserRouter>" in main_tsx

    def test_uses_helmet_provider(self, main_tsx: str) -> None:
        """Verify HelmetProvider wraps the app."""
        assert "<HelmetProvider>" in main_tsx

    def test_uses_strict_mode(self, main_tsx: str) -> None:
        """Verify React.StrictMode is used."""
        assert "StrictMode" in main_tsx

    def test_imports_app(self, main_tsx: str) -> None:
        """Verify App component is imported."""
        assert "import App" in main_tsx or "from './App'" in main_tsx

    def test_creates_root(self, main_tsx: str) -> None:
        """Verify createRoot is called."""
        assert "createRoot" in main_tsx

    def test_provider_nesting_order(self, main_tsx: str) -> None:
        """Verify HelmetProvider wraps BrowserRouter (correct nesting)."""
        helmet_pos = main_tsx.index("<HelmetProvider>")
        router_pos = main_tsx.index("<BrowserRouter>")
        assert helmet_pos < router_pos, (
            "HelmetProvider should wrap BrowserRouter"
        )


class TestAppTsx:
    """Tests for src/App.tsx."""

    @pytest.fixture()
    def app_tsx(self) -> str:
        """Load and return App.tsx content."""
        path = FRONTEND_DIR / "src" / "App.tsx"
        assert path.exists(), "frontend/src/App.tsx not found"
        return path.read_text(encoding="utf-8")

    def test_app_tsx_exists(self) -> None:
        """Verify src/App.tsx exists."""
        assert (FRONTEND_DIR / "src" / "App.tsx").exists()

    def test_imports_routes(self, app_tsx: str) -> None:
        """Verify Routes and Route are imported from react-router-dom."""
        assert "Routes" in app_tsx
        assert "Route" in app_tsx
        assert "react-router-dom" in app_tsx

    def test_imports_helmet(self, app_tsx: str) -> None:
        """Verify Helmet is imported from react-helmet-async."""
        assert "Helmet" in app_tsx
        assert "react-helmet-async" in app_tsx

    def test_has_routes(self, app_tsx: str) -> None:
        """Verify route definitions exist."""
        assert "<Routes>" in app_tsx
        assert "<Route" in app_tsx

    def test_exports_default(self, app_tsx: str) -> None:
        """Verify App is exported as default."""
        assert "export default App" in app_tsx

    def test_has_catch_all_route(self, app_tsx: str) -> None:
        """Verify a catch-all (*) route exists for 404."""
        assert 'path="*"' in app_tsx


class TestViteEnvDts:
    """Tests for vite-env.d.ts."""

    def test_vite_env_exists(self) -> None:
        """Verify vite-env.d.ts exists."""
        assert (FRONTEND_DIR / "src" / "vite-env.d.ts").exists()

    def test_vite_env_references_vite(self) -> None:
        """Verify vite-env.d.ts references vite/client."""
        content = (FRONTEND_DIR / "src" / "vite-env.d.ts").read_text(encoding="utf-8")
        assert "vite/client" in content
