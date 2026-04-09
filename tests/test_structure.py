"""Structural tests for the React Hello World project.

Validates that all required files exist with the correct content markers.
These tests run with pytest and inspect the repository files on disk.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

# Repository root is one level above the tests/ directory.
ROOT: Path = Path(__file__).resolve().parent.parent


def _read(relative_path: str) -> str:
    """Read and return the text content of a file relative to the repo root."""
    path = ROOT / relative_path
    assert path.exists(), f"Expected file not found: {relative_path}"
    return path.read_text(encoding="utf-8")


def _load_package_json() -> Dict[str, Any]:
    """Parse and return the package.json as a dictionary."""
    content = _read("package.json")
    return json.loads(content)


# --------------------------------------------------------------------------
# package.json
# --------------------------------------------------------------------------


def test_package_json_exists() -> None:
    """package.json must exist at the repository root."""
    assert (ROOT / "package.json").exists()


def test_package_json_has_react_dependency() -> None:
    """package.json must list react as a dependency."""
    pkg = _load_package_json()
    assert "react" in pkg.get("dependencies", {})


def test_package_json_has_react_dom_dependency() -> None:
    """package.json must list react-dom as a dependency."""
    pkg = _load_package_json()
    assert "react-dom" in pkg.get("dependencies", {})


def test_package_json_has_vite_dev_dependency() -> None:
    """package.json must list vite as a devDependency."""
    pkg = _load_package_json()
    assert "vite" in pkg.get("devDependencies", {})


def test_package_json_has_typescript_dev_dependency() -> None:
    """package.json must list typescript as a devDependency."""
    pkg = _load_package_json()
    assert "typescript" in pkg.get("devDependencies", {})


def test_package_json_has_react_plugin_dev_dependency() -> None:
    """package.json must list @vitejs/plugin-react as a devDependency."""
    pkg = _load_package_json()
    assert "@vitejs/plugin-react" in pkg.get("devDependencies", {})


def test_package_json_has_dev_script() -> None:
    """package.json scripts.dev must be 'vite'."""
    pkg = _load_package_json()
    assert pkg.get("scripts", {}).get("dev") == "vite"


def test_package_json_has_build_script() -> None:
    """package.json scripts.build must be 'tsc && vite build'."""
    pkg = _load_package_json()
    assert pkg.get("scripts", {}).get("build") == "tsc && vite build"


def test_package_json_has_preview_script() -> None:
    """package.json scripts.preview must be 'vite preview'."""
    pkg = _load_package_json()
    assert pkg.get("scripts", {}).get("preview") == "vite preview"


def test_package_json_type_module() -> None:
    """package.json must set type to 'module'."""
    pkg = _load_package_json()
    assert pkg.get("type") == "module"


# --------------------------------------------------------------------------
# vite.config.ts
# --------------------------------------------------------------------------


def test_vite_config_exists() -> None:
    """vite.config.ts must exist at the repository root."""
    assert (ROOT / "vite.config.ts").exists()


def test_vite_config_imports_react_plugin() -> None:
    """vite.config.ts must import the React plugin."""
    content = _read("vite.config.ts")
    assert "@vitejs/plugin-react" in content


def test_vite_config_uses_define_config() -> None:
    """vite.config.ts must use defineConfig."""
    content = _read("vite.config.ts")
    assert "defineConfig" in content


def test_vite_config_uses_react_plugin() -> None:
    """vite.config.ts must include react() in plugins."""
    content = _read("vite.config.ts")
    assert "plugins" in content
    assert "react()" in content


# --------------------------------------------------------------------------
# tsconfig.json
# --------------------------------------------------------------------------


def test_tsconfig_exists() -> None:
    """tsconfig.json must exist at the repository root."""
    assert (ROOT / "tsconfig.json").exists()


def test_tsconfig_react_jsx() -> None:
    """tsconfig.json must set jsx to 'react-jsx'."""
    content = _read("tsconfig.json")
    cfg = json.loads(content)
    assert cfg.get("compilerOptions", {}).get("jsx") == "react-jsx"


def test_tsconfig_strict() -> None:
    """tsconfig.json must enable strict mode."""
    content = _read("tsconfig.json")
    cfg = json.loads(content)
    assert cfg.get("compilerOptions", {}).get("strict") is True


def test_tsconfig_includes_src() -> None:
    """tsconfig.json must include the 'src' directory."""
    content = _read("tsconfig.json")
    cfg = json.loads(content)
    assert "src" in cfg.get("include", [])


# --------------------------------------------------------------------------
# index.html
# --------------------------------------------------------------------------


def test_index_html_exists() -> None:
    """index.html must exist at the repository root."""
    assert (ROOT / "index.html").exists()


def test_index_html_has_root_div() -> None:
    """index.html must contain a div with id='root'."""
    content = _read("index.html")
    assert 'id="root"' in content


def test_index_html_references_main_tsx() -> None:
    """index.html must reference src/main.tsx as a module script."""
    content = _read("index.html")
    assert 'src="/src/main.tsx"' in content
    assert 'type="module"' in content


def test_index_html_has_doctype() -> None:
    """index.html must start with a DOCTYPE declaration."""
    content = _read("index.html")
    assert content.strip().startswith("<!DOCTYPE html>")


def test_index_html_has_title() -> None:
    """index.html must include a <title> element."""
    content = _read("index.html")
    assert "<title>" in content


# --------------------------------------------------------------------------
# src/App.tsx
# --------------------------------------------------------------------------


def test_app_tsx_exists() -> None:
    """src/App.tsx must exist."""
    assert (ROOT / "src" / "App.tsx").exists()


def test_app_tsx_has_hello_world() -> None:
    """src/App.tsx must render 'Hello World' in an h1 element."""
    content = _read("src/App.tsx")
    assert "Hello World" in content
    assert "<h1>" in content or "<h1 " in content


def test_app_tsx_has_default_export() -> None:
    """src/App.tsx must have a default export."""
    content = _read("src/App.tsx")
    assert "export default" in content


def test_app_tsx_has_flex_centering() -> None:
    """src/App.tsx must use flex centering styles."""
    content = _read("src/App.tsx")
    assert "display" in content
    assert "flex" in content
    assert "justifyContent" in content
    assert "alignItems" in content
    assert "center" in content


def test_app_tsx_has_min_height_100vh() -> None:
    """src/App.tsx must set minHeight to 100vh on the wrapper div."""
    content = _read("src/App.tsx")
    assert "minHeight" in content
    assert "100vh" in content


def test_app_tsx_function_component() -> None:
    """src/App.tsx must define App as a function component."""
    content = _read("src/App.tsx")
    assert "function App" in content


def test_app_tsx_has_type_annotation() -> None:
    """src/App.tsx App function must have a JSX.Element return type."""
    content = _read("src/App.tsx")
    assert "JSX.Element" in content


# --------------------------------------------------------------------------
# src/main.tsx
# --------------------------------------------------------------------------


def test_main_tsx_exists() -> None:
    """src/main.tsx must exist."""
    assert (ROOT / "src" / "main.tsx").exists()


def test_main_tsx_imports_react() -> None:
    """src/main.tsx must import React."""
    content = _read("src/main.tsx")
    assert "import React" in content


def test_main_tsx_imports_react_dom() -> None:
    """src/main.tsx must import ReactDOM from react-dom/client."""
    content = _read("src/main.tsx")
    assert "react-dom/client" in content


def test_main_tsx_imports_app() -> None:
    """src/main.tsx must import the App component."""
    content = _read("src/main.tsx")
    assert "import App" in content
    assert "./App" in content


def test_main_tsx_uses_create_root() -> None:
    """src/main.tsx must call createRoot."""
    content = _read("src/main.tsx")
    assert "createRoot" in content


def test_main_tsx_targets_root_element() -> None:
    """src/main.tsx must target the element with id 'root'."""
    content = _read("src/main.tsx")
    assert "getElementById('root')" in content or 'getElementById("root")' in content


def test_main_tsx_renders_app() -> None:
    """src/main.tsx must render <App />."""
    content = _read("src/main.tsx")
    assert "<App />" in content or "<App/>" in content


def test_main_tsx_uses_strict_mode() -> None:
    """src/main.tsx must use React.StrictMode."""
    content = _read("src/main.tsx")
    assert "StrictMode" in content


def test_main_tsx_is_minimal() -> None:
    """src/main.tsx should be minimal — no unnecessary imports."""
    content = _read("src/main.tsx")
    lines = [line.strip() for line in content.strip().splitlines() if line.strip()]
    # Expect roughly 3 imports + the render call (a few lines)
    assert len(lines) <= 10, f"main.tsx has {len(lines)} non-empty lines, expected <= 10"
