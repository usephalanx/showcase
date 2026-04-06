"""Structural tests for the frontend project setup.

Validates that all required frontend files exist and contain the
expected configuration / content.
"""

import json
import pathlib

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent
FRONTEND = ROOT / "frontend"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _read(path: pathlib.Path) -> str:
    """Read a file and return its content as a string."""
    assert path.exists(), f"File not found: {path}"
    return path.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# File existence
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "relative",
    [
        "package.json",
        "tsconfig.json",
        "tsconfig.node.json",
        "vite.config.ts",
        "index.html",
        "src/main.tsx",
        "src/App.tsx",
        "src/index.css",
    ],
)
def test_file_exists(relative: str) -> None:
    """Each expected frontend file must exist."""
    assert (FRONTEND / relative).exists(), f"Missing: frontend/{relative}"


# ---------------------------------------------------------------------------
# package.json
# ---------------------------------------------------------------------------

def test_package_json_has_dependencies() -> None:
    """package.json must list react, react-dom, axios as dependencies."""
    data = json.loads(_read(FRONTEND / "package.json"))
    deps = data.get("dependencies", {})
    for dep in ["react", "react-dom", "axios"]:
        assert dep in deps, f"Missing dependency: {dep}"


def test_package_json_has_dev_dependencies() -> None:
    """package.json must list typescript and vite as devDependencies."""
    data = json.loads(_read(FRONTEND / "package.json"))
    dev_deps = data.get("devDependencies", {})
    for dep in ["typescript", "vite"]:
        assert dep in dev_deps, f"Missing devDependency: {dep}"


def test_package_json_scripts() -> None:
    """package.json must define dev, build, and preview scripts."""
    data = json.loads(_read(FRONTEND / "package.json"))
    scripts = data.get("scripts", {})
    for script in ["dev", "build", "preview"]:
        assert script in scripts, f"Missing script: {script}"


# ---------------------------------------------------------------------------
# vite.config.ts
# ---------------------------------------------------------------------------

def test_vite_config_has_proxy() -> None:
    """vite.config.ts must proxy /api to localhost:8000."""
    content = _read(FRONTEND / "vite.config.ts")
    assert "/api" in content, "Vite config missing /api proxy"
    assert "localhost:8000" in content, "Vite config missing localhost:8000 target"


def test_vite_config_uses_react_plugin() -> None:
    """vite.config.ts must import and use the React plugin."""
    content = _read(FRONTEND / "vite.config.ts")
    assert "@vitejs/plugin-react" in content
    assert "react()" in content


# ---------------------------------------------------------------------------
# tsconfig.json
# ---------------------------------------------------------------------------

def test_tsconfig_strict_mode() -> None:
    """tsconfig.json must enable strict mode."""
    data = json.loads(_read(FRONTEND / "tsconfig.json"))
    compiler = data.get("compilerOptions", {})
    assert compiler.get("strict") is True


def test_tsconfig_jsx() -> None:
    """tsconfig.json must set jsx to react-jsx."""
    data = json.loads(_read(FRONTEND / "tsconfig.json"))
    compiler = data.get("compilerOptions", {})
    assert compiler.get("jsx") == "react-jsx"


# ---------------------------------------------------------------------------
# index.html
# ---------------------------------------------------------------------------

def test_index_html_has_root_div() -> None:
    """index.html must contain a div#root mount point."""
    content = _read(FRONTEND / "index.html")
    assert 'id="root"' in content


def test_index_html_references_main_tsx() -> None:
    """index.html must reference /src/main.tsx."""
    content = _read(FRONTEND / "index.html")
    assert "/src/main.tsx" in content


# ---------------------------------------------------------------------------
# main.tsx
# ---------------------------------------------------------------------------

def test_main_tsx_imports_app() -> None:
    """main.tsx must import the App component."""
    content = _read(FRONTEND / "src/main.tsx")
    assert "import App" in content or "import { App }" in content


def test_main_tsx_imports_css() -> None:
    """main.tsx must import the global CSS file."""
    content = _read(FRONTEND / "src/main.tsx")
    assert "index.css" in content


def test_main_tsx_uses_strict_mode() -> None:
    """main.tsx must render inside React.StrictMode."""
    content = _read(FRONTEND / "src/main.tsx")
    assert "StrictMode" in content


# ---------------------------------------------------------------------------
# App.tsx
# ---------------------------------------------------------------------------

def test_app_tsx_is_functional_component() -> None:
    """App.tsx must export a functional React component."""
    content = _read(FRONTEND / "src/App.tsx")
    assert "React.FC" in content or "function App" in content
    assert "export default" in content


# ---------------------------------------------------------------------------
# index.css
# ---------------------------------------------------------------------------

def test_css_has_reset() -> None:
    """index.css must include a CSS reset (box-sizing rule)."""
    content = _read(FRONTEND / "src/index.css")
    assert "box-sizing" in content


def test_css_has_system_font_stack() -> None:
    """index.css must use a system font stack."""
    content = _read(FRONTEND / "src/index.css")
    # Check for at least one system-font keyword
    assert "-apple-system" in content or "system-ui" in content


def test_css_has_custom_properties() -> None:
    """index.css must define CSS custom properties for the color palette."""
    content = _read(FRONTEND / "src/index.css")
    assert "--color-gray" in content
