"""Tests to validate the structural completeness of ARCHITECTURE.md and RUNNING.md.

These tests ensure that the documentation files exist and contain all
required sections, endpoint references, and component names as specified
in the project plan.
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest

REPO_ROOT: Path = Path(__file__).resolve().parent.parent
ARCHITECTURE_PATH: Path = REPO_ROOT / "ARCHITECTURE.md"
RUNNING_PATH: Path = REPO_ROOT / "RUNNING.md"


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def _read_file(path: Path) -> str:
    """Read and return the full text content of a file."""
    return path.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# ARCHITECTURE.md existence
# ---------------------------------------------------------------------------


def test_architecture_md_exists() -> None:
    """ARCHITECTURE.md must exist at the repository root."""
    assert ARCHITECTURE_PATH.exists(), (
        f"ARCHITECTURE.md not found at {ARCHITECTURE_PATH}"
    )


# ---------------------------------------------------------------------------
# ARCHITECTURE.md required sections
# ---------------------------------------------------------------------------


_REQUIRED_SECTIONS = [
    "## 1. Overview",
    "## 2. Backend Architecture",
    "## 3. Database Schema",
    "## 4. API Endpoints",
    "## 5. Frontend Architecture",
    "## 6. File Structure",
    "## 7. CORS Configuration",
    "## 8. Development Workflow",
]


def test_architecture_md_has_required_sections() -> None:
    """ARCHITECTURE.md must contain all eight required section headings."""
    content = _read_file(ARCHITECTURE_PATH)
    for section in _REQUIRED_SECTIONS:
        assert section in content, (
            f"Missing section heading: '{section}' in ARCHITECTURE.md"
        )


# ---------------------------------------------------------------------------
# ARCHITECTURE.md endpoint references
# ---------------------------------------------------------------------------


_REQUIRED_ENDPOINTS = [
    "GET /tasks",
    "GET /tasks/{id}",
    "POST /tasks",
    "PUT /tasks/{id}",
    "DELETE /tasks/{id}",
]


def test_architecture_md_has_all_endpoints() -> None:
    """ARCHITECTURE.md must reference every REST endpoint."""
    content = _read_file(ARCHITECTURE_PATH)
    for endpoint in _REQUIRED_ENDPOINTS:
        assert endpoint in content, (
            f"Missing endpoint reference: '{endpoint}' in ARCHITECTURE.md"
        )


# ---------------------------------------------------------------------------
# ARCHITECTURE.md component references
# ---------------------------------------------------------------------------


_REQUIRED_COMPONENTS = [
    "App",
    "HomePage",
    "TaskForm",
    "TaskList",
    "TaskCard",
    "StatusBadge",
]


def test_architecture_md_has_all_components() -> None:
    """ARCHITECTURE.md must mention every React component by name."""
    content = _read_file(ARCHITECTURE_PATH)
    for component in _REQUIRED_COMPONENTS:
        assert component in content, (
            f"Missing component reference: '{component}' in ARCHITECTURE.md"
        )


# ---------------------------------------------------------------------------
# RUNNING.md existence
# ---------------------------------------------------------------------------


def test_running_md_exists() -> None:
    """RUNNING.md must exist at the repository root."""
    assert RUNNING_PATH.exists(), (
        f"RUNNING.md not found at {RUNNING_PATH}"
    )


# ---------------------------------------------------------------------------
# RUNNING.md content checks
# ---------------------------------------------------------------------------


def test_running_md_has_docker_compose_instructions() -> None:
    """RUNNING.md must contain docker compose commands."""
    content = _read_file(RUNNING_PATH)
    assert "docker compose up --build" in content, (
        "RUNNING.md must include 'docker compose up --build' command"
    )
    assert "docker compose down" in content, (
        "RUNNING.md must include 'docker compose down' command"
    )


def test_running_md_has_service_urls() -> None:
    """RUNNING.md must reference the frontend and backend URLs."""
    content = _read_file(RUNNING_PATH)
    assert "http://localhost:5173" in content, (
        "RUNNING.md must reference the frontend URL http://localhost:5173"
    )
    assert "http://localhost:8000" in content, (
        "RUNNING.md must reference the backend URL http://localhost:8000"
    )
    assert "http://localhost:8000/docs" in content, (
        "RUNNING.md must reference the API docs URL http://localhost:8000/docs"
    )


# ---------------------------------------------------------------------------
# Frontend project file existence checks
# ---------------------------------------------------------------------------


def test_frontend_package_json_exists() -> None:
    """frontend/package.json must exist."""
    path = REPO_ROOT / "frontend" / "package.json"
    assert path.exists(), f"frontend/package.json not found at {path}"


def test_frontend_vite_config_exists() -> None:
    """frontend/vite.config.ts must exist."""
    path = REPO_ROOT / "frontend" / "vite.config.ts"
    assert path.exists(), f"frontend/vite.config.ts not found at {path}"


def test_frontend_tsconfig_exists() -> None:
    """frontend/tsconfig.json must exist."""
    path = REPO_ROOT / "frontend" / "tsconfig.json"
    assert path.exists(), f"frontend/tsconfig.json not found at {path}"


def test_frontend_index_html_exists() -> None:
    """frontend/index.html must exist with a root div."""
    path = REPO_ROOT / "frontend" / "index.html"
    assert path.exists(), f"frontend/index.html not found at {path}"
    content = _read_file(path)
    assert 'id="root"' in content, (
        "frontend/index.html must contain a div with id='root'"
    )


# ---------------------------------------------------------------------------
# Frontend package.json dependency checks
# ---------------------------------------------------------------------------


def test_frontend_package_json_has_required_dependencies() -> None:
    """frontend/package.json must list all required dependencies."""
    import json

    path = REPO_ROOT / "frontend" / "package.json"
    data = json.loads(_read_file(path))

    deps = set(data.get("dependencies", {}).keys())
    dev_deps = set(data.get("devDependencies", {}).keys())
    all_deps = deps | dev_deps

    required = {"react", "react-dom", "typescript", "vite", "@vitejs/plugin-react", "axios"}
    for dep in required:
        assert dep in all_deps, (
            f"frontend/package.json is missing required dependency: {dep}"
        )


# ---------------------------------------------------------------------------
# Vite config content checks
# ---------------------------------------------------------------------------


def test_vite_config_has_react_plugin() -> None:
    """frontend/vite.config.ts must import and use the React plugin."""
    path = REPO_ROOT / "frontend" / "vite.config.ts"
    content = _read_file(path)
    assert "@vitejs/plugin-react" in content, (
        "vite.config.ts must import '@vitejs/plugin-react'"
    )
    assert "react()" in content, (
        "vite.config.ts must call the react() plugin"
    )


def test_vite_config_has_port_5173() -> None:
    """frontend/vite.config.ts must configure dev server on port 5173."""
    path = REPO_ROOT / "frontend" / "vite.config.ts"
    content = _read_file(path)
    assert "5173" in content, (
        "vite.config.ts must set the dev server port to 5173"
    )


# ---------------------------------------------------------------------------
# tsconfig.json strict mode check
# ---------------------------------------------------------------------------


def test_tsconfig_has_strict_mode() -> None:
    """frontend/tsconfig.json must enable strict mode."""
    import json

    path = REPO_ROOT / "frontend" / "tsconfig.json"
    data = json.loads(_read_file(path))
    compiler_options = data.get("compilerOptions", {})
    assert compiler_options.get("strict") is True, (
        "tsconfig.json must have \"strict\": true in compilerOptions"
    )
