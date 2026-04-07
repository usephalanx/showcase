"""Structural tests for the React Todo application.

Verify that the critical source files exist and contain the expected
import/export signatures so the app compiles end-to-end.
"""

import os
from pathlib import Path
from typing import List

import pytest

# Repository root is two levels up from tests/
ROOT: Path = Path(__file__).resolve().parent.parent


def _read(rel_path: str) -> str:
    """Read a file relative to the repository root and return its contents."""
    full = ROOT / rel_path
    assert full.exists(), f"Expected file not found: {rel_path}"
    return full.read_text(encoding="utf-8")


class TestCriticalFilesExist:
    """Ensure the minimum set of files required for compilation are present."""

    @pytest.mark.parametrize(
        "rel_path",
        [
            "src/App.tsx",
            "src/pages/TodoPage.tsx",
            "RUNNING.md",
            "ARCHITECTURE.md",
        ],
    )
    def test_file_exists(self, rel_path: str) -> None:
        """Verify that *rel_path* exists relative to the repo root."""
        full = ROOT / rel_path
        assert full.exists(), f"Missing file: {rel_path}"


class TestAppTsx:
    """Verify src/App.tsx imports and renders TodoPage correctly."""

    def test_imports_todo_page(self) -> None:
        """App.tsx must import TodoPage from the pages directory."""
        content = _read("src/App.tsx")
        assert "import TodoPage from './pages/TodoPage'" in content

    def test_renders_todo_page(self) -> None:
        """App.tsx must render the <TodoPage /> component."""
        content = _read("src/App.tsx")
        assert "<TodoPage />" in content or "<TodoPage/>" in content

    def test_exports_default(self) -> None:
        """App.tsx must have a default export."""
        content = _read("src/App.tsx")
        assert "export default App" in content


class TestTodoPage:
    """Verify src/pages/TodoPage.tsx is a self-contained, compilable component."""

    def test_exports_default(self) -> None:
        """TodoPage.tsx must have a default export."""
        content = _read("src/pages/TodoPage.tsx")
        assert "export default TodoPage" in content

    def test_does_not_import_nonexistent_components(self) -> None:
        """TodoPage must not import from ../components/* until those files exist."""
        content = _read("src/pages/TodoPage.tsx")
        # If TodoPage imports from ../components, verify each imported file exists.
        import re

        matches: List[str] = re.findall(
            r"from\s+['\"](\.\./components/\w+)['\"]", content
        )
        for rel_import in matches:
            # Convert relative import to file path from src/pages/
            resolved = (ROOT / "src" / "pages" / rel_import).with_suffix(".tsx")
            assert resolved.exists(), (
                f"TodoPage.tsx imports '{rel_import}' but {resolved} does not exist"
            )

    def test_contains_todo_interface(self) -> None:
        """TodoPage.tsx must define or import a Todo type."""
        content = _read("src/pages/TodoPage.tsx")
        assert "Todo" in content

    def test_uses_usestate(self) -> None:
        """TodoPage.tsx must use useState for state management."""
        content = _read("src/pages/TodoPage.tsx")
        assert "useState" in content


class TestRunningMd:
    """Verify RUNNING.md contains the required setup instructions."""

    def test_contains_npm_install(self) -> None:
        """RUNNING.md must document 'npm install'."""
        content = _read("RUNNING.md")
        assert "npm install" in content

    def test_contains_npm_run_dev(self) -> None:
        """RUNNING.md must document 'npm run dev'."""
        content = _read("RUNNING.md")
        assert "npm run dev" in content

    def test_contains_npm_test(self) -> None:
        """RUNNING.md must document 'npm test'."""
        content = _read("RUNNING.md")
        assert "npm test" in content

    def test_contains_app_description(self) -> None:
        """RUNNING.md must contain a description of the application."""
        content = _read("RUNNING.md")
        assert "Todo" in content
        assert "application" in content.lower() or "app" in content.lower()

    def test_mentions_localhost_5173(self) -> None:
        """RUNNING.md must mention the default dev server URL."""
        content = _read("RUNNING.md")
        assert "5173" in content


class TestArchitectureMd:
    """Verify ARCHITECTURE.md contains key architectural decisions."""

    def test_contains_file_structure_section(self) -> None:
        """ARCHITECTURE.md must have a File Structure section."""
        content = _read("ARCHITECTURE.md")
        assert "File Structure" in content or "file structure" in content.lower()

    def test_defines_todo_interface(self) -> None:
        """ARCHITECTURE.md must define the Todo interface with required fields."""
        content = _read("ARCHITECTURE.md")
        for field in ["id: string", "text: string", "completed: boolean", "createdAt: number"]:
            assert field in content, f"ARCHITECTURE.md missing Todo field: {field}"

    def test_defines_filter_type(self) -> None:
        """ARCHITECTURE.md must define the FilterType union."""
        content = _read("ARCHITECTURE.md")
        assert "FilterType" in content
        assert "'all'" in content
        assert "'active'" in content
        assert "'completed'" in content

    def test_lists_source_files(self) -> None:
        """ARCHITECTURE.md must reference at least 14 source file paths."""
        content = _read("ARCHITECTURE.md")
        # Count .tsx and .ts file references (excluding markdown code fence language hints)
        import re

        file_refs = re.findall(r"\S+\.tsx?\b", content)
        # Deduplicate
        unique = set(file_refs)
        assert len(unique) >= 14, (
            f"Expected at least 14 unique .ts/.tsx file references, found {len(unique)}: {unique}"
        )
