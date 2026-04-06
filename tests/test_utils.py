"""Tests for utility helpers in backend/utils/."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest
from sqlalchemy.orm import Session

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from models import Board, Category  # noqa: E402
from utils.slug import generate_slug, generate_unique_slug  # noqa: E402


# ---------------------------------------------------------------------------
# generate_slug (pure function) tests
# ---------------------------------------------------------------------------


class TestGenerateSlug:
    """Tests for the pure slug generation function."""

    def test_basic(self) -> None:
        """Simple text is slugified."""
        assert generate_slug("Hello World") == "hello-world"

    def test_unicode(self) -> None:
        """Unicode characters are transliterated."""
        result = generate_slug("Héllo Wörld")
        assert result == "hello-world"

    def test_special_characters(self) -> None:
        """Special characters are stripped."""
        result = generate_slug("My Board! @#$%")
        assert result == "my-board"

    def test_max_length(self) -> None:
        """Slug is truncated to max_length."""
        result = generate_slug("a" * 300, max_length=50)
        assert len(result) <= 50

    def test_empty_input_raises(self) -> None:
        """Empty input raises ValueError."""
        with pytest.raises(ValueError, match="Cannot generate slug"):
            generate_slug("")

    def test_whitespace_only_raises(self) -> None:
        """Whitespace-only input raises ValueError."""
        with pytest.raises(ValueError, match="Cannot generate slug"):
            generate_slug("   ")

    def test_symbols_only_raises(self) -> None:
        """Symbols-only input that produces empty slug raises ValueError."""
        with pytest.raises(ValueError, match="Cannot generate slug"):
            generate_slug("@#$%^&*")

    def test_hyphens_collapsed(self) -> None:
        """Multiple hyphens/spaces are collapsed."""
        result = generate_slug("hello   ---   world")
        assert result == "hello-world"


# ---------------------------------------------------------------------------
# generate_unique_slug (database-aware) tests
# ---------------------------------------------------------------------------


class TestGenerateUniqueSlug:
    """Tests for the database-aware unique slug generator."""

    def test_no_collision(self, db_session: Session) -> None:
        """When no collision exists, the base slug is returned."""
        slug = generate_unique_slug(db_session, Board, "My Board")
        assert slug == "my-board"

    def test_collision_appends_suffix(self, db_session: Session) -> None:
        """When a collision exists, a numeric suffix is appended."""
        board = Board(title="My Board", slug="my-board")
        db_session.add(board)
        db_session.commit()

        slug = generate_unique_slug(db_session, Board, "My Board")
        assert slug == "my-board-1"

    def test_multiple_collisions(self, db_session: Session) -> None:
        """Multiple collisions produce incrementing suffixes."""
        db_session.add(Board(title="Test", slug="test"))
        db_session.add(Board(title="Test", slug="test-1"))
        db_session.add(Board(title="Test", slug="test-2"))
        db_session.commit()

        slug = generate_unique_slug(db_session, Board, "Test")
        assert slug == "test-3"

    def test_current_id_excluded(self, db_session: Session) -> None:
        """Updating a record should not collide with itself."""
        board = Board(title="My Board", slug="my-board")
        db_session.add(board)
        db_session.commit()

        slug = generate_unique_slug(
            db_session, Board, "My Board", current_id=board.id
        )
        assert slug == "my-board"

    def test_different_models_no_cross_collision(self, db_session: Session) -> None:
        """Slugs are scoped per model – no cross-model collision."""
        db_session.add(Board(title="Test", slug="test"))
        db_session.commit()

        slug = generate_unique_slug(db_session, Category, "Test")
        assert slug == "test"

    def test_empty_value_raises(self, db_session: Session) -> None:
        """Empty value raises ValueError."""
        with pytest.raises(ValueError, match="Cannot generate slug"):
            generate_unique_slug(db_session, Board, "")

    def test_max_length_with_suffix(self, db_session: Session) -> None:
        """Slug with suffix respects max_length."""
        long_title = "a" * 20
        base_slug = generate_slug(long_title, max_length=20)
        db_session.add(Board(title=long_title, slug=base_slug))
        db_session.commit()

        slug = generate_unique_slug(
            db_session, Board, long_title, max_length=20
        )
        assert len(slug) <= 20
        assert slug.endswith("-1")
