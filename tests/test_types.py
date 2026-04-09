"""Tests for src/types.ts — Todo interface definition.

Verifies that the types.ts file exists, exports the Todo interface,
and that the interface has the correct fields with correct types.
"""

import re
from pathlib import Path

TYPES_FILE = Path(__file__).resolve().parent.parent / "src" / "types.ts"


def test_types_file_exists() -> None:
    """src/types.ts must exist."""
    assert TYPES_FILE.exists(), f"Expected {TYPES_FILE} to exist"


def test_types_file_exports_todo_interface() -> None:
    """src/types.ts must export a Todo interface."""
    content = TYPES_FILE.read_text(encoding="utf-8")
    assert re.search(r"export\s+interface\s+Todo\b", content), (
        "types.ts must contain 'export interface Todo'"
    )


def test_todo_interface_has_id_string() -> None:
    """Todo interface must have an 'id' field of type string."""
    content = TYPES_FILE.read_text(encoding="utf-8")
    assert re.search(r"id\s*:\s*string", content), (
        "Todo interface must have 'id: string'"
    )


def test_todo_interface_has_text_string() -> None:
    """Todo interface must have a 'text' field of type string."""
    content = TYPES_FILE.read_text(encoding="utf-8")
    assert re.search(r"text\s*:\s*string", content), (
        "Todo interface must have 'text: string'"
    )


def test_todo_interface_has_completed_boolean() -> None:
    """Todo interface must have a 'completed' field of type boolean."""
    content = TYPES_FILE.read_text(encoding="utf-8")
    assert re.search(r"completed\s*:\s*boolean", content), (
        "Todo interface must have 'completed: boolean'"
    )


def test_todo_interface_has_exactly_three_fields() -> None:
    """Todo interface must declare exactly three fields: id, text, completed."""
    content = TYPES_FILE.read_text(encoding="utf-8")
    # Extract the interface body
    match = re.search(
        r"export\s+interface\s+Todo\s*\{([^}]*)\}", content, re.DOTALL
    )
    assert match, "Could not find Todo interface body"
    body = match.group(1)
    # Count field declarations (lines with word: type pattern)
    fields = re.findall(r"\b(\w+)\s*:\s*\w+", body)
    field_names = [f for f in fields]
    assert sorted(field_names) == ["completed", "id", "text"], (
        f"Expected exactly [completed, id, text] fields, got {sorted(field_names)}"
    )
