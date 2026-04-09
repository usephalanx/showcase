"""Tests to verify the Vite + TypeScript + React project scaffolding.

Validates that all required configuration files exist and contain
the expected content.
"""

import json
from pathlib import Path
from typing import Any, Dict

import pytest

ROOT = Path(__file__).resolve().parent.parent


def _read_text(filename: str) -> str:
    """Read a file from the project root and return its text content."""
    path = ROOT / filename
    assert path.exists(), f"{filename} must exist at the project root"
    return path.read_text(encoding="utf-8")


def _load_json(filename: str) -> Dict[str, Any]:
    """Read a JSON file from the project root."""
    content = _read_text(filename)
    return json.loads(content)


# -------------------------------------------------------------------------
# package.json tests
# -------------------------------------------------------------------------


class TestPackageJson:
    """Tests for package.json structure and required dependencies."""

    @pytest.fixture(autouse=True)
    def _load(self) -> None:
        """Load package.json once for all tests in this class."""
        self.pkg: Dict[str, Any] = _load_json("package.json")

    def test_package_json_exists(self) -> None:
        """package.json exists and is valid JSON."""
        assert isinstance(self.pkg, dict)

    def test_has_name(self) -> None:
        """package.json has a name field."""
        assert "name" in self.pkg

    def test_has_type_module(self) -> None:
        """package.json uses ES module type."""
        assert self.pkg.get("type") == "module"

    def test_react_dependency(self) -> None:
        """react is listed as a dependency."""
        deps = self.pkg.get("dependencies", {})
        assert "react" in deps, "react must be in dependencies"

    def test_react_dom_dependency(self) -> None:
        """react-dom is listed as a dependency."""
        deps = self.pkg.get("dependencies", {})
        assert "react-dom" in deps, "react-dom must be in dependencies"

    def test_typescript_dev_dependency(self) -> None:
        """typescript is listed as a devDependency."""
        dev = self.pkg.get("devDependencies", {})
        assert "typescript" in dev, "typescript must be in devDependencies"

    def test_vite_dev_dependency(self) -> None:
        """vite is listed as a devDependency."""
        dev = self.pkg.get("devDependencies", {})
        assert "vite" in dev, "vite must be in devDependencies"

    def test_vite_plugin_react_dev_dependency(self) -> None:
        """@vitejs/plugin-react is listed as a devDependency."""
        dev = self.pkg.get("devDependencies", {})
        assert "@vitejs/plugin-react" in dev, (
            "@vitejs/plugin-react must be in devDependencies"
        )

    def test_has_dev_script(self) -> None:
        """A 'dev' script is defined."""
        scripts = self.pkg.get("scripts", {})
        assert "dev" in scripts

    def test_has_build_script(self) -> None:
        """A 'build' script is defined."""
        scripts = self.pkg.get("scripts", {})
        assert "build" in scripts


# -------------------------------------------------------------------------
# vite.config.ts tests
# -------------------------------------------------------------------------


class TestViteConfig:
    """Tests for vite.config.ts content."""

    @pytest.fixture(autouse=True)
    def _load(self) -> None:
        """Load vite.config.ts content."""
        self.content: str = _read_text("vite.config.ts")

    def test_vite_config_exists(self) -> None:
        """vite.config.ts exists."""
        assert len(self.content) > 0

    def test_imports_define_config(self) -> None:
        """vite.config.ts imports defineConfig from vite."""
        assert "defineConfig" in self.content

    def test_imports_react_plugin(self) -> None:
        """vite.config.ts imports the React plugin."""
        assert "@vitejs/plugin-react" in self.content

    def test_uses_react_plugin(self) -> None:
        """vite.config.ts includes react() in the plugins array."""
        assert "react()" in self.content

    def test_exports_default(self) -> None:
        """vite.config.ts has a default export."""
        assert "export default" in self.content


# -------------------------------------------------------------------------
# tsconfig.json tests
# -------------------------------------------------------------------------


class TestTsConfig:
    """Tests for tsconfig.json content."""

    @pytest.fixture(autouse=True)
    def _load(self) -> None:
        """Load tsconfig.json."""
        self.tsconfig: Dict[str, Any] = _load_json("tsconfig.json")

    def test_tsconfig_exists(self) -> None:
        """tsconfig.json exists and is valid JSON."""
        assert isinstance(self.tsconfig, dict)

    def test_strict_mode_enabled(self) -> None:
        """tsconfig.json has strict mode enabled."""
        compiler = self.tsconfig.get("compilerOptions", {})
        assert compiler.get("strict") is True, "strict must be true"

    def test_jsx_react_jsx(self) -> None:
        """tsconfig.json uses react-jsx transform."""
        compiler = self.tsconfig.get("compilerOptions", {})
        assert compiler.get("jsx") == "react-jsx"

    def test_module_resolution(self) -> None:
        """tsconfig.json has a module resolution strategy set."""
        compiler = self.tsconfig.get("compilerOptions", {})
        assert "moduleResolution" in compiler

    def test_includes_src(self) -> None:
        """tsconfig.json includes the src directory."""
        include = self.tsconfig.get("include", [])
        assert "src" in include, "'src' must be in include list"


# -------------------------------------------------------------------------
# PLAN.md tests
# -------------------------------------------------------------------------


class TestPlanMd:
    """Tests for PLAN.md content."""

    @pytest.fixture(autouse=True)
    def _load(self) -> None:
        """Load PLAN.md content."""
        self.content: str = _read_text("PLAN.md")

    def test_plan_md_exists(self) -> None:
        """PLAN.md exists."""
        assert len(self.content) > 0

    def test_file_structure_section(self) -> None:
        """PLAN.md has a File Structure section."""
        assert "File Structure" in self.content

    def test_references_todo_types(self) -> None:
        """PLAN.md references src/types/todo.ts."""
        assert "src/types/todo.ts" in self.content

    def test_references_app_component(self) -> None:
        """PLAN.md references src/components/App/App.tsx."""
        assert "src/components/App/App.tsx" in self.content

    def test_references_todo_input_component(self) -> None:
        """PLAN.md references src/components/TodoInput/TodoInput.tsx."""
        assert "src/components/TodoInput/TodoInput.tsx" in self.content

    def test_references_todo_list_component(self) -> None:
        """PLAN.md references src/components/TodoList/TodoList.tsx."""
        assert "src/components/TodoList/TodoList.tsx" in self.content

    def test_references_todo_item_component(self) -> None:
        """PLAN.md references src/components/TodoItem/TodoItem.tsx."""
        assert "src/components/TodoItem/TodoItem.tsx" in self.content

    def test_references_main_tsx(self) -> None:
        """PLAN.md references src/main.tsx."""
        assert "src/main.tsx" in self.content

    def test_data_model_section(self) -> None:
        """PLAN.md has a Data Model section."""
        assert "Data Model" in self.content

    def test_todo_interface_id_string(self) -> None:
        """PLAN.md defines id as string in the Todo interface."""
        assert "id" in self.content
        assert "string" in self.content

    def test_todo_interface_text_string(self) -> None:
        """PLAN.md defines text as string in the Todo interface."""
        assert "text" in self.content

    def test_todo_interface_completed_boolean(self) -> None:
        """PLAN.md defines completed as boolean in the Todo interface."""
        assert "completed" in self.content
        assert "boolean" in self.content

    def test_component_hierarchy_section(self) -> None:
        """PLAN.md has a Component Hierarchy section."""
        assert "Component Hierarchy" in self.content

    def test_state_management_section(self) -> None:
        """PLAN.md has a State Management section."""
        assert "State Management" in self.content

    def test_uses_usestate(self) -> None:
        """PLAN.md specifies useState for state management."""
        assert "useState" in self.content

    def test_styling_strategy_section(self) -> None:
        """PLAN.md has a Styling Strategy section."""
        assert "Styling" in self.content

    def test_css_modules_mentioned(self) -> None:
        """PLAN.md specifies CSS Modules."""
        assert "CSS Modules" in self.content

    def test_crypto_random_uuid(self) -> None:
        """PLAN.md specifies crypto.randomUUID() for id generation."""
        assert "crypto.randomUUID()" in self.content

    def test_testing_strategy_section(self) -> None:
        """PLAN.md has a Testing Strategy section."""
        assert "Testing Strategy" in self.content


# -------------------------------------------------------------------------
# RUNNING.md tests
# -------------------------------------------------------------------------


class TestRunningMd:
    """Tests for RUNNING.md content."""

    @pytest.fixture(autouse=True)
    def _load(self) -> None:
        """Load RUNNING.md content."""
        self.content: str = _read_text("RUNNING.md")

    def test_running_md_exists(self) -> None:
        """RUNNING.md exists."""
        assert len(self.content) > 0

    def test_has_team_brief(self) -> None:
        """RUNNING.md contains a TEAM_BRIEF section."""
        assert "TEAM_BRIEF" in self.content

    def test_team_brief_has_stack(self) -> None:
        """TEAM_BRIEF declares the stack."""
        assert "stack:" in self.content

    def test_team_brief_has_test_runner(self) -> None:
        """TEAM_BRIEF declares the test runner."""
        assert "test_runner:" in self.content
