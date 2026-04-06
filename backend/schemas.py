"""Pydantic schemas for the Kanban application.

Defines request/response schemas for all domain models:
Board, Column, Card, and Category.
"""

from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


# ---------------------------------------------------------------------------
# Category schemas  (declared first so Card schemas can reference them)
# ---------------------------------------------------------------------------


class CategoryCreate(BaseModel):
    """Schema for creating a new category."""

    name: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Human-readable category name.",
    )
    parent_id: Optional[int] = Field(
        None,
        description="Optional parent category ID for hierarchy.",
    )


class CategoryUpdate(BaseModel):
    """Schema for updating an existing category.

    All fields are optional; only supplied fields are updated.
    """

    name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=255,
        description="Human-readable category name.",
    )
    parent_id: Optional[int] = Field(
        None,
        description="Optional parent category ID for hierarchy.",
    )


class CategoryResponse(BaseModel):
    """Schema for category API responses."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    slug: str
    parent_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime


# ---------------------------------------------------------------------------
# Card schemas
# ---------------------------------------------------------------------------


class CardCreate(BaseModel):
    """Schema for creating a new card within a column."""

    title: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Card title.",
    )
    description: Optional[str] = Field(
        None,
        description="Optional detailed description (supports Markdown).",
    )
    position: int = Field(
        0,
        ge=0,
        description="Ordering position within the column.",
    )
    meta_title: Optional[str] = Field(
        None,
        max_length=255,
        description="Optional SEO meta title override.",
    )
    meta_description: Optional[str] = Field(
        None,
        max_length=500,
        description="Optional SEO meta description override.",
    )


class CardUpdate(BaseModel):
    """Schema for updating an existing card.

    All fields are optional; only supplied fields are updated.
    """

    title: Optional[str] = Field(
        None,
        min_length=1,
        max_length=255,
        description="Card title.",
    )
    description: Optional[str] = Field(
        None,
        description="Optional detailed description.",
    )
    position: Optional[int] = Field(
        None,
        ge=0,
        description="Ordering position within the column.",
    )
    meta_title: Optional[str] = Field(
        None,
        max_length=255,
        description="Optional SEO meta title override.",
    )
    meta_description: Optional[str] = Field(
        None,
        max_length=500,
        description="Optional SEO meta description override.",
    )


class CardMove(BaseModel):
    """Schema for moving a card to a different column and/or position."""

    column_id: int = Field(
        ...,
        description="Target column ID to move the card into.",
    )
    position: int = Field(
        ...,
        ge=0,
        description="Target position within the destination column.",
    )


class CardCategoryAction(BaseModel):
    """Schema for associating a category with a card."""

    category_id: int = Field(
        ...,
        description="ID of the category to associate.",
    )


class CardResponse(BaseModel):
    """Schema for card API responses."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    column_id: int
    title: str
    slug: str
    description: Optional[str] = None
    position: int
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    categories: List[CategoryResponse] = Field(
        default_factory=list,
        description="Categories associated with this card.",
    )


# ---------------------------------------------------------------------------
# Column schemas
# ---------------------------------------------------------------------------


class ColumnCreate(BaseModel):
    """Schema for creating a new column within a board."""

    title: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Column heading.",
    )
    board_id: int = Field(
        ...,
        description="ID of the parent board.",
    )
    position: int = Field(
        0,
        ge=0,
        description="Ordering position within the board.",
    )


class ColumnUpdate(BaseModel):
    """Schema for updating an existing column.

    All fields are optional; only supplied fields are updated.
    """

    title: Optional[str] = Field(
        None,
        min_length=1,
        max_length=255,
        description="Column heading.",
    )
    position: Optional[int] = Field(
        None,
        ge=0,
        description="Ordering position within the board.",
    )


class ColumnResponse(BaseModel):
    """Schema for column API responses."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    board_id: int
    title: str
    position: int
    created_at: datetime
    updated_at: datetime
    cards: List[CardResponse] = Field(
        default_factory=list,
        description="Cards belonging to this column.",
    )


# ---------------------------------------------------------------------------
# Board schemas
# ---------------------------------------------------------------------------


class BoardCreate(BaseModel):
    """Schema for creating a new board."""

    title: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Human-readable board title.",
    )
    description: Optional[str] = Field(
        None,
        description="Optional long description of the board.",
    )
    meta_title: Optional[str] = Field(
        None,
        max_length=255,
        description="Optional SEO meta title override.",
    )
    meta_description: Optional[str] = Field(
        None,
        max_length=500,
        description="Optional SEO meta description override.",
    )


class BoardUpdate(BaseModel):
    """Schema for updating an existing board.

    All fields are optional; only supplied fields are updated.
    """

    title: Optional[str] = Field(
        None,
        min_length=1,
        max_length=255,
        description="Human-readable board title.",
    )
    description: Optional[str] = Field(
        None,
        description="Optional long description of the board.",
    )
    meta_title: Optional[str] = Field(
        None,
        max_length=255,
        description="Optional SEO meta title override.",
    )
    meta_description: Optional[str] = Field(
        None,
        max_length=500,
        description="Optional SEO meta description override.",
    )


class BoardResponse(BaseModel):
    """Schema for board API responses."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    slug: str
    description: Optional[str] = None
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    columns: List[ColumnResponse] = Field(
        default_factory=list,
        description="Columns belonging to this board.",
    )
