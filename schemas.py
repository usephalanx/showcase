"""Pydantic request/response schemas for the Kanban API.

Defines validation schemas for all entities:
- Board: create, update, response, list with pagination
- Column: create, update, response
- Card: create, update, move, response
- Tag: create, response

All schemas use strict validation and include SEO fields
(meta_title, meta_description, slug) where appropriate.
"""

from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator


# ---------------------------------------------------------------------------
# Tag schemas
# ---------------------------------------------------------------------------


class TagCreate(BaseModel):
    """Request body for creating a new tag.

    Attributes:
        name: Display name of the tag. Must be non-empty and <= 100 chars.
    """

    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Display name of the tag",
    )

    @field_validator("name")
    @classmethod
    def name_not_blank(cls, v: str) -> str:
        """Ensure the name is not only whitespace."""
        if not v.strip():
            raise ValueError("Tag name must not be blank")
        return v.strip()


class TagResponse(BaseModel):
    """Response body representing a single tag.

    Attributes:
        id: Primary key of the tag.
        name: Display name of the tag.
    """

    id: int
    name: str

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# Card schemas
# ---------------------------------------------------------------------------


class CardCreate(BaseModel):
    """Request body for creating a new card.

    Attributes:
        title: Display title of the card. Must be non-empty and <= 255 chars.
        description: Optional longer description of the card.
        column_id: Foreign key to the column this card belongs to.
        position: Integer position within the column (0-based). Defaults to 0.
        meta_title: Optional SEO title override (max 70 chars).
        meta_description: Optional SEO meta description (max 160 chars).
        slug: Optional custom slug. Auto-generated from title if omitted.
        tag_ids: Optional list of tag IDs to associate with the card.
    """

    title: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Display title of the card",
    )
    description: Optional[str] = Field(
        None,
        description="Optional longer description of the card",
    )
    column_id: int = Field(
        ...,
        gt=0,
        description="ID of the column this card belongs to",
    )
    position: int = Field(
        0,
        ge=0,
        description="Position within the column (0-based)",
    )
    meta_title: Optional[str] = Field(
        None,
        max_length=70,
        description="SEO title override (max 70 chars)",
    )
    meta_description: Optional[str] = Field(
        None,
        max_length=160,
        description="SEO meta description (max 160 chars)",
    )
    slug: Optional[str] = Field(
        None,
        max_length=255,
        description="Custom URL slug. Auto-generated from title if omitted",
    )
    tag_ids: Optional[List[int]] = Field(
        None,
        description="List of tag IDs to associate with this card",
    )

    @field_validator("title")
    @classmethod
    def title_not_blank(cls, v: str) -> str:
        """Ensure the title is not only whitespace."""
        if not v.strip():
            raise ValueError("Card title must not be blank")
        return v.strip()

    @field_validator("slug")
    @classmethod
    def slug_format(cls, v: Optional[str]) -> Optional[str]:
        """Validate that a custom slug contains only URL-safe characters."""
        if v is not None:
            v = v.strip()
            if not v:
                return None
            import re
            if not re.match(r"^[a-z0-9]+(?:-[a-z0-9]+)*$", v):
                raise ValueError(
                    "Slug must contain only lowercase alphanumeric "
                    "characters and hyphens"
                )
        return v


class CardUpdate(BaseModel):
    """Request body for updating an existing card.

    All fields are optional; only provided fields will be updated.

    Attributes:
        title: New display title of the card.
        description: New description of the card.
        position: New position within the column.
        meta_title: New SEO title override.
        meta_description: New SEO meta description.
        slug: New custom slug.
        tag_ids: New list of tag IDs (replaces existing associations).
    """

    title: Optional[str] = Field(
        None,
        min_length=1,
        max_length=255,
        description="New display title of the card",
    )
    description: Optional[str] = Field(
        None,
        description="New description of the card",
    )
    position: Optional[int] = Field(
        None,
        ge=0,
        description="New position within the column",
    )
    meta_title: Optional[str] = Field(
        None,
        max_length=70,
        description="New SEO title override (max 70 chars)",
    )
    meta_description: Optional[str] = Field(
        None,
        max_length=160,
        description="New SEO meta description (max 160 chars)",
    )
    slug: Optional[str] = Field(
        None,
        max_length=255,
        description="New custom URL slug",
    )
    tag_ids: Optional[List[int]] = Field(
        None,
        description="New list of tag IDs (replaces existing associations)",
    )

    @field_validator("title")
    @classmethod
    def title_not_blank(cls, v: Optional[str]) -> Optional[str]:
        """Ensure the title is not only whitespace when provided."""
        if v is not None:
            if not v.strip():
                raise ValueError("Card title must not be blank")
            return v.strip()
        return v

    @field_validator("slug")
    @classmethod
    def slug_format(cls, v: Optional[str]) -> Optional[str]:
        """Validate that a custom slug contains only URL-safe characters."""
        if v is not None:
            v = v.strip()
            if not v:
                return None
            import re
            if not re.match(r"^[a-z0-9]+(?:-[a-z0-9]+)*$", v):
                raise ValueError(
                    "Slug must contain only lowercase alphanumeric "
                    "characters and hyphens"
                )
        return v


class CardMoveRequest(BaseModel):
    """Request body for moving a card to a different column and/or position.

    Attributes:
        column_id: Target column ID to move the card to.
        position: Target position within the destination column (0-based).
    """

    column_id: int = Field(
        ...,
        gt=0,
        description="Target column ID",
    )
    position: int = Field(
        ...,
        ge=0,
        description="Target position within the destination column (0-based)",
    )


class CardResponse(BaseModel):
    """Response body representing a single card.

    Attributes:
        id: Primary key of the card.
        title: Display title of the card.
        description: Optional longer description.
        slug: SEO-friendly URL slug.
        position: Position within the column (0-based).
        column_id: Foreign key to the parent column.
        meta_title: Optional SEO title override.
        meta_description: Optional SEO meta description.
        created_at: Timestamp when the card was created.
        updated_at: Timestamp of the last update.
        tags: List of tags associated with this card.
    """

    id: int
    title: str
    description: Optional[str] = None
    slug: str
    position: int
    column_id: int
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    tags: List[TagResponse] = Field(default_factory=list)

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# Column schemas
# ---------------------------------------------------------------------------


class ColumnCreate(BaseModel):
    """Request body for creating a new column.

    Attributes:
        title: Display title of the column. Must be non-empty and <= 255 chars.
        board_id: Foreign key to the parent board.
        position: Integer position within the board (0-based). Defaults to 0.
    """

    title: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Display title of the column",
    )
    board_id: int = Field(
        ...,
        gt=0,
        description="ID of the parent board",
    )
    position: int = Field(
        0,
        ge=0,
        description="Position within the board (0-based)",
    )

    @field_validator("title")
    @classmethod
    def title_not_blank(cls, v: str) -> str:
        """Ensure the title is not only whitespace."""
        if not v.strip():
            raise ValueError("Column title must not be blank")
        return v.strip()


class ColumnResponse(BaseModel):
    """Response body representing a single column.

    Attributes:
        id: Primary key of the column.
        title: Display title of the column.
        position: Position within the board (0-based).
        board_id: Foreign key to the parent board.
        cards: List of cards within this column, ordered by position.
    """

    id: int
    title: str
    position: int
    board_id: int
    cards: List[CardResponse] = Field(default_factory=list)

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# Board schemas
# ---------------------------------------------------------------------------


class BoardCreate(BaseModel):
    """Request body for creating a new board.

    Attributes:
        title: Display title of the board. Must be non-empty and <= 255 chars.
        description: Optional longer description.
        meta_title: Optional SEO title override (max 70 chars).
        meta_description: Optional SEO meta description (max 160 chars).
        slug: Optional custom slug. Auto-generated from title if omitted.
    """

    title: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Display title of the board",
    )
    description: Optional[str] = Field(
        None,
        description="Optional longer description of the board",
    )
    meta_title: Optional[str] = Field(
        None,
        max_length=70,
        description="SEO title override (max 70 chars)",
    )
    meta_description: Optional[str] = Field(
        None,
        max_length=160,
        description="SEO meta description (max 160 chars)",
    )
    slug: Optional[str] = Field(
        None,
        max_length=255,
        description="Custom URL slug. Auto-generated from title if omitted",
    )

    @field_validator("title")
    @classmethod
    def title_not_blank(cls, v: str) -> str:
        """Ensure the title is not only whitespace."""
        if not v.strip():
            raise ValueError("Board title must not be blank")
        return v.strip()

    @field_validator("slug")
    @classmethod
    def slug_format(cls, v: Optional[str]) -> Optional[str]:
        """Validate that a custom slug contains only URL-safe characters."""
        if v is not None:
            v = v.strip()
            if not v:
                return None
            import re
            if not re.match(r"^[a-z0-9]+(?:-[a-z0-9]+)*$", v):
                raise ValueError(
                    "Slug must contain only lowercase alphanumeric "
                    "characters and hyphens"
                )
        return v


class BoardResponse(BaseModel):
    """Response body representing a single board.

    Attributes:
        id: Primary key of the board.
        title: Display title of the board.
        slug: SEO-friendly URL slug.
        description: Optional longer description.
        meta_title: Optional SEO title override.
        meta_description: Optional SEO meta description.
        created_at: Timestamp when the board was created.
        updated_at: Timestamp of the last update.
        columns: List of columns within this board, ordered by position.
    """

    id: int
    title: str
    slug: str
    description: Optional[str] = None
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    columns: List[ColumnResponse] = Field(default_factory=list)

    model_config = {"from_attributes": True}


class PaginationMeta(BaseModel):
    """Pagination metadata for list endpoints.

    Attributes:
        total: Total number of items matching the query.
        page: Current page number (1-based).
        per_page: Number of items per page.
        total_pages: Total number of pages available.
    """

    total: int = Field(..., ge=0, description="Total number of items")
    page: int = Field(..., ge=1, description="Current page number (1-based)")
    per_page: int = Field(..., ge=1, description="Number of items per page")
    total_pages: int = Field(..., ge=0, description="Total number of pages")


class BoardListResponse(BaseModel):
    """Response body for listing boards with pagination metadata.

    Attributes:
        data: List of board summaries for the current page.
        meta: Pagination metadata.
    """

    data: List[BoardResponse]
    meta: PaginationMeta
