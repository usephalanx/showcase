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
# File existence checks
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
    all_deps = {}
    all_deps.update(pkg.get("dependencies", {}))
    all_deps.update(pkg.get("devDependencies", {}))
    forbidden = ["next", "@angular/core", "vue", "svelte"]
    for dep in forbidden:
        assert dep not in all_deps, f"Unexpected dependency: {dep}"


# ------------------------------------------------------------------
# index.html checks
# ------------------------------------------------------------------


def test_index_html_has_root_div() -> None:
    """index.html must contain a <div id="root"> mount point."""
    content = (ROOT / "index.html").read_text(encoding="utf-8")
    assert 'id="root"' in content, "index.html missing div#root"


def test_index_html_references_main_tsx() -> None:
    """index.html must reference /src/main.tsx as a module script."""
    content = (ROOT / "index.html").read_text(encoding="utf-8")
    assert "/src/main.tsx" in content, "index.html missing script src for main.tsx"
    assert 'type="module"' in content, "Script tag should use type=module"


# ------------------------------------------------------------------
# Source file content checks
# ------------------------------------------------------------------


def test_app_tsx_contains_hello_world() -> None:
    """App.tsx must render the text 'Hello World'."""
    content = (ROOT / "src" / "App.tsx").read_text(encoding="utf-8")
    assert "Hello World" in content, "App.tsx must contain 'Hello World'"


def test_main_tsx_imports_app() -> None:
    """main.tsx must import the App component."""
    content = (ROOT / "src" / "main.tsx").read_text(encoding="utf-8")
    assert "import App" in content or "import { App }" in content, (
        "main.tsx must import App component"
    )


def test_main_tsx_uses_createroot() -> None:
    """main.tsx must use ReactDOM.createRoot (React 18 API)."""
    content = (ROOT / "src" / "main.tsx").read_text(encoding="utf-8")
    assert "createRoot" in content, "main.tsx must use createRoot (React 18 API)"


def test_main_tsx_uses_strict_mode() -> None:
    """main.tsx must wrap the app in React.StrictMode."""
    content = (ROOT / "src" / "main.tsx").read_text(encoding="utf-8")
    assert "StrictMode" in content, "main.tsx must use React.StrictMode"


# ------------------------------------------------------------------
# RUNNING.md checks
# ------------------------------------------------------------------


def test_running_md_contains_npm_install() -> None:
    """RUNNING.md must include 'npm install' instruction."""
    content = (ROOT / "RUNNING.md").read_text(encoding="utf-8")
    assert "npm install" in content, "RUNNING.md must mention 'npm install'"


def test_running_md_contains_npm_run_dev() -> None:
    """RUNNING.md must include 'npm run dev' instruction."""
    content = (ROOT / "RUNNING.md").read_text(encoding="utf-8")
    assert "npm run dev" in content, "RUNNING.md must mention 'npm run dev'"


def test_running_md_contains_localhost_url() -> None:
    """RUNNING.md must mention the localhost URL."""
    content = (ROOT / "RUNNING.md").read_text(encoding="utf-8")
    assert "localhost:5173" in content, "RUNNING.md must mention http://localhost:5173"


# ------------------------------------------------------------------
# tsconfig.json checks
# ------------------------------------------------------------------


def test_tsconfig_strict_mode() -> None:
    """tsconfig.json must enable strict mode."""
    content = (ROOT / "tsconfig.json").read_text(encoding="utf-8")
    tsconfig = json.loads(content)
    compiler_options = tsconfig.get("compilerOptions", {})
    assert compiler_options.get("strict") is True, "tsconfig must have strict: true"


def test_tsconfig_jsx_react_jsx() -> None:
    """tsconfig.json must set jsx to react-jsx."""
    content = (ROOT / "tsconfig.json").read_text(encoding="utf-8")
    tsconfig = json.loads(content)
    compiler_options = tsconfig.get("compilerOptions", {})
    assert compiler_options.get("jsx") == "react-jsx", (
        "tsconfig must set jsx to 'react-jsx'"
    )


def test_tsconfig_includes_src() -> None:
    """tsconfig.json must include the src directory."""
    content = (ROOT / "tsconfig.json").read_text(encoding="utf-8")
    tsconfig = json.loads(content)
    include = tsconfig.get("include", [])
    assert "src" in include, "tsconfig must include 'src' directory"


# ------------------------------------------------------------------
# vite.config.ts checks
# ------------------------------------------------------------------


def test_vite_config_imports_react_plugin() -> None:
    """vite.config.ts must import the React plugin."""
    content = (ROOT / "vite.config.ts").read_text(encoding="utf-8")
    assert "@vitejs/plugin-react" in content, (
        "vite.config.ts must import @vitejs/plugin-react"
    )


def test_vite_config_uses_define_config() -> None:
    """vite.config.ts must use defineConfig."""
    content = (ROOT / "vite.config.ts").read_text(encoding="utf-8")
    assert "defineConfig" in content, "vite.config.ts must use defineConfig"
