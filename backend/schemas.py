"""Pydantic schemas for the Kanban application.

Defines request/response schemas for all domain models:
Board, Column, Card, Category, and SEO meta.
"""

from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


# ---------------------------------------------------------------------------
# Category schemas
# ---------------------------------------------------------------------------


class CategoryCreate(BaseModel):
    """Schema for creating a new category."""

    name: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Human-readable category name.",
    )
    description: Optional[str] = Field(
        None,
        description="Optional description of the category.",
    )
    parent_id: Optional[int] = Field(
        None,
        description="ID of the parent category (null for root).",
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
    description: Optional[str] = Field(
        None,
        description="Optional description of the category.",
    )
    parent_id: Optional[int] = Field(
        None,
        description="ID of the parent category (null for root).",
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


class CategoryResponse(BaseModel):
    """Schema for category API responses (flat, without children)."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    slug: str
    description: Optional[str] = None
    parent_id: Optional[int] = None
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class CategoryTreeResponse(BaseModel):
    """Schema for category API responses with nested children tree."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    slug: str
    description: Optional[str] = None
    parent_id: Optional[int] = None
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    children: List[CategoryTreeResponse] = Field(
        default_factory=list,
        description="Child categories forming a tree.",
    )


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
    column_id: int = Field(
        ...,
        description="ID of the parent column.",
    )
    description: Optional[str] = Field(
        None,
        description="Optional detailed description.",
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
    category_ids: Optional[List[int]] = Field(
        None,
        description="List of category IDs to associate.",
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
    column_id: Optional[int] = Field(
        None,
        description="ID of the parent column (for moving cards).",
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
    category_ids: Optional[List[int]] = Field(
        None,
        description="List of category IDs to associate.",
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


# ---------------------------------------------------------------------------
# SEO Meta schemas
# ---------------------------------------------------------------------------


class SEOMetaResponse(BaseModel):
    """Schema for computed SEO meta tags."""

    title: str = Field(
        ...,
        description="Computed page title (meta title).",
    )
    description: str = Field(
        ...,
        description="Computed meta description.",
    )
    og_title: str = Field(
        ...,
        description="Open Graph og:title tag.",
    )
    og_description: str = Field(
        ...,
        description="Open Graph og:description tag.",
    )
    canonical_url: str = Field(
        ...,
        description="Canonical URL for the page.",
    )
    og_type: str = Field(
        "website",
        description="Open Graph og:type tag.",
    )
    page_type: str = Field(
        ...,
        description="The resource type (board, card, category).",
    )
