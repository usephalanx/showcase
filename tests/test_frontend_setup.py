"""Tests to validate the frontend project setup, API layer, and Auth component.

These tests verify that all required files exist with the correct content,
configuration, and structure without needing to run Node.js or a browser.
"""

import json
import os
import re
from pathlib import Path
from typing import Dict, Any

import pytest

# Resolve the frontend directory relative to the project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent
FRONTEND_DIR = PROJECT_ROOT / "frontend"


def read_file(relative_path: str) -> str:
    """Read a file relative to the frontend directory and return its contents."""
    file_path = FRONTEND_DIR / relative_path
    assert file_path.exists(), f"File not found: {file_path}"
    return file_path.read_text(encoding="utf-8")


def load_json(relative_path: str) -> Dict[str, Any]:
    """Load and parse a JSON file relative to the frontend directory."""
    content = read_file(relative_path)
    return json.loads(content)


class TestPackageJson:
    """Validate frontend/package.json dependencies and scripts."""

    def test_package_json_exists(self) -> None:
        """package.json must exist in the frontend directory."""
        assert (FRONTEND_DIR / "package.json").exists()

    def test_package_json_is_valid_json(self) -> None:
        """package.json must be valid JSON."""
        load_json("package.json")

    def test_runtime_dependencies(self) -> None:
        """All required runtime dependencies must be listed."""
        pkg = load_json("package.json")
        deps = pkg.get("dependencies", {})
        required = [
            "react",
            "react-dom",
            "@dnd-kit/core",
            "@dnd-kit/sortable",
            "@dnd-kit/utilities",
            "axios",
        ]
        for dep in required:
            assert dep in deps, f"Missing runtime dependency: {dep}"

    def test_dev_dependencies(self) -> None:
        """All required dev dependencies must be listed."""
        pkg = load_json("package.json")
        dev_deps = pkg.get("devDependencies", {})
        required = [
            "vite",
            "@vitejs/plugin-react",
            "tailwindcss",
            "postcss",
            "autoprefixer",
        ]
        for dep in required:
            assert dep in dev_deps, f"Missing dev dependency: {dep}"

    def test_scripts_defined(self) -> None:
        """Must have dev, build, and preview scripts."""
        pkg = load_json("package.json")
        scripts = pkg.get("scripts", {})
        assert "dev" in scripts
        assert "build" in scripts
        assert "preview" in scripts


class TestViteConfig:
    """Validate frontend/vite.config.js."""

    def test_vite_config_exists(self) -> None:
        """vite.config.js must exist."""
        assert (FRONTEND_DIR / "vite.config.js").exists()

    def test_react_plugin_imported(self) -> None:
        """Must import the React plugin."""
        content = read_file("vite.config.js")
        assert "@vitejs/plugin-react" in content

    def test_react_plugin_used(self) -> None:
        """Must use react() in the plugins array."""
        content = read_file("vite.config.js")
        assert "react()" in content

    def test_proxy_configured(self) -> None:
        """Must proxy /api to localhost:8000."""
        content = read_file("vite.config.js")
        assert "'/api'" in content or '"/api"' in content
        assert "localhost:8000" in content or "127.0.0.1:8000" in content


class TestTailwindConfig:
    """Validate frontend/tailwind.config.js."""

    def test_tailwind_config_exists(self) -> None:
        """tailwind.config.js must exist."""
        assert (FRONTEND_DIR / "tailwind.config.js").exists()

    def test_dark_mode_class_strategy(self) -> None:
        """Dark mode must use 'class' strategy."""
        content = read_file("tailwind.config.js")
        assert "'class'" in content or '"class"' in content

    def test_content_paths_configured(self) -> None:
        """Content paths must include src/**/*.{js,jsx}."""
        content = read_file("tailwind.config.js")
        assert "./src/**/*.{js,jsx}" in content or "src/**/*.{js,jsx}" in content


class TestPostCSSConfig:
    """Validate frontend/postcss.config.js."""

    def test_postcss_config_exists(self) -> None:
        """postcss.config.js must exist."""
        assert (FRONTEND_DIR / "postcss.config.js").exists()

    def test_tailwind_plugin_referenced(self) -> None:
        """Must reference tailwindcss plugin."""
        content = read_file("postcss.config.js")
        assert "tailwindcss" in content

    def test_autoprefixer_plugin_referenced(self) -> None:
        """Must reference autoprefixer plugin."""
        content = read_file("postcss.config.js")
        assert "autoprefixer" in content


class TestIndexHtml:
    """Validate frontend/index.html."""

    def test_index_html_exists(self) -> None:
        """index.html must exist."""
        assert (FRONTEND_DIR / "index.html").exists()

    def test_root_div_present(self) -> None:
        """Must contain a div with id='root'."""
        content = read_file("index.html")
        assert 'id="root"' in content

    def test_dark_class_on_html(self) -> None:
        """html element must have 'dark' class."""
        content = read_file("index.html")
        assert re.search(r'<html[^>]*class="[^"]*dark[^"]*"', content)

    def test_module_script_tag(self) -> None:
        """Must include a module script tag pointing to src/main.jsx."""
        content = read_file("index.html")
        assert 'type="module"' in content
        assert "src/main.jsx" in content


class TestApiLayer:
    """Validate frontend/src/api.js structure and exports."""

    def test_api_js_exists(self) -> None:
        """api.js must exist in src/."""
        assert (FRONTEND_DIR / "src" / "api.js").exists()

    def test_axios_import(self) -> None:
        """Must import axios."""
        content = read_file("src/api.js")
        assert "import axios" in content

    def test_base_url_configured(self) -> None:
        """Must set baseURL to /api."""
        content = read_file("src/api.js")
        assert "baseURL" in content
        assert "/api" in content

    def test_request_interceptor(self) -> None:
        """Must set up a request interceptor for JWT."""
        content = read_file("src/api.js")
        assert "interceptors.request.use" in content
        assert "Bearer" in content
        assert "localStorage" in content

    def test_response_interceptor(self) -> None:
        """Must set up a response interceptor for 401 handling."""
        content = read_file("src/api.js")
        assert "interceptors.response.use" in content
        assert "401" in content

    def test_register_function_exported(self) -> None:
        """Must export a register function."""
        content = read_file("src/api.js")
        assert "export async function register" in content

    def test_login_function_exported(self) -> None:
        """Must export a login function."""
        content = read_file("src/api.js")
        assert "export async function login" in content

    def test_get_boards_function_exported(self) -> None:
        """Must export a getBoards function."""
        content = read_file("src/api.js")
        assert "export async function getBoards" in content

    def test_create_board_function_exported(self) -> None:
        """Must export a createBoard function."""
        content = read_file("src/api.js")
        assert "export async function createBoard" in content

    def test_get_board_function_exported(self) -> None:
        """Must export a getBoard function."""
        content = read_file("src/api.js")
        assert "export async function getBoard" in content

    def test_delete_board_function_exported(self) -> None:
        """Must export a deleteBoard function."""
        content = read_file("src/api.js")
        assert "export async function deleteBoard" in content

    def test_create_card_function_exported(self) -> None:
        """Must export a createCard function."""
        content = read_file("src/api.js")
        assert "export async function createCard" in content

    def test_update_card_function_exported(self) -> None:
        """Must export an updateCard function."""
        content = read_file("src/api.js")
        assert "export async function updateCard" in content

    def test_delete_card_function_exported(self) -> None:
        """Must export a deleteCard function."""
        content = read_file("src/api.js")
        assert "export async function deleteCard" in content

    def test_move_card_function_exported(self) -> None:
        """Must export a moveCard function."""
        content = read_file("src/api.js")
        assert "export async function moveCard" in content

    def test_register_posts_to_auth_register(self) -> None:
        """register function must POST to /auth/register."""
        content = read_file("src/api.js")
        assert "/auth/register" in content

    def test_login_posts_to_auth_login(self) -> None:
        """login function must POST to /auth/login."""
        content = read_file("src/api.js")
        assert "/auth/login" in content

    def test_move_card_endpoint(self) -> None:
        """moveCard must hit /cards/{id}/move endpoint."""
        content = read_file("src/api.js")
        assert "/move" in content
        assert "column_id" in content
        assert "position" in content

    def test_default_export(self) -> None:
        """api instance must be the default export."""
        content = read_file("src/api.js")
        assert "export default api" in content


class TestAuthComponent:
    """Validate frontend/src/components/Auth.jsx structure."""

    def test_auth_jsx_exists(self) -> None:
        """Auth.jsx must exist in src/components/."""
        assert (FRONTEND_DIR / "src" / "components" / "Auth.jsx").exists()

    def test_imports_react(self) -> None:
        """Must import React."""
        content = read_file("src/components/Auth.jsx")
        assert "import React" in content

    def test_imports_api_functions(self) -> None:
        """Must import login and register from api.js."""
        content = read_file("src/components/Auth.jsx")
        assert "login" in content
        assert "register" in content
        assert "from" in content
        assert "api" in content

    def test_uses_usestate(self) -> None:
        """Must use useState for controlled inputs."""
        content = read_file("src/components/Auth.jsx")
        assert "useState" in content

    def test_has_username_input(self) -> None:
        """Must have a username input field."""
        content = read_file("src/components/Auth.jsx")
        assert 'id="username"' in content or "input-username" in content

    def test_has_email_input(self) -> None:
        """Must have an email input field (for register mode)."""
        content = read_file("src/components/Auth.jsx")
        assert 'id="email"' in content or 'type="email"' in content

    def test_has_password_input(self) -> None:
        """Must have a password input field."""
        content = read_file("src/components/Auth.jsx")
        assert 'type="password"' in content

    def test_has_toggle_between_login_and_register(self) -> None:
        """Must have a mechanism to toggle between login and register."""
        content = read_file("src/components/Auth.jsx")
        assert "isLogin" in content or "isRegister" in content or "mode" in content

    def test_error_display(self) -> None:
        """Must have error state and display mechanism."""
        content = read_file("src/components/Auth.jsx")
        assert "error" in content.lower()
        assert "setError" in content

    def test_stores_token_in_localstorage(self) -> None:
        """Must store JWT in localStorage on success."""
        content = read_file("src/components/Auth.jsx")
        assert "localStorage.setItem" in content
        assert "token" in content

    def test_calls_on_auth_callback(self) -> None:
        """Must call onAuth callback prop after authentication."""
        content = read_file("src/components/Auth.jsx")
        assert "onAuth" in content

    def test_form_validation(self) -> None:
        """Must include client-side validation."""
        content = read_file("src/components/Auth.jsx")
        assert "validate" in content or "required" in content.lower()

    def test_dark_theme_classes(self) -> None:
        """Must use dark theme classes (bg-gray-800, bg-gray-900, etc.)."""
        content = read_file("src/components/Auth.jsx")
        assert "bg-gray-800" in content or "bg-gray-900" in content

    def test_loading_state(self) -> None:
        """Must handle loading state during API calls."""
        content = read_file("src/components/Auth.jsx")
        assert "loading" in content or "isLoading" in content

    def test_export_default(self) -> None:
        """Must have a default export."""
        content = read_file("src/components/Auth.jsx")
        assert "export default" in content


class TestAppComponent:
    """Validate frontend/src/App.jsx."""

    def test_app_jsx_exists(self) -> None:
        """App.jsx must exist in src/."""
        assert (FRONTEND_DIR / "src" / "App.jsx").exists()

    def test_imports_auth_component(self) -> None:
        """Must import the Auth component."""
        content = read_file("src/App.jsx")
        assert "Auth" in content

    def test_authentication_state(self) -> None:
        """Must manage authentication state."""
        content = read_file("src/App.jsx")
        assert "isAuthenticated" in content or "authenticated" in content

    def test_checks_localstorage_token(self) -> None:
        """Must check localStorage for existing token on mount."""
        content = read_file("src/App.jsx")
        assert "localStorage" in content
        assert "token" in content


class TestMainEntry:
    """Validate frontend/src/main.jsx."""

    def test_main_jsx_exists(self) -> None:
        """main.jsx must exist in src/."""
        assert (FRONTEND_DIR / "src" / "main.jsx").exists()

    def test_renders_to_root(self) -> None:
        """Must render to the root element."""
        content = read_file("src/main.jsx")
        assert "root" in content
        assert "createRoot" in content

    def test_imports_app(self) -> None:
        """Must import the App component."""
        content = read_file("src/main.jsx")
        assert "App" in content


class TestCSSEntry:
    """Validate frontend/src/index.css."""

    def test_index_css_exists(self) -> None:
        """index.css must exist in src/."""
        assert (FRONTEND_DIR / "src" / "index.css").exists()

    def test_tailwind_directives(self) -> None:
        """Must include all three Tailwind directives."""
        content = read_file("src/index.css")
        assert "@tailwind base" in content
        assert "@tailwind components" in content
        assert "@tailwind utilities" in content
