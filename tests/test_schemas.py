"""Tests for Pydantic schemas defined in backend/schemas.py."""

from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

import pytest
from pydantic import ValidationError

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from schemas import (  # noqa: E402
    BoardCreate,
    BoardResponse,
    BoardUpdate,
    CardCreate,
    CardResponse,
    CardUpdate,
    CategoryCreate,
    CategoryResponse,
    CategoryUpdate,
    ColumnCreate,
    ColumnResponse,
    ColumnUpdate,
)


# ---------------------------------------------------------------------------
# Board schema tests
# ---------------------------------------------------------------------------


class TestBoardCreate:
    """Tests for BoardCreate schema."""

    def test_valid_minimal(self) -> None:
        """Only title is required."""
        schema = BoardCreate(title="My Board")
        assert schema.title == "My Board"
        assert schema.description is None
        assert schema.meta_title is None
        assert schema.meta_description is None

    def test_valid_full(self) -> None:
        """All fields populated."""
        schema = BoardCreate(
            title="My Board",
            description="A nice board",
            meta_title="SEO Title",
            meta_description="SEO Description",
        )
        assert schema.title == "My Board"
        assert schema.description == "A nice board"

    def test_empty_title_rejected(self) -> None:
        """Title with empty string should be rejected."""
        with pytest.raises(ValidationError):
            BoardCreate(title="")

    def test_missing_title_rejected(self) -> None:
        """Missing title should be rejected."""
        with pytest.raises(ValidationError):
            BoardCreate()  # type: ignore[call-arg]

    def test_meta_title_max_length(self) -> None:
        """meta_title exceeding 255 chars should be rejected."""
        with pytest.raises(ValidationError):
            BoardCreate(title="OK", meta_title="x" * 256)

    def test_meta_description_max_length(self) -> None:
        """meta_description exceeding 500 chars should be rejected."""
        with pytest.raises(ValidationError):
            BoardCreate(title="OK", meta_description="x" * 501)


class TestBoardUpdate:
    """Tests for BoardUpdate schema."""

    def test_all_none(self) -> None:
        """All fields are optional – an empty update is valid."""
        schema = BoardUpdate()
        assert schema.title is None
        assert schema.description is None

    def test_partial_update(self) -> None:
        """Only updating one field is valid."""
        schema = BoardUpdate(title="New Title")
        assert schema.title == "New Title"
        assert schema.description is None

    def test_empty_title_rejected(self) -> None:
        """An explicitly empty title should be rejected."""
        with pytest.raises(ValidationError):
            BoardUpdate(title="")


class TestBoardResponse:
    """Tests for BoardResponse schema."""

    def test_from_dict(self) -> None:
        """Construct from a plain dict."""
        now = datetime.now(timezone.utc)
        data = {
            "id": 1,
            "title": "Board",
            "slug": "board",
            "description": None,
            "meta_title": None,
            "meta_description": None,
            "created_at": now,
            "updated_at": now,
            "columns": [],
        }
        schema = BoardResponse(**data)
        assert schema.id == 1
        assert schema.slug == "board"
        assert schema.columns == []

    def test_columns_default_empty(self) -> None:
        """Columns should default to an empty list."""
        now = datetime.now(timezone.utc)
        schema = BoardResponse(
            id=1,
            title="B",
            slug="b",
            created_at=now,
            updated_at=now,
        )
        assert schema.columns == []


# ---------------------------------------------------------------------------
# Column schema tests
# ---------------------------------------------------------------------------


class TestColumnCreate:
    """Tests for ColumnCreate schema."""

    def test_valid(self) -> None:
        """Valid column creation."""
        schema = ColumnCreate(title="To Do", board_id=1)
        assert schema.title == "To Do"
        assert schema.board_id == 1
        assert schema.position == 0

    def test_custom_position(self) -> None:
        """Position can be explicitly set."""
        schema = ColumnCreate(title="Done", board_id=1, position=3)
        assert schema.position == 3

    def test_missing_board_id_rejected(self) -> None:
        """board_id is required."""
        with pytest.raises(ValidationError):
            ColumnCreate(title="Col")  # type: ignore[call-arg]

    def test_negative_position_rejected(self) -> None:
        """Negative position should be rejected."""
        with pytest.raises(ValidationError):
            ColumnCreate(title="Col", board_id=1, position=-1)


class TestColumnUpdate:
    """Tests for ColumnUpdate schema."""

    def test_all_none(self) -> None:
        """All fields optional."""
        schema = ColumnUpdate()
        assert schema.title is None
        assert schema.position is None

    def test_partial(self) -> None:
        """Partial update."""
        schema = ColumnUpdate(position=5)
        assert schema.position == 5
        assert schema.title is None


class TestColumnResponse:
    """Tests for ColumnResponse schema."""

    def test_from_dict(self) -> None:
        """Construct from a plain dict."""
        now = datetime.now(timezone.utc)
        schema = ColumnResponse(
            id=1,
            board_id=1,
            title="To Do",
            position=0,
            created_at=now,
            updated_at=now,
        )
        assert schema.id == 1
        assert schema.cards == []


# ---------------------------------------------------------------------------
# Card schema tests
# ---------------------------------------------------------------------------


class TestCardCreate:
    """Tests for CardCreate schema."""

    def test_valid_minimal(self) -> None:
        """Only title and column_id are required."""
        schema = CardCreate(title="Fix bug", column_id=1)
        assert schema.title == "Fix bug"
        assert schema.column_id == 1
        assert schema.description is None
        assert schema.position == 0
        assert schema.category_ids == []

    def test_with_categories(self) -> None:
        """Card can be created with category associations."""
        schema = CardCreate(title="Task", column_id=1, category_ids=[1, 2, 3])
        assert schema.category_ids == [1, 2, 3]

    def test_missing_column_id_rejected(self) -> None:
        """column_id is required."""
        with pytest.raises(ValidationError):
            CardCreate(title="Task")  # type: ignore[call-arg]

    def test_empty_title_rejected(self) -> None:
        """Empty title should be rejected."""
        with pytest.raises(ValidationError):
            CardCreate(title="", column_id=1)


class TestCardUpdate:
    """Tests for CardUpdate schema."""

    def test_all_none(self) -> None:
        """All fields optional."""
        schema = CardUpdate()
        assert schema.title is None
        assert schema.description is None
        assert schema.column_id is None
        assert schema.position is None
        assert schema.category_ids is None

    def test_move_card(self) -> None:
        """Update column_id and position for card move."""
        schema = CardUpdate(column_id=2, position=3)
        assert schema.column_id == 2
        assert schema.position == 3


class TestCardResponse:
    """Tests for CardResponse schema."""

    def test_from_dict(self) -> None:
        """Construct from a plain dict."""
        now = datetime.now(timezone.utc)
        schema = CardResponse(
            id=1,
            column_id=1,
            title="Task",
            slug="task",
            position=0,
            created_at=now,
            updated_at=now,
        )
        assert schema.id == 1
        assert schema.categories == []


# ---------------------------------------------------------------------------
# Category schema tests
# ---------------------------------------------------------------------------


class TestCategoryCreate:
    """Tests for CategoryCreate schema."""

    def test_valid_minimal(self) -> None:
        """Only name is required."""
        schema = CategoryCreate(name="Urgent")
        assert schema.name == "Urgent"
        assert schema.parent_id is None
        assert schema.description is None

    def test_with_parent(self) -> None:
        """Category with parent_id."""
        schema = CategoryCreate(name="Sub", parent_id=1)
        assert schema.parent_id == 1

    def test_empty_name_rejected(self) -> None:
        """Empty name should be rejected."""
        with pytest.raises(ValidationError):
            CategoryCreate(name="")

    def test_missing_name_rejected(self) -> None:
        """Missing name should be rejected."""
        with pytest.raises(ValidationError):
            CategoryCreate()  # type: ignore[call-arg]


class TestCategoryUpdate:
    """Tests for CategoryUpdate schema."""

    def test_all_none(self) -> None:
        """All fields optional."""
        schema = CategoryUpdate()
        assert schema.name is None
        assert schema.parent_id is None

    def test_partial(self) -> None:
        """Partial update."""
        schema = CategoryUpdate(name="New Name")
        assert schema.name == "New Name"


class TestCategoryResponse:
    """Tests for CategoryResponse schema."""

    def test_from_dict(self) -> None:
        """Construct from a plain dict."""
        now = datetime.now(timezone.utc)
        schema = CategoryResponse(
            id=1,
            name="Urgent",
            slug="urgent",
            created_at=now,
            updated_at=now,
        )
        assert schema.id == 1
        assert schema.parent_id is None
