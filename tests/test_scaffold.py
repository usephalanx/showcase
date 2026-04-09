"""Tests to validate the project scaffold configuration files exist and are correct."""

import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent


def test_package_json_exists() -> None:
    """Verify package.json exists at project root."""
    assert (ROOT / "package.json").is_file()


def test_package_json_has_required_scripts() -> None:
    """Verify package.json contains dev, build, preview, and test scripts."""
    with open(ROOT / "package.json", encoding="utf-8") as f:
        pkg = json.load(f)
    scripts = pkg.get("scripts", {})
    for script_name in ("dev", "build", "preview", "test"):
        assert script_name in scripts, f"Missing script: {script_name}"


def test_package_json_has_react_dependencies() -> None:
    """Verify package.json lists react and react-dom as dependencies."""
    with open(ROOT / "package.json", encoding="utf-8") as f:
        pkg = json.load(f)
    deps = pkg.get("dependencies", {})
    assert "react" in deps
    assert "react-dom" in deps


def test_package_json_has_dev_dependencies() -> None:
    """Verify package.json lists required dev dependencies."""
    with open(ROOT / "package.json", encoding="utf-8") as f:
        pkg = json.load(f)
    dev_deps = pkg.get("devDependencies", {})
    required = [
        "typescript",
        "vite",
        "@vitejs/plugin-react",
        "vitest",
        "@testing-library/react",
        "@testing-library/jest-dom",
        "jsdom",
    ]
    for dep in required:
        assert dep in dev_deps, f"Missing devDependency: {dep}"


def test_tsconfig_json_exists() -> None:
    """Verify tsconfig.json exists at project root."""
    assert (ROOT / "tsconfig.json").is_file()


def test_tsconfig_strict_mode() -> None:
    """Verify tsconfig.json has strict mode enabled."""
    with open(ROOT / "tsconfig.json", encoding="utf-8") as f:
        tsconfig = json.load(f)
    compiler_options = tsconfig.get("compilerOptions", {})
    assert compiler_options.get("strict") is True


def test_tsconfig_jsx_support() -> None:
    """Verify tsconfig.json has JSX set to react-jsx."""
    with open(ROOT / "tsconfig.json", encoding="utf-8") as f:
        tsconfig = json.load(f)
    compiler_options = tsconfig.get("compilerOptions", {})
    assert compiler_options.get("jsx") == "react-jsx"


def test_tsconfig_target() -> None:
    """Verify tsconfig.json targets ES2020."""
    with open(ROOT / "tsconfig.json", encoding="utf-8") as f:
        tsconfig = json.load(f)
    compiler_options = tsconfig.get("compilerOptions", {})
    assert compiler_options.get("target") == "ES2020"


def test_tsconfig_module_resolution() -> None:
    """Verify tsconfig.json uses bundler module resolution."""
    with open(ROOT / "tsconfig.json", encoding="utf-8") as f:
        tsconfig = json.load(f)
    compiler_options = tsconfig.get("compilerOptions", {})
    assert compiler_options.get("moduleResolution") == "bundler"


def test_tsconfig_includes_src() -> None:
    """Verify tsconfig.json includes the src directory."""
    with open(ROOT / "tsconfig.json", encoding="utf-8") as f:
        tsconfig = json.load(f)
    assert "src" in tsconfig.get("include", [])


def test_vite_config_exists() -> None:
    """Verify vite.config.ts exists at project root."""
    assert (ROOT / "vite.config.ts").is_file()


def test_vite_config_has_react_plugin() -> None:
    """Verify vite.config.ts imports and uses the React plugin."""
    content = (ROOT / "vite.config.ts").read_text(encoding="utf-8")
    assert "@vitejs/plugin-react" in content
    assert "react()" in content


def test_vite_config_has_test_block() -> None:
    """Verify vite.config.ts includes vitest test configuration."""
    content = (ROOT / "vite.config.ts").read_text(encoding="utf-8")
    assert "test" in content
    assert "jsdom" in content
    assert "setupFiles" in content


def test_index_html_exists() -> None:
    """Verify index.html exists at project root."""
    assert (ROOT / "index.html").is_file()


def test_index_html_has_root_div() -> None:
    """Verify index.html contains a div with id root."""
    content = (ROOT / "index.html").read_text(encoding="utf-8")
    assert 'id="root"' in content


def test_index_html_has_module_script() -> None:
    """Verify index.html contains a module script pointing to main.tsx."""
    content = (ROOT / "index.html").read_text(encoding="utf-8")
    assert 'type="module"' in content
    assert 'src="/src/main.tsx"' in content


def test_main_tsx_exists() -> None:
    """Verify src/main.tsx exists."""
    assert (ROOT / "src" / "main.tsx").is_file()


def test_main_tsx_imports_react_dom() -> None:
    """Verify src/main.tsx imports ReactDOM."""
    content = (ROOT / "src" / "main.tsx").read_text(encoding="utf-8")
    assert "react-dom" in content


def test_main_tsx_creates_root() -> None:
    """Verify src/main.tsx calls createRoot."""
    content = (ROOT / "src" / "main.tsx").read_text(encoding="utf-8")
    assert "createRoot" in content


def test_app_tsx_exists() -> None:
    """Verify src/App.tsx exists."""
    assert (ROOT / "src" / "App.tsx").is_file()


def test_app_tsx_has_hello_world() -> None:
    """Verify src/App.tsx renders Hello World."""
    content = (ROOT / "src" / "App.tsx").read_text(encoding="utf-8")
    assert "Hello World" in content


def test_app_tsx_has_counter_state() -> None:
    """Verify src/App.tsx uses useState for counter."""
    content = (ROOT / "src" / "App.tsx").read_text(encoding="utf-8")
    assert "useState" in content
    assert "count" in content


def test_app_css_exists() -> None:
    """Verify src/App.css exists."""
    assert (ROOT / "src" / "App.css").is_file()


def test_setup_tests_exists() -> None:
    """Verify src/setupTests.ts exists."""
    assert (ROOT / "src" / "setupTests.ts").is_file()


def test_setup_tests_imports_jest_dom() -> None:
    """Verify src/setupTests.ts imports jest-dom."""
    content = (ROOT / "src" / "setupTests.ts").read_text(encoding="utf-8")
    assert "@testing-library/jest-dom" in content


def test_app_test_exists() -> None:
    """Verify src/App.test.tsx exists."""
    assert (ROOT / "src" / "App.test.tsx").is_file()


def test_app_test_has_hello_world_test() -> None:
    """Verify src/App.test.tsx includes a Hello World heading test."""
    content = (ROOT / "src" / "App.test.tsx").read_text(encoding="utf-8")
    assert "Hello World" in content


def test_app_test_has_counter_tests() -> None:
    """Verify src/App.test.tsx includes counter tests."""
    content = (ROOT / "src" / "App.test.tsx").read_text(encoding="utf-8")
    assert "Count: 0" in content
    assert "Count: 1" in content
    assert "Count: 2" in content
