"""Tests for slug generation utilities."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from utils.slug import generate_slug, generate_unique_slug  # noqa: E402


class TestGenerateSlug:
    """Unit tests for the pure slug generation function."""

    def test_basic(self) -> None:
        """Converts a simple title to a slug."""
        assert generate_slug("Hello World") == "hello-world"

    def test_special_characters(self) -> None:
        """Strips special characters."""
        assert generate_slug("Hello! @World#") == "hello-world"

    def test_unicode(self) -> None:
        """Handles unicode characters."""
        result = generate_slug("Café Résumé")
        assert result == "cafe-resume"

    def test_max_length(self) -> None:
        """Truncates to max_length."""
        result = generate_slug("A" * 300, max_length=10)
        assert len(result) <= 10

    def test_empty_raises(self) -> None:
        """Raises ValueError for empty input."""
        with pytest.raises(ValueError):
            generate_slug("")


class TestGenerateUniqueSlug:
    """Integration tests for unique slug generation with DB."""

    def test_unique_no_collision(
        self,
        db_session: "Session",  # type: ignore[name-defined]
    ) -> None:
        """Returns the base slug when no collision exists."""
        from models import Board

        slug = generate_unique_slug(db=db_session, model=Board, value="Unique Board")
        assert slug == "unique-board"

    def test_collision_appends_suffix(
        self,
        db_session: "Session",  # type: ignore[name-defined]
    ) -> None:
        """Appends -1 when the base slug is taken."""
        from models import Board

        board = Board(title="Test", slug="test")
        db_session.add(board)
        db_session.commit()

        slug = generate_unique_slug(db=db_session, model=Board, value="Test")
        assert slug == "test-1"

    def test_collision_excludes_current_id(
        self,
        db_session: "Session",  # type: ignore[name-defined]
    ) -> None:
        """Excludes the current record from collision check."""
        from models import Board

        board = Board(title="Test", slug="test")
        db_session.add(board)
        db_session.commit()

        slug = generate_unique_slug(
            db=db_session,
            model=Board,
            value="Test",
            current_id=board.id,
        )
        assert slug == "test"
