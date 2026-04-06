"""Tests to validate that architecture documentation is complete and well-structured."""

import os
import pathlib

import pytest

ROOT_DIR = pathlib.Path(__file__).resolve().parent.parent


def _read_file(filename: str) -> str:
    """Read a file from the project root and return its content."""
    filepath = ROOT_DIR / filename
    assert filepath.exists(), f"{filename} does not exist at {filepath}"
    content = filepath.read_text(encoding="utf-8")
    return content


class TestArchitectureMd:
    """Tests for ARCHITECTURE.md completeness."""

    def test_architecture_md_exists(self) -> None:
        """Verify ARCHITECTURE.md exists at the repo root and is non-empty."""
        content = _read_file("ARCHITECTURE.md")
        assert len(content.strip()) > 0, "ARCHITECTURE.md is empty"

    def test_architecture_has_all_sections(self) -> None:
        """Parse ARCHITECTURE.md and assert all 9 required H2 sections exist."""
        content = _read_file("ARCHITECTURE.md")
        required_sections = [
            "Tech Stack",
            "Data Models",
            "API Endpoints",
            "URL Structure",
            "Meta Tag Strategy",
            "Frontend Component Tree",
            "Database Schema",
            "Directory Structure",
            "Deployment",
        ]
        for section in required_sections:
            assert section in content, (
                f"ARCHITECTURE.md is missing required section: '{section}'"
            )

    def test_architecture_has_board_model(self) -> None:
        """Verify the Board data model is documented."""
        content = _read_file("ARCHITECTURE.md")
        assert "Board" in content
        assert "slug" in content.lower()

    def test_architecture_has_card_model(self) -> None:
        """Verify the Card data model is documented."""
        content = _read_file("ARCHITECTURE.md")
        assert "Card" in content
        assert "column_id" in content

    def test_architecture_has_tag_model(self) -> None:
        """Verify the Tag data model is documented."""
        content = _read_file("ARCHITECTURE.md")
        assert "Tag" in content
        assert "card_tags" in content.lower() or "CardTag" in content

    def test_architecture_has_api_methods(self) -> None:
        """Verify API endpoint definitions include HTTP methods."""
        content = _read_file("ARCHITECTURE.md")
        for method in ["GET", "POST", "PUT", "DELETE"]:
            assert method in content, f"Missing HTTP method {method} in API docs"

    def test_architecture_has_sql_schema(self) -> None:
        """Verify the SQL schema section contains CREATE TABLE statements."""
        content = _read_file("ARCHITECTURE.md")
        assert "CREATE TABLE" in content

    def test_architecture_has_slug_strategy(self) -> None:
        """Verify slug generation strategy is documented."""
        content = _read_file("ARCHITECTURE.md")
        assert "Slug Generation" in content or "slug generation" in content.lower()

    def test_architecture_has_reordering_algorithm(self) -> None:
        """Verify card reordering algorithm is documented."""
        content = _read_file("ARCHITECTURE.md")
        assert "reorder" in content.lower() or "position" in content.lower()


class TestRunningMd:
    """Tests for RUNNING.md completeness."""

    def test_running_md_exists(self) -> None:
        """Verify RUNNING.md exists and is non-empty."""
        content = _read_file("RUNNING.md")
        assert len(content.strip()) > 0, "RUNNING.md is empty"

    def test_running_md_has_docker_instructions(self) -> None:
        """Verify RUNNING.md includes Docker instructions."""
        content = _read_file("RUNNING.md")
        assert "docker" in content.lower()

    def test_running_md_has_urls(self) -> None:
        """Verify RUNNING.md includes access URLs."""
        content = _read_file("RUNNING.md")
        assert "localhost" in content


class TestFrontendSetup:
    """Tests for frontend project configuration files."""

    def test_package_json_exists(self) -> None:
        """Verify package.json exists in the frontend directory."""
        content = _read_file("frontend/package.json")
        assert len(content.strip()) > 0

    def test_package_json_has_required_dependencies(self) -> None:
        """Verify all required dependencies are listed in package.json."""
        import json

        content = _read_file("frontend/package.json")
        pkg = json.loads(content)
        deps = pkg.get("dependencies", {})
        dev_deps = pkg.get("devDependencies", {})
        all_deps = {**deps, **dev_deps}

        required = [
            "react",
            "react-dom",
            "react-router-dom",
            "react-helmet-async",
            "axios",
            "tailwindcss",
            "@headlessui/react",
        ]
        for dep in required:
            assert dep in all_deps, f"Missing dependency: {dep}"

    def test_package_json_has_dnd_dependency(self) -> None:
        """Verify drag-and-drop library is included."""
        import json

        content = _read_file("frontend/package.json")
        pkg = json.loads(content)
        deps = pkg.get("dependencies", {})
        has_dnd = (
            "@hello-pangea/dnd" in deps
            or "react-beautiful-dnd" in deps
            or "@dnd-kit/core" in deps
        )
        assert has_dnd, "Missing drag-and-drop dependency"

    def test_vite_config_exists(self) -> None:
        """Verify vite.config.ts exists."""
        content = _read_file("frontend/vite.config.ts")
        assert "proxy" in content, "vite.config.ts should contain proxy configuration"
        assert "8000" in content, "Proxy should target backend port 8000"

    def test_tsconfig_exists(self) -> None:
        """Verify tsconfig.json exists and has strict mode."""
        content = _read_file("frontend/tsconfig.json")
        assert '"strict": true' in content or '"strict":true' in content

    def test_tailwind_config_exists(self) -> None:
        """Verify tailwind.config.js exists with custom color palette."""
        content = _read_file("frontend/tailwind.config.js")
        assert "primary" in content
        assert "colors" in content

    def test_postcss_config_exists(self) -> None:
        """Verify postcss.config.js exists."""
        content = _read_file("frontend/postcss.config.js")
        assert "tailwindcss" in content
        assert "autoprefixer" in content

    def test_index_html_exists(self) -> None:
        """Verify index.html exists with proper meta tags."""
        content = _read_file("frontend/index.html")
        assert "<meta charset" in content.lower() or 'charset="UTF-8"' in content
        assert "viewport" in content
        assert "og:title" in content
        assert "twitter:card" in content
        assert 'id="root"' in content

    def test_main_tsx_exists(self) -> None:
        """Verify main.tsx entry point exists with required providers."""
        content = _read_file("frontend/src/main.tsx")
        assert "BrowserRouter" in content
        assert "HelmetProvider" in content
        assert "ReactDOM" in content

    def test_app_tsx_exists(self) -> None:
        """Verify App.tsx exists with routing setup."""
        content = _read_file("frontend/src/App.tsx")
        assert "Routes" in content or "Route" in content

    def test_index_css_has_tailwind_directives(self) -> None:
        """Verify index.css has Tailwind directives."""
        content = _read_file("frontend/src/index.css")
        assert "@tailwind base" in content
        assert "@tailwind components" in content
        assert "@tailwind utilities" in content

    def test_types_index_exists(self) -> None:
        """Verify TypeScript type definitions exist."""
        content = _read_file("frontend/src/types/index.ts")
        assert "Board" in content
        assert "Card" in content
        assert "Tag" in content
        assert "Column" in content

    def test_api_client_exists(self) -> None:
        """Verify API client module exists."""
        content = _read_file("frontend/src/api/client.ts")
        assert "axios" in content
        assert "/api" in content
