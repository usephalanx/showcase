"""Structural tests that verify the project architecture.

These tests inspect the file system and file contents to ensure that
all required project files exist with the expected configuration.
They do NOT require npm install or any Node.js tooling.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

# Repository root is one level above the tests/ directory.
ROOT: Path = Path(__file__).resolve().parent.parent


def _load_package_json() -> Dict[str, Any]:
    """Load and parse the root package.json file."""
    package_path = ROOT / "package.json"
    return json.loads(package_path.read_text(encoding="utf-8"))


# ------------------------------------------------------------------
# Individual file existence checks
# ------------------------------------------------------------------


def test_package_json_exists() -> None:
    """package.json must exist at the project root."""
    path = ROOT / "package.json"
    assert path.exists(), "Required file missing: package.json"
    assert path.is_file(), "Expected a file but got directory: package.json"


def test_vite_config_ts_exists() -> None:
    """vite.config.ts must exist at the project root."""
    path = ROOT / "vite.config.ts"
    assert path.exists(), "Required file missing: vite.config.ts"
    assert path.is_file(), "Expected a file but got directory: vite.config.ts"


def test_tsconfig_json_exists() -> None:
    """tsconfig.json must exist at the project root."""
    path = ROOT / "tsconfig.json"
    assert path.exists(), "Required file missing: tsconfig.json"
    assert path.is_file(), "Expected a file but got directory: tsconfig.json"


def test_index_html_exists() -> None:
    """index.html must exist at the project root."""
    path = ROOT / "index.html"
    assert path.exists(), "Required file missing: index.html"
    assert path.is_file(), "Expected a file but got directory: index.html"


def test_main_tsx_exists() -> None:
    """src/main.tsx must exist in the src directory."""
    path = ROOT / "src" / "main.tsx"
    assert path.exists(), "Required file missing: src/main.tsx"
    assert path.is_file(), "Expected a file but got directory: src/main.tsx"


def test_app_tsx_exists() -> None:
    """src/App.tsx must exist in the src directory."""
    path = ROOT / "src" / "App.tsx"
    assert path.exists(), "Required file missing: src/App.tsx"
    assert path.is_file(), "Expected a file but got directory: src/App.tsx"


def test_running_md_exists() -> None:
    """RUNNING.md must exist at the project root."""
    path = ROOT / "RUNNING.md"
    assert path.exists(), "Required file missing: RUNNING.md"
    assert path.is_file(), "Expected a file but got directory: RUNNING.md"


# ------------------------------------------------------------------
# Aggregate existence check
# ------------------------------------------------------------------


def test_required_files_exist() -> None:
    """All required project files must be present in the repository."""
    required_files = [
        "package.json",
        "vite.config.ts",
        "tsconfig.json",
        "index.html",
        "src/main.tsx",
        "src/App.tsx",
        "RUNNING.md",
    ]
    for relative in required_files:
        path = ROOT / relative
        assert path.exists(), f"Required file missing: {relative}"
        assert path.is_file(), f"Expected a file but got directory: {relative}"


# ------------------------------------------------------------------
# package.json dependency checks
# ------------------------------------------------------------------


def test_package_json_has_react_18() -> None:
    """package.json must list react ^18.x as a dependency."""
    pkg = _load_package_json()
    deps = pkg.get("dependencies", {})
    assert "react" in deps, "'react' not found in dependencies"
    assert "18" in deps["react"], f"Expected React 18, got {deps['react']}"


def test_package_json_has_react_dom_18() -> None:
    """package.json must list react-dom ^18.x as a dependency."""
    pkg = _load_package_json()
    deps = pkg.get("dependencies", {})
    assert "react-dom" in deps, "'react-dom' not found in dependencies"
    assert "18" in deps["react-dom"], f"Expected React-DOM 18, got {deps['react-dom']}"


def test_package_json_has_vite_5() -> None:
    """package.json must list vite ^5.x as a dev dependency."""
    pkg = _load_package_json()
    dev_deps = pkg.get("devDependencies", {})
    assert "vite" in dev_deps, "'vite' not found in devDependencies"
    assert "5" in dev_deps["vite"], f"Expected Vite 5, got {dev_deps['vite']}"


def test_package_json_has_typescript() -> None:
    """package.json must list typescript as a dev dependency."""
    pkg = _load_package_json()
    dev_deps = pkg.get("devDependencies", {})
    assert "typescript" in dev_deps, "'typescript' not found in devDependencies"


def test_package_json_has_vitejs_plugin_react() -> None:
    """package.json must list @vitejs/plugin-react as a dev dependency."""
    pkg = _load_package_json()
    dev_deps = pkg.get("devDependencies", {})
    assert "@vitejs/plugin-react" in dev_deps, (
        "'@vitejs/plugin-react' not found in devDependencies"
    )


def test_package_json_scripts() -> None:
    """package.json must define dev, build, and preview scripts."""
    pkg = _load_package_json()
    scripts = pkg.get("scripts", {})
    assert "dev" in scripts, "'dev' script missing"
    assert "build" in scripts, "'build' script missing"
    assert "preview" in scripts, "'preview' script missing"
    assert "vite" in scripts["dev"], "'dev' script should invoke vite"


def test_package_json_no_heavy_deps() -> None:
    """package.json should not include heavy frameworks like next, angular, or vue."""
    pkg = _load_package_json()
    all_deps: Dict[str, str] = {}
    all_deps.update(pkg.get("dependencies", {}))
    all_deps.update(pkg.get("devDependencies", {}))
    forbidden = ["next", "@angular/core", "vue", "svelte"]
    for dep in forbidden:
        assert dep not in all_deps, f"Unexpected dependency: {dep}"
