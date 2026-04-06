"""Tests that validate the contents of RUNNING.md.

Ensures the documentation contains all required sections, URLs, and
commands so that a developer can follow it to run the application.
"""

from __future__ import annotations

from pathlib import Path

import pytest

RUNNING_MD_PATH = Path(__file__).resolve().parent.parent / "RUNNING.md"


@pytest.fixture(scope="module")
def running_md_content() -> str:
    """Read and return the contents of RUNNING.md."""
    assert RUNNING_MD_PATH.exists(), f"RUNNING.md not found at {RUNNING_MD_PATH}"
    return RUNNING_MD_PATH.read_text(encoding="utf-8")


def test_running_md_exists() -> None:
    """Verify RUNNING.md exists at the repository root."""
    assert RUNNING_MD_PATH.exists()


def test_running_md_has_backend_install_instructions(running_md_content: str) -> None:
    """Verify that backend dependency installation is documented."""
    assert "pip install" in running_md_content


def test_running_md_has_uvicorn_command(running_md_content: str) -> None:
    """Verify that the uvicorn run command is documented."""
    assert "uvicorn" in running_md_content
    assert "backend.main:app" in running_md_content


def test_running_md_has_frontend_install_instructions(running_md_content: str) -> None:
    """Verify that frontend dependency installation is documented."""
    assert "npm install" in running_md_content


def test_running_md_has_vite_dev_server_command(running_md_content: str) -> None:
    """Verify that the Vite dev server run command is documented."""
    assert "npm run dev" in running_md_content


def test_running_md_has_seed_command(running_md_content: str) -> None:
    """Verify that the optional seed command is documented."""
    assert "python -m backend.seed" in running_md_content


def test_running_md_has_backend_url(running_md_content: str) -> None:
    """Verify that the backend URL is documented."""
    assert "http://localhost:8000" in running_md_content


def test_running_md_has_frontend_url(running_md_content: str) -> None:
    """Verify that the frontend URL is documented."""
    assert "http://localhost:5173" in running_md_content


def test_running_md_has_swagger_url(running_md_content: str) -> None:
    """Verify that the Swagger UI URL is documented."""
    assert "http://localhost:8000/docs" in running_md_content


def test_running_md_has_docker_instructions(running_md_content: str) -> None:
    """Verify that Docker Compose instructions are included."""
    assert "docker compose up" in running_md_content
    assert "docker compose down" in running_md_content
