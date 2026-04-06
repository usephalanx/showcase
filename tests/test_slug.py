"""Tests for the slug generation utility."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest
from sqlalchemy.orm import Session

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

import models  # noqa: E402
from utils.slug import generate_unique_slug  # noqa: E402


class TestGenerateUniqueSlug:
    """Tests for generate_unique_slug."""

    def test_basic_slug_generation(self, db_session: Session) -> None:
        """A simple title should produce a clean slug."""
        slug = generate_unique_slug(db_session, models.Board, "My Test Board")
        assert slug == "my-test-board"

    def test_slug_with_special_characters(self, db_session: Session) -> None:
        """Special characters should be stripped from slugs."""
        slug = generate_unique_slug(db_session, models.Board, "Hello, World! @#$%")
        assert slug == "hello-world"

    def test_slug_collision_appends_suffix(
        self, db_session: Session, sample_board: models.Board,
    ) -> None:
        """When a slug already exists, a numeric suffix is appended."""
        slug = generate_unique_slug(db_session, models.Board, "Test Board")
        assert slug == "test-board-1"

    def test_slug_collision_increments(
        self, db_session: Session, sample_board: models.Board,
    ) -> None:
        """Multiple collisions increment the suffix."""
        # Create test-board-1
        board1 = models.Board(title="T", slug="test-board-1")
        db_session.add(board1)
        db_session.commit()

        slug = generate_unique_slug(db_session, models.Board, "Test Board")
        assert slug == "test-board-2"

    def test_slug_excludes_current_id(
        self, db_session: Session, sample_board: models.Board,
    ) -> None:
        """When updating, the current record's slug shouldn't conflict with itself."""
        slug = generate_unique_slug(
            db_session, models.Board, "Test Board", current_id=sample_board.id,
        )
        assert slug == "test-board"

    def test_empty_value_raises(self, db_session: Session) -> None:
        """An empty or whitespace-only value should raise ValueError."""
        with pytest.raises(ValueError, match="Cannot generate slug"):
            generate_unique_slug(db_session, models.Board, "   ")

    def test_slug_for_card_model(self, db_session: Session, sample_column: models.Column) -> None:
        """Slug generation should work for the Card model too."""
        slug = generate_unique_slug(db_session, models.Card, "Implement Feature X")
        assert slug == "implement-feature-x"

    def test_slug_for_category_model(self, db_session: Session) -> None:
        """Slug generation should work for the Category model."""
        slug = generate_unique_slug(db_session, models.Category, "Bug Reports")
        assert slug == "bug-reports"

    def test_unicode_slug(self, db_session: Session) -> None:
        """Unicode titles should produce transliterated slugs."""
        slug = generate_unique_slug(db_session, models.Board, "Ünïcödé Tëst")
        assert slug  # Should produce a non-empty string
        assert " " not in slug

    def test_max_length_respected(self, db_session: Session) -> None:
        """Slug should not exceed the max_length."""
        long_title = "A" * 500
        slug = generate_unique_slug(db_session, models.Board, long_title, max_length=50)
        assert len(slug) <= 50

    def test_max_length_with_suffix(self, db_session: Session) -> None:
        """Slug with collision suffix should not exceed max_length."""
        title = "A" * 50
        # Create the initial slug
        slug1 = generate_unique_slug(db_session, models.Board, title, max_length=50)
        board = models.Board(title=title, slug=slug1)
        db_session.add(board)
        db_session.commit()

        # Generate second slug, should still respect max_length
        slug2 = generate_unique_slug(db_session, models.Board, title, max_length=50)
        assert len(slug2) <= 50
        assert slug2 != slug1
