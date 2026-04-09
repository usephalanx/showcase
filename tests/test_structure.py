"""Structural tests for the Hello World React project.

These tests verify that every required file exists, that configuration
files contain expected values, and that the App component meets the
specification (centered Hello World text).
"""

import json
import os
from pathlib import Path
from typing import Any, Dict

import pytest

# Root of the repository (parent of the tests/ directory).
ROOT: Path = Path(__file__).resolve().parent.parent


def _load_json(path: Path) -> Dict[str, Any]:
    """Load and return a JSON file as a dictionary."""
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def _read_text(path: Path) -> str:
    """Read and return the full text content of a file."""
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


# ------------------------------------------------------------------
# File existence
# ------------------------------------------------------------------

REQUIRED_FILES = [
    "package.json",
    "vite.config.ts",
    "tsconfig.json",
    "index.html",
    "src/main.tsx",
    "src/App.tsx",
    "RUNNING.md",
]


@pytest.mark.parametrize("rel_path", REQUIRED_FILES)
def test_required_files_exist(rel_path: str) -> None:
    """Every required project file must exist on disk."""
    full = ROOT / rel_path
    assert full.exists(), f"Missing required file: {rel_path}"


# ------------------------------------------------------------------
# package.json — dependencies
# ------------------------------------------------------------------


@pytest.fixture()
def package_json() -> Dict[str, Any]:
    """Return the parsed package.json content."""
    return _load_json(ROOT / "package.json")


def test_package_json_has_react_18(package_json: Dict[str, Any]) -> None:
    """package.json must list react ^18 as a dependency."""
    deps = package_json.get("dependencies", {})
    assert "react" in deps, "react not in dependencies"
    assert "18" in deps["react"], f"Expected react 18, got {deps['react']}"


def test_package_json_has_react_dom_18(package_json: Dict[str, Any]) -> None:
    """package.json must list react-dom ^18 as a dependency."""
    deps = package_json.get("dependencies", {})
    assert "react-dom" in deps, "react-dom not in dependencies"
    assert "18" in deps["react-dom"], f"Expected react-dom 18, got {deps['react-dom']}"


def test_package_json_has_vite_5(package_json: Dict[str, Any]) -> None:
    """package.json must list vite ^5 as a dev dependency."""
    dev_deps = package_json.get("devDependencies", {})
    assert "vite" in dev_deps, "vite not in devDependencies"
    assert "5" in dev_deps["vite"], f"Expected vite 5, got {dev_deps['vite']}"


def test_package_json_has_typescript(package_json: Dict[str, Any]) -> None:
    """package.json must list typescript as a dev dependency."""
    dev_deps = package_json.get("devDependencies", {})
    assert "typescript" in dev_deps, "typescript not in devDependencies"


def test_package_json_has_vitejs_plugin_react(package_json: Dict[str, Any]) -> None:
    """package.json must list @vitejs/plugin-react as a dev dependency."""
    dev_deps = package_json.get("devDependencies", {})
    assert "@vitejs/plugin-react" in dev_deps, "@vitejs/plugin-react not in devDependencies"


def test_package_json_has_types_react(package_json: Dict[str, Any]) -> None:
    """package.json must list @types/react as a dev dependency."""
    dev_deps = package_json.get("devDependencies", {})
    assert "@types/react" in dev_deps, "@types/react not in devDependencies"


def test_package_json_has_types_react_dom(package_json: Dict[str, Any]) -> None:
    """package.json must list @types/react-dom as a dev dependency."""
    dev_deps = package_json.get("devDependencies", {})
    assert "@types/react-dom" in dev_deps, "@types/react-dom not in devDependencies"


def test_package_json_scripts(package_json: Dict[str, Any]) -> None:
    """package.json must define dev, build, and preview scripts."""
    scripts = package_json.get("scripts", {})
    assert "dev" in scripts, "Missing 'dev' script"
    assert "build" in scripts, "Missing 'build' script"
    assert "preview" in scripts, "Missing 'preview' script"


def test_package_json_no_ui_library(package_json: Dict[str, Any]) -> None:
    """No external UI library should be present (e.g. MUI, Chakra, Ant)."""
    all_deps = {}
    all_deps.update(package_json.get("dependencies", {}))
    all_deps.update(package_json.get("devDependencies", {}))

    forbidden = [
        "@mui/material",
        "@chakra-ui/react",
        "antd",
        "bootstrap",
        "tailwindcss",
        "@emotion/react",
        "styled-components",
    ]
    for lib in forbidden:
        assert lib not in all_deps, f"Forbidden UI library found: {lib}"


def test_package_json_is_private(package_json: Dict[str, Any]) -> None:
    """package.json must have private set to true."""
    assert package_json.get("private") is True


# ------------------------------------------------------------------
# tsconfig.json
# ------------------------------------------------------------------


def test_tsconfig_strict() -> None:
    """tsconfig.json must have strict mode enabled."""
    tsconfig = _load_json(ROOT / "tsconfig.json")
    compiler_opts = tsconfig.get("compilerOptions", {})
    assert compiler_opts.get("strict") is True


def test_tsconfig_jsx_react_jsx() -> None:
    """tsconfig.json must set jsx to react-jsx."""
    tsconfig = _load_json(ROOT / "tsconfig.json")
    compiler_opts = tsconfig.get("compilerOptions", {})
    assert compiler_opts.get("jsx") == "react-jsx"


def test_tsconfig_includes_src() -> None:
    """tsconfig.json must include the src directory."""
    tsconfig = _load_json(ROOT / "tsconfig.json")
    includes = tsconfig.get("include", [])
    assert "src" in includes


# ------------------------------------------------------------------
# vite.config.ts
# ------------------------------------------------------------------


def test_vite_config_uses_react_plugin() -> None:
    """vite.config.ts must import and use the React plugin."""
    content = _read_text(ROOT / "vite.config.ts")
    assert "@vitejs/plugin-react" in content
    assert "react()" in content


def test_vite_config_port_3000() -> None:
    """vite.config.ts must configure the dev server on port 3000."""
    content = _read_text(ROOT / "vite.config.ts")
    assert "3000" in content


# ------------------------------------------------------------------
# index.html
# ------------------------------------------------------------------


def test_index_html_has_root_div() -> None:
    """index.html must contain a div with id='root'."""
    content = _read_text(ROOT / "index.html")
    assert 'id="root"' in content


def test_index_html_references_main_tsx() -> None:
    """index.html must reference /src/main.tsx as a module script."""
    content = _read_text(ROOT / "index.html")
    assert 'src="/src/main.tsx"' in content
    assert 'type="module"' in content


def test_index_html_has_lang_en() -> None:
    """index.html must set the lang attribute to 'en'."""
    content = _read_text(ROOT / "index.html")
    assert 'lang="en"' in content


def test_index_html_has_charset() -> None:
    """index.html must declare UTF-8 charset."""
    content = _read_text(ROOT / "index.html")
    assert 'charset="UTF-8"' in content or 'charset="utf-8"' in content


def test_index_html_has_viewport_meta() -> None:
    """index.html must include a viewport meta tag."""
    content = _read_text(ROOT / "index.html")
    assert "viewport" in content


# ------------------------------------------------------------------
# src/main.tsx
# ------------------------------------------------------------------


def test_main_tsx_imports_react_dom() -> None:
    """src/main.tsx must import from react-dom/client."""
    content = _read_text(ROOT / "src" / "main.tsx")
    assert "react-dom/client" in content


def test_main_tsx_imports_app() -> None:
    """src/main.tsx must import the App component."""
    content = _read_text(ROOT / "src" / "main.tsx")
    assert "import App" in content or "import { App }" in content


def test_main_tsx_creates_root() -> None:
    """src/main.tsx must call createRoot."""
    content = _read_text(ROOT / "src" / "main.tsx")
    assert "createRoot" in content


def test_main_tsx_uses_strict_mode() -> None:
    """src/main.tsx must wrap App in React.StrictMode."""
    content = _read_text(ROOT / "src" / "main.tsx")
    assert "StrictMode" in content


def test_main_tsx_targets_root_element() -> None:
    """src/main.tsx must target the element with id 'root'."""
    content = _read_text(ROOT / "src" / "main.tsx")
    assert "getElementById('root')" in content or 'getElementById("root")' in content


# ------------------------------------------------------------------
# src/App.tsx — the core deliverable
# ------------------------------------------------------------------


def test_app_tsx_renders_hello_world() -> None:
    """src/App.tsx must contain the exact text 'Hello World'."""
    content = _read_text(ROOT / "src" / "App.tsx")
    assert "Hello World" in content


def test_app_tsx_uses_h1() -> None:
    """src/App.tsx must render an <h1> element."""
    content = _read_text(ROOT / "src" / "App.tsx")
    assert "<h1>" in content


def test_app_tsx_exports_default() -> None:
    """src/App.tsx must have a default export."""
    content = _read_text(ROOT / "src" / "App.tsx")
    assert "export default" in content


def test_app_tsx_has_centering_styles() -> None:
    """src/App.tsx must use flexbox centering (display flex, justify-content, align-items)."""
    content = _read_text(ROOT / "src" / "App.tsx")
    # Check for inline style properties (camelCase for React)
    assert "display" in content and "flex" in content.lower(), (
        "Expected display: 'flex' for centering"
    )
    assert "justifyContent" in content or "justify-content" in content, (
        "Expected justifyContent for horizontal centering"
    )
    assert "alignItems" in content or "align-items" in content, (
        "Expected alignItems for vertical centering"
    )


def test_app_tsx_has_full_viewport_height() -> None:
    """src/App.tsx must set min-height to 100vh for full-viewport centering."""
    content = _read_text(ROOT / "src" / "App.tsx")
    assert "100vh" in content, "Expected minHeight: '100vh' for full viewport"


def test_app_tsx_defines_app_function() -> None:
    """src/App.tsx must define a function named App."""
    content = _read_text(ROOT / "src" / "App.tsx")
    assert "function App" in content


def test_app_tsx_has_docstring_or_comment() -> None:
    """src/App.tsx must have a descriptive comment or JSDoc."""
    content = _read_text(ROOT / "src" / "App.tsx")
    assert "/**" in content or "//" in content, "Expected a comment/docstring in App.tsx"


def test_app_tsx_no_external_imports() -> None:
    """src/App.tsx must not import from external UI libraries."""
    content = _read_text(ROOT / "src" / "App.tsx")
    forbidden_imports = [
        "@mui",
        "@chakra",
        "antd",
        "bootstrap",
        "tailwind",
        "styled-components",
    ]
    for lib in forbidden_imports:
        assert lib not in content, f"Forbidden import found: {lib}"


# ------------------------------------------------------------------
# RUNNING.md
# ------------------------------------------------------------------


def test_running_md_exists() -> None:
    """RUNNING.md must exist at the repository root."""
    assert (ROOT / "RUNNING.md").exists()


def test_running_md_has_npm_install() -> None:
    """RUNNING.md must document 'npm install'."""
    content = _read_text(ROOT / "RUNNING.md")
    assert "npm install" in content


def test_running_md_has_npm_run_dev() -> None:
    """RUNNING.md must document 'npm run dev'."""
    content = _read_text(ROOT / "RUNNING.md")
    assert "npm run dev" in content


def test_running_md_has_npm_run_build() -> None:
    """RUNNING.md must document 'npm run build'."""
    content = _read_text(ROOT / "RUNNING.md")
    assert "npm run build" in content
