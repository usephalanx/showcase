"""Python-level tests verifying App component source files exist and are well-formed.

These tests validate the static structure of the React component files
without requiring a Node.js runtime.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def test_app_tsx_exists() -> None:
    """Verify src/App.tsx exists."""
    app_path = ROOT / "src" / "App.tsx"
    assert app_path.is_file(), "src/App.tsx should exist"


def test_app_css_exists() -> None:
    """Verify src/App.css exists."""
    css_path = ROOT / "src" / "App.css"
    assert css_path.is_file(), "src/App.css should exist"


def test_app_tsx_contains_hello_world() -> None:
    """Verify App.tsx renders an h1 with Hello World."""
    content = (ROOT / "src" / "App.tsx").read_text()
    assert "<h1>Hello World</h1>" in content, "App.tsx must contain <h1>Hello World</h1>"


def test_app_tsx_uses_usestate() -> None:
    """Verify App.tsx imports and uses useState."""
    content = (ROOT / "src" / "App.tsx").read_text()
    assert "useState" in content, "App.tsx must use useState hook"


def test_app_tsx_has_counter_button() -> None:
    """Verify App.tsx renders a button that displays the count."""
    content = (ROOT / "src" / "App.tsx").read_text()
    assert "Count:" in content, "App.tsx must display 'Count:' in a button"
    assert "<button" in content, "App.tsx must contain a <button> element"


def test_app_tsx_has_setcount_increment() -> None:
    """Verify App.tsx increments count via setCount."""
    content = (ROOT / "src" / "App.tsx").read_text()
    assert "setCount" in content, "App.tsx must call setCount"


def test_app_css_has_flexbox_centering() -> None:
    """Verify App.css uses flexbox for centering."""
    content = (ROOT / "src" / "App.css").read_text()
    assert "display: flex" in content, "App.css must use display: flex"
    assert "justify-content: center" in content, "App.css must center horizontally"
    assert "align-items: center" in content, "App.css must center vertically"


def test_app_css_has_button_hover() -> None:
    """Verify App.css styles the button hover state."""
    content = (ROOT / "src" / "App.css").read_text()
    assert "button:hover" in content, "App.css must include button:hover styles"


def test_app_css_has_button_styling() -> None:
    """Verify App.css styles buttons with padding, font-size, cursor, and border-radius."""
    content = (ROOT / "src" / "App.css").read_text()
    assert "padding:" in content, "App.css must set button padding"
    assert "font-size:" in content, "App.css must set button font-size"
    assert "cursor: pointer" in content, "App.css must set cursor: pointer on button"
    assert "border-radius:" in content, "App.css must set border-radius on button"


def test_app_tsx_imports_css() -> None:
    """Verify App.tsx imports App.css."""
    content = (ROOT / "src" / "App.tsx").read_text()
    assert "import './App.css'" in content, "App.tsx must import './App.css'"


def test_app_tsx_default_export() -> None:
    """Verify App.tsx has a default export."""
    content = (ROOT / "src" / "App.tsx").read_text()
    assert "export default App" in content, "App.tsx must export App as default"


def test_main_tsx_exists() -> None:
    """Verify src/main.tsx exists as the entry point."""
    main_path = ROOT / "src" / "main.tsx"
    assert main_path.is_file(), "src/main.tsx should exist"


def test_index_html_exists() -> None:
    """Verify index.html exists as the HTML entry point."""
    index_path = ROOT / "index.html"
    assert index_path.is_file(), "index.html should exist"


def test_index_html_has_root_div() -> None:
    """Verify index.html contains a root div for React mounting."""
    content = (ROOT / "index.html").read_text()
    assert 'id="root"' in content, "index.html must contain a div with id='root'"
