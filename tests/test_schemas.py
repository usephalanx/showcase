"""Comprehensive tests for Pydantic schemas defined in schemas.py.

Covers validation rules, serialisation from ORM objects, edge cases,
and all schema types: Board, Column, Card, Tag, and pagination.
"""

from __future__ import annotations

import math
from datetime import datetime, timezone
from typing import Any, Dict, List

import pytest
from pydantic import ValidationError

from schemas import (
    BoardCreate,
    BoardListResponse,
    BoardResponse,
    CardCreate,
    CardMoveRequest,
    CardResponse,
    CardUpdate,
    ColumnCreate,
    ColumnResponse,
    PaginationMeta,
    TagCreate,
    TagResponse,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_NOW: datetime = datetime.now(timezone.utc)


def _make_tag_dict(tag_id: int = 1, name: str = "bug") -> Dict[str, Any]:
    """Return a minimal tag dict suitable for TagResponse."""
    return {"id": tag_id, "name": name}


def _make_card_dict(**overrides: Any) -> Dict[str, Any]:
    """Return a minimal card dict suitable for CardResponse."""
    base: Dict[str, Any] = {
        "id": 1,
        "title": "Fix login bug",
        "description": "Users cannot log in with SSO",
        "slug": "fix-login-bug",
        "position": 0,
        "column_id": 1,
        "meta_title": None,
        "meta_description": None,
        "created_at": _NOW,
        "updated_at": _NOW,
        "tags": [],
    }
    base.update(overrides)
    return base


def _make_column_dict(**overrides: Any) -> Dict[str, Any]:
    """Return a minimal column dict suitable for ColumnResponse."""
    base: Dict[str, Any] = {
        "id": 1,
        "title": "To Do",
        "position": 0,
        "board_id": 1,
        "cards": [],
    }
    base.update(overrides)
    return base


def _make_board_dict(**overrides: Any) -> Dict[str, Any]:
    """Return a minimal board dict suitable for BoardResponse."""
    base: Dict[str, Any] = {
        "id": 1,
        "title": "Sprint 1",
        "slug": "sprint-1",
        "description": None,
        "meta_title": None,
        "meta_description": None,
        "created_at": _NOW,
        "updated_at": _NOW,
        "columns": [],
    }
    base.update(overrides)
    return base


# ===================================================================
# TagCreate
# ===================================================================


class TestTagCreate:
    """Tests for TagCreate schema."""

    def test_valid_tag(self) -> None:
        """A simple valid name should pass."""
        tag = TagCreate(name="bug")
        assert tag.name == "bug"

    def test_strips_whitespace(self) -> None:
        """Leading/trailing whitespace should be stripped."""
        tag = TagCreate(name="  feature  ")
        assert tag.name == "feature"

    def test_empty_string_rejected(self) -> None:
        """An empty string should be rejected."""
        with pytest.raises(ValidationError):
            TagCreate(name="")

    def test_blank_string_rejected(self) -> None:
        """A whitespace-only string should be rejected."""
        with pytest.raises(ValidationError):
            TagCreate(name="   ")

    def test_max_length(self) -> None:
        """Name at exactly 100 chars should pass."""
        tag = TagCreate(name="a" * 100)
        assert len(tag.name) == 100

    def test_exceeds_max_length(self) -> None:
        """Name exceeding 100 chars should be rejected."""
        with pytest.raises(ValidationError):
            TagCreate(name="a" * 101)


# ===================================================================
# TagResponse
# ===================================================================


class TestTagResponse:
    """Tests for TagResponse schema."""

    def test_valid_response(self) -> None:
        """A valid dict should produce a TagResponse."""
        resp = TagResponse(**_make_tag_dict())
        assert resp.id == 1
        assert resp.name == "bug"

    def test_from_attributes_enabled(self) -> None:
        """The model_config should allow from_attributes."""
        assert TagResponse.model_config.get("from_attributes") is True


# ===================================================================
# CardCreate
# ===================================================================


class TestCardCreate:
    """Tests for CardCreate schema."""

    def test_valid_minimal(self) -> None:
        """Minimal valid create with just title and column_id."""
        card = CardCreate(title="Task A", column_id=1)
        assert card.title == "Task A"
        assert card.column_id == 1
        assert card.position == 0
        assert card.description is None
        assert card.meta_title is None
        assert card.meta_description is None
        assert card.slug is None
        assert card.tag_ids is None

    def test_valid_full(self) -> None:
        """Full create with all fields populated."""
        card = CardCreate(
            title="Task B",
            description="A lengthy description",
            column_id=2,
            position=3,
            meta_title="SEO Title",
            meta_description="SEO Description",
            slug="task-b",
            tag_ids=[1, 2, 3],
        )
        assert card.slug == "task-b"
        assert card.tag_ids == [1, 2, 3]

    def test_title_blank_rejected(self) -> None:
        """Whitespace-only title should be rejected."""
        with pytest.raises(ValidationError):
            CardCreate(title="   ", column_id=1)

    def test_title_empty_rejected(self) -> None:
        """Empty title should be rejected."""
        with pytest.raises(ValidationError):
            CardCreate(title="", column_id=1)

    def test_column_id_must_be_positive(self) -> None:
        """column_id must be > 0."""
        with pytest.raises(ValidationError):
            CardCreate(title="Task", column_id=0)

    def test_position_cannot_be_negative(self) -> None:
        """position must be >= 0."""
        with pytest.raises(ValidationError):
            CardCreate(title="Task", column_id=1, position=-1)

    def test_meta_title_max_length(self) -> None:
        """meta_title exceeding 70 chars should be rejected."""
        with pytest.raises(ValidationError):
            CardCreate(title="Task", column_id=1, meta_title="a" * 71)

    def test_meta_description_max_length(self) -> None:
        """meta_description exceeding 160 chars should be rejected."""
        with pytest.raises(ValidationError):
            CardCreate(title="Task", column_id=1, meta_description="a" * 161)

    def test_slug_invalid_chars_rejected(self) -> None:
        """Slug with uppercase or special chars should be rejected."""
        with pytest.raises(ValidationError):
            CardCreate(title="Task", column_id=1, slug="Invalid Slug!")

    def test_slug_valid_format(self) -> None:
        """A valid slug should pass."""
        card = CardCreate(title="Task", column_id=1, slug="my-valid-slug-123")
        assert card.slug == "my-valid-slug-123"

    def test_slug_empty_string_becomes_none(self) -> None:
        """An empty slug string should become None."""
        card = CardCreate(title="Task", column_id=1, slug="")
        assert card.slug is None

    def test_slug_whitespace_only_becomes_none(self) -> None:
        """A whitespace-only slug should become None."""
        card = CardCreate(title="Task", column_id=1, slug="   ")
        assert card.slug is None

    def test_title_is_stripped(self) -> None:
        """Leading/trailing whitespace on title should be stripped."""
        card = CardCreate(title="  Task C  ", column_id=1)
        assert card.title == "Task C"


# ===================================================================
# CardUpdate
# ===================================================================


class TestCardUpdate:
    """Tests for CardUpdate schema."""

    def test_all_fields_optional(self) -> None:
        """An empty update body should be valid."""
        update = CardUpdate()
        assert update.title is None
        assert update.description is None
        assert update.position is None
        assert update.meta_title is None
        assert update.meta_description is None
        assert update.slug is None
        assert update.tag_ids is None

    def test_partial_update_title(self) -> None:
        """Updating only the title should work."""
        update = CardUpdate(title="New Title")
        assert update.title == "New Title"

    def test_partial_update_tags(self) -> None:
        """Updating only tag_ids should work."""
        update = CardUpdate(tag_ids=[5, 6])
        assert update.tag_ids == [5, 6]

    def test_title_blank_rejected(self) -> None:
        """Whitespace-only title in update should be rejected."""
        with pytest.raises(ValidationError):
            CardUpdate(title="   ")

    def test_slug_invalid_rejected(self) -> None:
        """Invalid slug in update should be rejected."""
        with pytest.raises(ValidationError):
            CardUpdate(slug="BAD SLUG")

    def test_meta_title_too_long(self) -> None:
        """meta_title exceeding 70 chars should be rejected."""
        with pytest.raises(ValidationError):
            CardUpdate(meta_title="x" * 71)

    def test_meta_description_too_long(self) -> None:
        """meta_description exceeding 160 chars should be rejected."""
        with pytest.raises(ValidationError):
            CardUpdate(meta_description="x" * 161)

    def test_position_negative_rejected(self) -> None:
        """Negative position should be rejected."""
        with pytest.raises(ValidationError):
            CardUpdate(position=-1)


# ===================================================================
# CardMoveRequest
# ===================================================================


class TestCardMoveRequest:
    """Tests for CardMoveRequest schema."""

    def test_valid_move(self) -> None:
        """A valid move request."""
        move = CardMoveRequest(column_id=3, position=2)
        assert move.column_id == 3
        assert move.position == 2

    def test_column_id_must_be_positive(self) -> None:
        """column_id must be > 0."""
        with pytest.raises(ValidationError):
            CardMoveRequest(column_id=0, position=0)

    def test_position_must_be_non_negative(self) -> None:
        """position must be >= 0."""
        with pytest.raises(ValidationError):
            CardMoveRequest(column_id=1, position=-1)

    def test_missing_column_id_rejected(self) -> None:
        """column_id is required."""
        with pytest.raises(ValidationError):
            CardMoveRequest(position=0)  # type: ignore[call-arg]

    def test_missing_position_rejected(self) -> None:
        """position is required."""
        with pytest.raises(ValidationError):
            CardMoveRequest(column_id=1)  # type: ignore[call-arg]


# ===================================================================
# CardResponse
# ===================================================================


class TestCardResponse:
    """Tests for CardResponse schema."""

    def test_valid_response(self) -> None:
        """A valid card dict should produce a CardResponse."""
        resp = CardResponse(**_make_card_dict())
        assert resp.id == 1
        assert resp.title == "Fix login bug"
        assert resp.slug == "fix-login-bug"
        assert resp.tags == []

    def test_with_tags(self) -> None:
        """CardResponse should include nested tags."""
        data = _make_card_dict(tags=[_make_tag_dict(1, "bug"), _make_tag_dict(2, "urgent")])
        resp = CardResponse(**data)
        assert len(resp.tags) == 2
        assert resp.tags[0].name == "bug"
        assert resp.tags[1].name == "urgent"

    def test_seo_fields(self) -> None:
        """SEO fields should be present."""
        data = _make_card_dict(
            meta_title="Custom SEO Title",
            meta_description="Custom SEO description for the card.",
        )
        resp = CardResponse(**data)
        assert resp.meta_title == "Custom SEO Title"
        assert resp.meta_description == "Custom SEO description for the card."

    def test_from_attributes_enabled(self) -> None:
        """The model_config should allow from_attributes."""
        assert CardResponse.model_config.get("from_attributes") is True


# ===================================================================
# ColumnCreate
# ===================================================================


class TestColumnCreate:
    """Tests for ColumnCreate schema."""

    def test_valid_minimal(self) -> None:
        """Minimal valid column create."""
        col = ColumnCreate(title="To Do", board_id=1)
        assert col.title == "To Do"
        assert col.board_id == 1
        assert col.position == 0

    def test_title_blank_rejected(self) -> None:
        """Whitespace-only title should be rejected."""
        with pytest.raises(ValidationError):
            ColumnCreate(title="   ", board_id=1)

    def test_title_empty_rejected(self) -> None:
        """Empty title should be rejected."""
        with pytest.raises(ValidationError):
            ColumnCreate(title="", board_id=1)

    def test_board_id_must_be_positive(self) -> None:
        """board_id must be > 0."""
        with pytest.raises(ValidationError):
            ColumnCreate(title="To Do", board_id=0)

    def test_position_default_zero(self) -> None:
        """position should default to 0."""
        col = ColumnCreate(title="In Progress", board_id=1)
        assert col.position == 0

    def test_position_negative_rejected(self) -> None:
        """Negative position should be rejected."""
        with pytest.raises(ValidationError):
            ColumnCreate(title="Done", board_id=1, position=-1)

    def test_title_stripped(self) -> None:
        """Leading/trailing whitespace on title should be stripped."""
        col = ColumnCreate(title="  In Progress  ", board_id=1)
        assert col.title == "In Progress"

    def test_title_max_length(self) -> None:
        """Title at exactly 255 chars should pass."""
        col = ColumnCreate(title="a" * 255, board_id=1)
        assert len(col.title) == 255

    def test_title_exceeds_max_length(self) -> None:
        """Title exceeding 255 chars should be rejected."""
        with pytest.raises(ValidationError):
            ColumnCreate(title="a" * 256, board_id=1)


# ===================================================================
# ColumnResponse
# ===================================================================


class TestColumnResponse:
    """Tests for ColumnResponse schema."""

    def test_valid_response(self) -> None:
        """A valid column dict should produce a ColumnResponse."""
        resp = ColumnResponse(**_make_column_dict())
        assert resp.id == 1
        assert resp.title == "To Do"
        assert resp.cards == []

    def test_with_cards(self) -> None:
        """ColumnResponse should include nested cards."""
        data = _make_column_dict(cards=[_make_card_dict()])
        resp = ColumnResponse(**data)
        assert len(resp.cards) == 1
        assert resp.cards[0].title == "Fix login bug"

    def test_from_attributes_enabled(self) -> None:
        """The model_config should allow from_attributes."""
        assert ColumnResponse.model_config.get("from_attributes") is True


# ===================================================================
# BoardCreate
# ===================================================================


class TestBoardCreate:
    """Tests for BoardCreate schema."""

    def test_valid_minimal(self) -> None:
        """Minimal valid board create with just title."""
        board = BoardCreate(title="Sprint 1")
        assert board.title == "Sprint 1"
        assert board.description is None
        assert board.meta_title is None
        assert board.meta_description is None
        assert board.slug is None

    def test_valid_full(self) -> None:
        """Full board create with all fields."""
        board = BoardCreate(
            title="Sprint 1",
            description="First sprint of the project",
            meta_title="Sprint 1 Board",
            meta_description="Track all tasks for Sprint 1.",
            slug="sprint-1",
        )
        assert board.slug == "sprint-1"
        assert board.meta_title == "Sprint 1 Board"

    def test_title_blank_rejected(self) -> None:
        """Whitespace-only title should be rejected."""
        with pytest.raises(ValidationError):
            BoardCreate(title="   ")

    def test_title_empty_rejected(self) -> None:
        """Empty title should be rejected."""
        with pytest.raises(ValidationError):
            BoardCreate(title="")

    def test_meta_title_max_length(self) -> None:
        """meta_title exceeding 70 chars should be rejected."""
        with pytest.raises(ValidationError):
            BoardCreate(title="Board", meta_title="a" * 71)

    def test_meta_title_at_max_length(self) -> None:
        """meta_title at exactly 70 chars should pass."""
        board = BoardCreate(title="Board", meta_title="a" * 70)
        assert len(board.meta_title) == 70  # type: ignore[arg-type]

    def test_meta_description_max_length(self) -> None:
        """meta_description exceeding 160 chars should be rejected."""
        with pytest.raises(ValidationError):
            BoardCreate(title="Board", meta_description="a" * 161)

    def test_meta_description_at_max_length(self) -> None:
        """meta_description at exactly 160 chars should pass."""
        board = BoardCreate(title="Board", meta_description="a" * 160)
        assert len(board.meta_description) == 160  # type: ignore[arg-type]

    def test_slug_invalid_rejected(self) -> None:
        """Slug with invalid characters should be rejected."""
        with pytest.raises(ValidationError):
            BoardCreate(title="Board", slug="Invalid Slug!")

    def test_slug_uppercase_rejected(self) -> None:
        """Slug with uppercase letters should be rejected."""
        with pytest.raises(ValidationError):
            BoardCreate(title="Board", slug="MySlug")

    def test_slug_valid(self) -> None:
        """A valid slug should pass."""
        board = BoardCreate(title="Board", slug="my-board-123")
        assert board.slug == "my-board-123"

    def test_slug_empty_becomes_none(self) -> None:
        """An empty slug should become None."""
        board = BoardCreate(title="Board", slug="")
        assert board.slug is None

    def test_slug_whitespace_becomes_none(self) -> None:
        """A whitespace-only slug should become None."""
        board = BoardCreate(title="Board", slug="   ")
        assert board.slug is None

    def test_title_stripped(self) -> None:
        """Title should have whitespace stripped."""
        board = BoardCreate(title="  Sprint 1  ")
        assert board.title == "Sprint 1"

    def test_title_max_length(self) -> None:
        """Title at exactly 255 chars should pass."""
        board = BoardCreate(title="b" * 255)
        assert len(board.title) == 255

    def test_title_exceeds_max_length(self) -> None:
        """Title exceeding 255 chars should be rejected."""
        with pytest.raises(ValidationError):
            BoardCreate(title="b" * 256)


# ===================================================================
# BoardResponse
# ===================================================================


class TestBoardResponse:
    """Tests for BoardResponse schema."""

    def test_valid_response(self) -> None:
        """A valid board dict should produce a BoardResponse."""
        resp = BoardResponse(**_make_board_dict())
        assert resp.id == 1
        assert resp.title == "Sprint 1"
        assert resp.slug == "sprint-1"
        assert resp.columns == []

    def test_with_columns(self) -> None:
        """BoardResponse should include nested columns."""
        data = _make_board_dict(columns=[_make_column_dict()])
        resp = BoardResponse(**data)
        assert len(resp.columns) == 1
        assert resp.columns[0].title == "To Do"

    def test_with_full_hierarchy(self) -> None:
        """BoardResponse should include columns with cards with tags."""
        tag = _make_tag_dict(1, "urgent")
        card = _make_card_dict(tags=[tag])
        column = _make_column_dict(cards=[card])
        board = _make_board_dict(columns=[column])
        resp = BoardResponse(**board)
        assert resp.columns[0].cards[0].tags[0].name == "urgent"

    def test_seo_fields(self) -> None:
        """SEO fields should be present on BoardResponse."""
        data = _make_board_dict(
            meta_title="Board SEO Title",
            meta_description="Board SEO description.",
        )
        resp = BoardResponse(**data)
        assert resp.meta_title == "Board SEO Title"
        assert resp.meta_description == "Board SEO description."

    def test_from_attributes_enabled(self) -> None:
        """The model_config should allow from_attributes."""
        assert BoardResponse.model_config.get("from_attributes") is True


# ===================================================================
# PaginationMeta
# ===================================================================


class TestPaginationMeta:
    """Tests for PaginationMeta schema."""

    def test_valid(self) -> None:
        """A valid pagination meta."""
        meta = PaginationMeta(total=50, page=1, per_page=10, total_pages=5)
        assert meta.total == 50
        assert meta.page == 1
        assert meta.per_page == 10
        assert meta.total_pages == 5

    def test_total_cannot_be_negative(self) -> None:
        """total must be >= 0."""
        with pytest.raises(ValidationError):
            PaginationMeta(total=-1, page=1, per_page=10, total_pages=0)

    def test_page_must_be_positive(self) -> None:
        """page must be >= 1."""
        with pytest.raises(ValidationError):
            PaginationMeta(total=0, page=0, per_page=10, total_pages=0)

    def test_per_page_must_be_positive(self) -> None:
        """per_page must be >= 1."""
        with pytest.raises(ValidationError):
            PaginationMeta(total=0, page=1, per_page=0, total_pages=0)

    def test_empty_results(self) -> None:
        """Zero total items is valid."""
        meta = PaginationMeta(total=0, page=1, per_page=10, total_pages=0)
        assert meta.total == 0
        assert meta.total_pages == 0


# ===================================================================
# BoardListResponse
# ===================================================================


class TestBoardListResponse:
    """Tests for BoardListResponse schema."""

    def test_valid_with_data(self) -> None:
        """BoardListResponse with data and meta should be valid."""
        boards = [_make_board_dict(), _make_board_dict(id=2, slug="sprint-2", title="Sprint 2")]
        meta = {"total": 2, "page": 1, "per_page": 10, "total_pages": 1}
        resp = BoardListResponse(data=boards, meta=meta)
        assert len(resp.data) == 2
        assert resp.meta.total == 2
        assert resp.data[0].title == "Sprint 1"
        assert resp.data[1].title == "Sprint 2"

    def test_empty_list(self) -> None:
        """BoardListResponse with no data should be valid."""
        meta = {"total": 0, "page": 1, "per_page": 10, "total_pages": 0}
        resp = BoardListResponse(data=[], meta=meta)
        assert len(resp.data) == 0
        assert resp.meta.total == 0

    def test_nested_hierarchy(self) -> None:
        """BoardListResponse should support fully nested board data."""
        tag = _make_tag_dict()
        card = _make_card_dict(tags=[tag])
        column = _make_column_dict(cards=[card])
        board = _make_board_dict(columns=[column])
        meta = {"total": 1, "page": 1, "per_page": 10, "total_pages": 1}
        resp = BoardListResponse(data=[board], meta=meta)
        assert resp.data[0].columns[0].cards[0].tags[0].name == "bug"


# ===================================================================
# Slug validation edge cases (cross-schema)
# ===================================================================


class TestSlugValidation:
    """Test slug validation across all schemas that accept slugs."""

    @pytest.mark.parametrize(
        "slug",
        [
            "valid-slug",
            "a",
            "slug-with-123-numbers",
            "123",
            "a-b-c-d-e",
        ],
    )
    def test_valid_slugs_board(self, slug: str) -> None:
        """Various valid slugs should be accepted by BoardCreate."""
        board = BoardCreate(title="Board", slug=slug)
        assert board.slug == slug

    @pytest.mark.parametrize(
        "slug",
        [
            "UPPERCASE",
            "has spaces",
            "has_underscore",
            "trailing-",
            "-leading",
            "double--hyphen",
            "special!@#",
        ],
    )
    def test_invalid_slugs_board(self, slug: str) -> None:
        """Various invalid slugs should be rejected by BoardCreate."""
        with pytest.raises(ValidationError):
            BoardCreate(title="Board", slug=slug)

    @pytest.mark.parametrize(
        "slug",
        [
            "valid-slug",
            "a",
            "my-card-42",
        ],
    )
    def test_valid_slugs_card_create(self, slug: str) -> None:
        """Valid slugs should be accepted by CardCreate."""
        card = CardCreate(title="Card", column_id=1, slug=slug)
        assert card.slug == slug

    @pytest.mark.parametrize(
        "slug",
        [
            "UPPERCASE",
            "has spaces",
            "-leading",
            "trailing-",
        ],
    )
    def test_invalid_slugs_card_create(self, slug: str) -> None:
        """Invalid slugs should be rejected by CardCreate."""
        with pytest.raises(ValidationError):
            CardCreate(title="Card", column_id=1, slug=slug)

    @pytest.mark.parametrize(
        "slug",
        [
            "valid-slug",
            "my-card-42",
        ],
    )
    def test_valid_slugs_card_update(self, slug: str) -> None:
        """Valid slugs should be accepted by CardUpdate."""
        update = CardUpdate(slug=slug)
        assert update.slug == slug

    @pytest.mark.parametrize(
        "slug",
        [
            "INVALID",
            "has space",
        ],
    )
    def test_invalid_slugs_card_update(self, slug: str) -> None:
        """Invalid slugs should be rejected by CardUpdate."""
        with pytest.raises(ValidationError):
            CardUpdate(slug=slug)


# ===================================================================
# Serialisation round-trip tests
# ===================================================================


class TestSerialisationRoundTrip:
    """Test that schemas serialise to JSON-compatible dicts and back."""

    def test_board_response_round_trip(self) -> None:
        """BoardResponse should survive model_dump -> re-parse cycle."""
        original = BoardResponse(**_make_board_dict())
        data = original.model_dump()
        restored = BoardResponse(**data)
        assert restored.id == original.id
        assert restored.title == original.title
        assert restored.slug == original.slug

    def test_card_response_round_trip(self) -> None:
        """CardResponse should survive model_dump -> re-parse cycle."""
        original = CardResponse(**_make_card_dict(tags=[_make_tag_dict()]))
        data = original.model_dump()
        restored = CardResponse(**data)
        assert restored.tags[0].name == original.tags[0].name

    def test_board_list_response_round_trip(self) -> None:
        """BoardListResponse should survive model_dump -> re-parse cycle."""
        boards = [_make_board_dict()]
        meta = {"total": 1, "page": 1, "per_page": 10, "total_pages": 1}
        original = BoardListResponse(data=boards, meta=meta)
        data = original.model_dump()
        restored = BoardListResponse(**data)
        assert restored.meta.total == 1
        assert len(restored.data) == 1
