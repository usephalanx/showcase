"""Tests to verify RUNNING.md exists and contains required sections."""

from __future__ import annotations

from pathlib import Path

RUNNING_MD = Path(__file__).resolve().parent.parent / "RUNNING.md"


def test_running_md_exists() -> None:
    """RUNNING.md must be present at the repository root."""
    assert RUNNING_MD.exists(), "RUNNING.md not found at the repository root"


def test_running_md_contains_install_instructions() -> None:
    """RUNNING.md must document how to install dependencies."""
    content = RUNNING_MD.read_text(encoding="utf-8")
    assert "pip install -r requirements.txt" in content


def test_running_md_contains_run_instructions() -> None:
    """RUNNING.md must document how to start the application."""
    content = RUNNING_MD.read_text(encoding="utf-8")
    assert "python main.py" in content
    assert "uvicorn" in content


def test_running_md_mentions_seed_data() -> None:
    """RUNNING.md must mention that seed data is pre-loaded."""
    content = RUNNING_MD.read_text(encoding="utf-8")
    assert "seed" in content.lower()


def test_running_md_contains_test_instructions() -> None:
    """RUNNING.md must explain how to run the test suite."""
    content = RUNNING_MD.read_text(encoding="utf-8")
    assert "pytest" in content
