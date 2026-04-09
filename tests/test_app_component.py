"""Python tests verifying file structure and content of the React+Vite app.

These tests validate that all expected project files exist and contain
the required content, without needing Node.js or npm installed.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import List

import pytest

# Repository root is two levels up from this test file (tests/ -> root)
ROOT: Path = Path(__file__).resolve().parent.parent


class TestProjectStructure:
    """Verify that all required project files exist."""

    REQUIRED_FILES: List[str] = [
        "RUNNING.md",
        "package.json",
        "tsconfig.json",
        "vite.config.ts",
        "index.html",
        "src/main.tsx",
        "src/App.tsx",
        "src/App.css",
        "src/setupTests.ts",
        "src/App.test.tsx",
    ]

    @pytest.mark.parametrize("filepath", REQUIRED_FILES)
    def test_file_exists(self, filepath: str) -> None:
        """Each required project file must exist."""
        assert (ROOT / filepath).is_file(), f"Missing file: {filepath}"


class TestRunningMd:
    """Verify RUNNING.md content."""

    @pytest.fixture()
    def content(self) -> str:
        """Read RUNNING.md content."""
        return (ROOT / "RUNNING.md").read_text(encoding="utf-8")

    def test_contains_npm_install(self, content: str) -> None:
        """RUNNING.md must document npm install."""
        assert "npm install" in content

    def test_contains_npm_run_dev(self, content: str) -> None:
        """RUNNING.md must document npm run dev."""
        assert "npm run dev" in content

    def test_contains_npm_run_build(self, content: str) -> None:
        """RUNNING.md must document npm run build."""
        assert "npm run build" in content

    def test_contains_npm_run_preview(self, content: str) -> None:
        """RUNNING.md must document npm run preview."""
        assert "npm run preview" in content

    def test_contains_localhost_5173(self, content: str) -> None:
        """RUNNING.md must document the default dev server URL."""
        assert "localhost:5173" in content

    def test_contains_team_brief(self, content: str) -> None:
        """RUNNING.md must contain the TEAM_BRIEF section."""
        assert "## TEAM_BRIEF" in content


class TestPackageJson:
    """Verify package.json content."""

    @pytest.fixture()
    def pkg(self) -> dict:
        """Parse package.json."""
        text = (ROOT / "package.json").read_text(encoding="utf-8")
        return json.loads(text)

    def test_has_dev_script(self, pkg: dict) -> None:
        """package.json must define a 'dev' script using vite."""
        assert "dev" in pkg.get("scripts", {})
        assert "vite" in pkg["scripts"]["dev"]

    def test_has_build_script(self, pkg: dict) -> None:
        """package.json must define a 'build' script."""
        assert "build" in pkg.get("scripts", {})

    def test_has_preview_script(self, pkg: dict) -> None:
        """package.json must define a 'preview' script."""
        assert "preview" in pkg.get("scripts", {})

    def test_has_react_dependency(self, pkg: dict) -> None:
        """package.json must list react as a dependency."""
        deps = pkg.get("dependencies", {})
        assert "react" in deps

    def test_has_react_dom_dependency(self, pkg: dict) -> None:
        """package.json must list react-dom as a dependency."""
        deps = pkg.get("dependencies", {})
        assert "react-dom" in deps

    def test_has_typescript_devdep(self, pkg: dict) -> None:
        """package.json must list typescript as a dev dependency."""
        dev_deps = pkg.get("devDependencies", {})
        assert "typescript" in dev_deps

    def test_has_vite_devdep(self, pkg: dict) -> None:
        """package.json must list vite as a dev dependency."""
        dev_deps = pkg.get("devDependencies", {})
        assert "vite" in dev_deps


class TestAppComponent:
    """Verify src/App.tsx content."""

    @pytest.fixture()
    def content(self) -> str:
        """Read src/App.tsx content."""
        return (ROOT / "src" / "App.tsx").read_text(encoding="utf-8")

    def test_contains_hello_world(self, content: str) -> None:
        """App.tsx must render a Hello World heading."""
        assert "Hello World" in content

    def test_contains_usestate(self, content: str) -> None:
        """App.tsx must use useState for the counter."""
        assert "useState" in content

    def test_contains_count(self, content: str) -> None:
        """App.tsx must reference count in the rendered output."""
        assert "count" in content.lower()

    def test_contains_button(self, content: str) -> None:
        """App.tsx must render a button element."""
        assert "<button" in content


class TestIndexHtml:
    """Verify index.html content."""

    @pytest.fixture()
    def content(self) -> str:
        """Read index.html content."""
        return (ROOT / "index.html").read_text(encoding="utf-8")

    def test_has_root_div(self, content: str) -> None:
        """index.html must contain a root div."""
        assert 'id="root"' in content

    def test_has_module_script(self, content: str) -> None:
        """index.html must include the main.tsx module script."""
        assert 'type="module"' in content
        assert "src/main.tsx" in content

    def test_has_doctype(self, content: str) -> None:
        """index.html must start with a DOCTYPE declaration."""
        assert content.strip().startswith("<!DOCTYPE html>")


class TestViteConfig:
    """Verify vite.config.ts content."""

    @pytest.fixture()
    def content(self) -> str:
        """Read vite.config.ts content."""
        return (ROOT / "vite.config.ts").read_text(encoding="utf-8")

    def test_imports_react_plugin(self, content: str) -> None:
        """vite.config.ts must import the React plugin."""
        assert "@vitejs/plugin-react" in content

    def test_uses_define_config(self, content: str) -> None:
        """vite.config.ts must use defineConfig."""
        assert "defineConfig" in content


class TestTsConfig:
    """Verify tsconfig.json content."""

    @pytest.fixture()
    def config(self) -> dict:
        """Parse tsconfig.json."""
        text = (ROOT / "tsconfig.json").read_text(encoding="utf-8")
        return json.loads(text)

    def test_jsx_react_jsx(self, config: dict) -> None:
        """tsconfig.json must set jsx to react-jsx."""
        assert config.get("compilerOptions", {}).get("jsx") == "react-jsx"

    def test_strict_mode(self, config: dict) -> None:
        """tsconfig.json must enable strict mode."""
        assert config.get("compilerOptions", {}).get("strict") is True

    def test_includes_src(self, config: dict) -> None:
        """tsconfig.json must include the src directory."""
        assert "src" in config.get("include", [])
