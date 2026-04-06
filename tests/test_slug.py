"""Tests for slug generation utilities."""

from __future__ import annotations

import pytest

from slug import generate_slug, generate_unique_slug


class TestGenerateSlug:
    """Test suite for the generate_slug function."""

    def test_basic_title(self) -> None:
        """Test basic title conversion to slug."""
        assert generate_slug("My Board Title") == "my-board-title"

    def test_extra_whitespace(self) -> None:
        """Test that extra whitespace is normalized."""
        assert generate_slug("  Hello   World!!  ") == "hello-world"

    def test_special_characters_removed(self) -> None:
        """Test that special characters are removed."""
        assert generate_slug("Hello@World#2024!") == "helloworld2024"

    def test_underscores_become_hyphens(self) -> None:
        """Test that underscores are converted to hyphens."""
        assert generate_slug("my_board_title") == "my-board-title"

    def test_consecutive_hyphens_collapsed(self) -> None:
        """Test that consecutive hyphens are collapsed."""
        assert generate_slug("hello---world") == "hello-world"

    def test_leading_trailing_hyphens_stripped(self) -> None:
        """Test that leading/trailing hyphens are stripped."""
        assert generate_slug("---hello---") == "hello"

    def test_numeric_title(self) -> None:
        """Test that numeric titles produce valid slugs."""
        assert generate_slug("2024 Board") == "2024-board"

    def test_empty_string(self) -> None:
        """Test that empty string returns empty slug."""
        assert generate_slug("") == ""

    def test_only_special_chars(self) -> None:
        """Test that a string of only special chars returns empty slug."""
        assert generate_slug("@#$%^&*()") == ""

    def test_mixed_case(self) -> None:
        """Test that mixed case is lowercased."""
        assert generate_slug("MyBoard") == "myboard"

    def test_unicode_characters_stripped(self) -> None:
        """Test that non-ASCII characters are stripped."""
        result = generate_slug("Über Cool")
        assert result == "ber-cool"

    def test_tabs_and_newlines(self) -> None:
        """Test that tabs and newlines are treated as whitespace."""
        assert generate_slug("hello\tworld\nnew") == "hello-world-new"

    def test_single_word(self) -> None:
        """Test a single word title."""
        assert generate_slug("backlog") == "backlog"

    def test_already_a_slug(self) -> None:
        """Test that an already-valid slug is unchanged."""
        assert generate_slug("my-board") == "my-board"


class TestGenerateUniqueSlug:
    """Test suite for the generate_unique_slug function."""

    def test_no_collision(self) -> None:
        """Test that the base slug is returned when there's no collision."""
        result = generate_unique_slug("My Board", lambda s: False)
        assert result == "my-board"

    def test_single_collision(self) -> None:
        """Test that -2 suffix is appended on first collision."""
        existing = {"my-board"}
        result = generate_unique_slug("My Board", lambda s: s in existing)
        assert result == "my-board-2"

    def test_multiple_collisions(self) -> None:
        """Test incrementing suffix on multiple collisions."""
        existing = {"my-board", "my-board-2", "my-board-3"}
        result = generate_unique_slug("My Board", lambda s: s in existing)
        assert result == "my-board-4"

    def test_empty_title_raises(self) -> None:
        """Test that an empty title raises ValueError."""
        with pytest.raises(ValueError, match="Cannot generate slug"):
            generate_unique_slug("", lambda s: False)

    def test_special_chars_only_raises(self) -> None:
        """Test that a title with only special chars raises ValueError."""
        with pytest.raises(ValueError, match="Cannot generate slug"):
            generate_unique_slug("@#$%", lambda s: False)

    def test_collision_with_numbers_in_title(self) -> None:
        """Test collision handling when title already has numbers."""
        existing = {"board-2024"}
        result = generate_unique_slug("Board 2024", lambda s: s in existing)
        assert result == "board-2024-2"
