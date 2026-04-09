"""Tests for the TodoInput React component.

Validates that the component source contains the correct structure,
props interface, state management, and submission logic.
"""

from pathlib import Path

import pytest

COMPONENT_PATH = Path(__file__).resolve().parent.parent / "src" / "components" / "TodoInput.tsx"


@pytest.fixture()
def component_source() -> str:
    """Read and return the TodoInput component source code."""
    assert COMPONENT_PATH.exists(), f"TodoInput.tsx not found at {COMPONENT_PATH}"
    return COMPONENT_PATH.read_text(encoding="utf-8")


class TestTodoInputExists:
    """Verify the component file exists and is non-empty."""

    def test_file_exists(self) -> None:
        """TodoInput.tsx must exist at the expected path."""
        assert COMPONENT_PATH.exists()

    def test_file_not_empty(self, component_source: str) -> None:
        """TodoInput.tsx must contain content."""
        assert len(component_source.strip()) > 0


class TestTodoInputPropsInterface:
    """Verify the props interface is properly defined."""

    def test_defines_todo_input_props(self, component_source: str) -> None:
        """Component must export a TodoInputProps interface."""
        assert "TodoInputProps" in component_source

    def test_on_add_prop_defined(self, component_source: str) -> None:
        """Props interface must include an onAdd callback."""
        assert "onAdd" in component_source

    def test_on_add_accepts_string(self, component_source: str) -> None:
        """onAdd must accept a string parameter."""
        assert "(text: string)" in component_source or "(text:string)" in component_source


class TestTodoInputStateManagement:
    """Verify the component uses local state for the input value."""

    def test_uses_use_state(self, component_source: str) -> None:
        """Component must use useState hook."""
        assert "useState" in component_source

    def test_imports_use_state(self, component_source: str) -> None:
        """useState must be imported from react."""
        assert "useState" in component_source
        assert "react" in component_source.lower() or "React" in component_source

    def test_state_initialized_empty(self, component_source: str) -> None:
        """The input state must be initialized to an empty string."""
        assert 'useState("")' in component_source or "useState('')" in component_source or 'useState<string>("")' in component_source or "useState<string>('')" in component_source


class TestTodoInputFormStructure:
    """Verify the component renders a form with input and button."""

    def test_renders_form_element(self, component_source: str) -> None:
        """Component must render a <form> element."""
        assert "<form" in component_source

    def test_form_has_on_submit(self, component_source: str) -> None:
        """Form must have an onSubmit handler."""
        assert "onSubmit" in component_source

    def test_renders_input_element(self, component_source: str) -> None:
        """Component must render an <input> element."""
        assert "<input" in component_source

    def test_input_is_text_type(self, component_source: str) -> None:
        """Input element must be of type text."""
        assert 'type="text"' in component_source or "type='text'" in component_source

    def test_input_is_controlled(self, component_source: str) -> None:
        """Input must have value prop bound to state (controlled component)."""
        assert "value={text}" in component_source or "value={ text }" in component_source

    def test_input_has_on_change(self, component_source: str) -> None:
        """Input must have an onChange handler."""
        assert "onChange" in component_source

    def test_renders_submit_button(self, component_source: str) -> None:
        """Component must render a submit button."""
        assert "<button" in component_source
        assert 'type="submit"' in component_source or "type='submit'" in component_source


class TestTodoInputSubmissionLogic:
    """Verify submission behavior: prevent empty, call onAdd, clear input."""

    def test_prevents_default_form_behavior(self, component_source: str) -> None:
        """Form submit handler must call preventDefault."""
        assert "preventDefault" in component_source

    def test_trims_input_text(self, component_source: str) -> None:
        """Component must trim whitespace before validation."""
        assert "trim()" in component_source

    def test_prevents_empty_submission(self, component_source: str) -> None:
        """Component must check for empty text and return early."""
        assert "length" in component_source or '=== ""' in component_source or "=== ''" in component_source

    def test_calls_on_add(self, component_source: str) -> None:
        """Component must call onAdd with the text."""
        assert "onAdd(" in component_source

    def test_clears_input_after_submit(self, component_source: str) -> None:
        """Component must reset text state to empty string after submission."""
        assert 'setText("")' in component_source or "setText('')" in component_source


class TestTodoInputExport:
    """Verify the component is properly exported."""

    def test_default_export(self, component_source: str) -> None:
        """Component must have a default export."""
        assert "export default" in component_source

    def test_exports_todo_input(self, component_source: str) -> None:
        """Default export must be TodoInput."""
        assert "export default TodoInput" in component_source


class TestTodoInputAccessibility:
    """Verify basic accessibility features."""

    def test_input_has_placeholder(self, component_source: str) -> None:
        """Input should have a placeholder for usability."""
        assert "placeholder" in component_source

    def test_input_has_aria_label(self, component_source: str) -> None:
        """Input should have an aria-label for screen readers."""
        assert "aria-label" in component_source
