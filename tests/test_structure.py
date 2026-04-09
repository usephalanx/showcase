"""Structural tests for the Hello World React + Vite project.

Verifies that every required file exists in the project tree.
Each file check is its own test function following pytest conventions.
Paths are resolved relative to the project root using
``pathlib.Path(__file__).parent.parent``.
"""

import os
from pathlib import Path

import pytest

# Resolve project root (one level up from the tests/ directory).
BASE_DIR: Path = Path(__file__).resolve().parent.parent


def test_package_json_exists() -> None:
    """package.json must exist at the project root."""
    filepath = BASE_DIR / "package.json"
    assert filepath.exists(), f"Missing required file: {filepath}"
    assert filepath.is_file(), f"Expected a regular file: {filepath}"


def test_vite_config_ts_exists() -> None:
    """vite.config.ts must exist at the project root."""
    filepath = BASE_DIR / "vite.config.ts"
    assert filepath.exists(), f"Missing required file: {filepath}"
    assert filepath.is_file(), f"Expected a regular file: {filepath}"


def test_index_html_exists() -> None:
    """index.html must exist at the project root."""
    filepath = BASE_DIR / "index.html"
    assert filepath.exists(), f"Missing required file: {filepath}"
    assert filepath.is_file(), f"Expected a regular file: {filepath}"


def test_tsconfig_json_exists() -> None:
    """tsconfig.json must exist at the project root."""
    filepath = BASE_DIR / "tsconfig.json"
    assert filepath.exists(), f"Missing required file: {filepath}"
    assert filepath.is_file(), f"Expected a regular file: {filepath}"


def test_main_tsx_exists() -> None:
    """src/main.tsx must exist in the src directory."""
    filepath = BASE_DIR / "src" / "main.tsx"
    assert filepath.exists(), f"Missing required file: {filepath}"
    assert filepath.is_file(), f"Expected a regular file: {filepath}"


def test_app_tsx_exists() -> None:
    """src/App.tsx must exist in the src directory."""
    filepath = BASE_DIR / "src" / "App.tsx"
    assert filepath.exists(), f"Missing required file: {filepath}"
    assert filepath.is_file(), f"Expected a regular file: {filepath}"


def test_running_md_exists() -> None:
    """RUNNING.md must exist at the project root."""
    filepath = BASE_DIR / "RUNNING.md"
    assert filepath.exists(), f"Missing required file: {filepath}"
    assert filepath.is_file(), f"Expected a regular file: {filepath}"
