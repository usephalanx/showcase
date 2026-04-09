"""Tests for tsconfig.json structure and compiler options.

Validates that the TypeScript configuration matches the required
settings for strict mode, modern JSX transform, and ESNext modules.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

import pytest

ROOT_DIR = Path(__file__).resolve().parent.parent
TSCONFIG_PATH = ROOT_DIR / "tsconfig.json"


@pytest.fixture()
def tsconfig() -> Dict[str, Any]:
    """Parse and return the contents of tsconfig.json as a dictionary."""
    assert TSCONFIG_PATH.exists(), "tsconfig.json must exist at the project root"
    content = TSCONFIG_PATH.read_text(encoding="utf-8")
    return json.loads(content)


def test_tsconfig_exists() -> None:
    """tsconfig.json should exist at the project root."""
    assert TSCONFIG_PATH.exists()


def test_tsconfig_is_valid_json() -> None:
    """tsconfig.json should be valid JSON."""
    content = TSCONFIG_PATH.read_text(encoding="utf-8")
    parsed = json.loads(content)
    assert isinstance(parsed, dict)


def test_strict_mode(tsconfig: Dict[str, Any]) -> None:
    """TypeScript strict mode should be enabled."""
    assert tsconfig["compilerOptions"]["strict"] is True


def test_jsx_react_jsx(tsconfig: Dict[str, Any]) -> None:
    """JSX should be set to 'react-jsx' for the modern transform."""
    assert tsconfig["compilerOptions"]["jsx"] == "react-jsx"


def test_module_esnext(tsconfig: Dict[str, Any]) -> None:
    """Module system should be set to ESNext."""
    assert tsconfig["compilerOptions"]["module"] == "ESNext"


def test_module_resolution_bundler(tsconfig: Dict[str, Any]) -> None:
    """Module resolution should be set to 'bundler'."""
    assert tsconfig["compilerOptions"]["moduleResolution"] == "bundler"


def test_target_es2020(tsconfig: Dict[str, Any]) -> None:
    """Compilation target should be ES2020."""
    assert tsconfig["compilerOptions"]["target"] == "ES2020"


def test_include_src(tsconfig: Dict[str, Any]) -> None:
    """The 'include' array should contain 'src'."""
    assert "include" in tsconfig
    assert "src" in tsconfig["include"]


def test_no_emit(tsconfig: Dict[str, Any]) -> None:
    """noEmit should be true (Vite handles bundling, not tsc)."""
    assert tsconfig["compilerOptions"]["noEmit"] is True


def test_isolated_modules(tsconfig: Dict[str, Any]) -> None:
    """isolatedModules should be true for compatibility with Vite/esbuild."""
    assert tsconfig["compilerOptions"]["isolatedModules"] is True


def test_es_module_interop(tsconfig: Dict[str, Any]) -> None:
    """esModuleInterop should be enabled."""
    assert tsconfig["compilerOptions"]["esModuleInterop"] is True


def test_skip_lib_check(tsconfig: Dict[str, Any]) -> None:
    """skipLibCheck should be enabled for faster compilation."""
    assert tsconfig["compilerOptions"]["skipLibCheck"] is True


def test_force_consistent_casing(tsconfig: Dict[str, Any]) -> None:
    """forceConsistentCasingInFileNames should be enabled."""
    assert tsconfig["compilerOptions"]["forceConsistentCasingInFileNames"] is True


def test_resolve_json_module(tsconfig: Dict[str, Any]) -> None:
    """resolveJsonModule should be enabled."""
    assert tsconfig["compilerOptions"]["resolveJsonModule"] is True


def test_lib_includes_dom(tsconfig: Dict[str, Any]) -> None:
    """The lib array should include ES2020, DOM, and DOM.Iterable."""
    lib = tsconfig["compilerOptions"]["lib"]
    assert "ES2020" in lib
    assert "DOM" in lib
    assert "DOM.Iterable" in lib
