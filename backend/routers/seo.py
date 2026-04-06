"""SEO meta tag computation endpoint.

Provides GET /api/seo/:page_type/:slug that returns computed meta tags
(title, description, og:title, og:description, canonical URL) for any
board, card, or category page.
"""

from __future__ import annotations

import os

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db
from models import Board, Card, Category
from schemas import SEOMetaResponse

router = APIRouter(prefix="/api/seo", tags=["seo"])

# Base URL for canonical links; override via SITE_BASE_URL env var.
SITE_BASE_URL: str = os.environ.get("SITE_BASE_URL", "https://example.com")

# Site name appended to page titles.
SITE_NAME: str = os.environ.get("SITE_NAME", "Kanban Board")

# Default description when none is available.
DEFAULT_DESCRIPTION: str = "Manage your tasks efficiently with our Kanban board."

# Maximum length for meta descriptions.
META_DESCRIPTION_MAX_LENGTH: int = 160


def _truncate(text: str, max_length: int = META_DESCRIPTION_MAX_LENGTH) -> str:
    """Truncate text to a maximum length, appending ellipsis if needed.

    Args:
        text: The text to truncate.
        max_length: Maximum allowed character length.

    Returns:
        The truncated string.
    """
    if len(text) <= max_length:
        return text
    return text[: max_length - 3].rstrip() + "..."


def _compute_board_meta(board: Board) -> SEOMetaResponse:
    """Compute SEO meta tags for a board page.

    Args:
        board: The Board ORM object.

    Returns:
        SEOMetaResponse with computed meta tags.
    """
    title = board.meta_title or f"{board.title} | {SITE_NAME}"
    description_raw = board.meta_description or board.description or DEFAULT_DESCRIPTION
    description = _truncate(description_raw)

    return SEOMetaResponse(
        title=title,
        description=description,
        og_title=title,
        og_description=description,
        canonical_url=f"{SITE_BASE_URL}/boards/{board.slug}",
        og_type="website",
        page_type="board",
    )


def _compute_card_meta(card: Card) -> SEOMetaResponse:
    """Compute SEO meta tags for a card page.

    Args:
        card: The Card ORM object.

    Returns:
        SEOMetaResponse with computed meta tags.
    """
    title = card.meta_title or f"{card.title} | {SITE_NAME}"
    description_raw = card.meta_description or card.description or DEFAULT_DESCRIPTION
    description = _truncate(description_raw)

    return SEOMetaResponse(
        title=title,
        description=description,
        og_title=title,
        og_description=description,
        canonical_url=f"{SITE_BASE_URL}/cards/{card.slug}",
        og_type="article",
        page_type="card",
    )


def _compute_category_meta(category: Category) -> SEOMetaResponse:
    """Compute SEO meta tags for a category page.

    Args:
        category: The Category ORM object.

    Returns:
        SEOMetaResponse with computed meta tags.
    """
    title = category.meta_title or f"{category.name} | {SITE_NAME}"
    description_raw = category.meta_description or category.description or DEFAULT_DESCRIPTION
    description = _truncate(description_raw)

    return SEOMetaResponse(
        title=title,
        description=description,
        og_title=title,
        og_description=description,
        canonical_url=f"{SITE_BASE_URL}/categories/{category.slug}",
        og_type="website",
        page_type="category",
    )


_PAGE_TYPE_HANDLERS = {
    "board": (Board, "slug", _compute_board_meta),
    "card": (Card, "slug", _compute_card_meta),
    "category": (Category, "slug", _compute_category_meta),
}


@router.get(
    "/{page_type}/{slug}",
    response_model=SEOMetaResponse,
    summary="Get computed SEO meta tags for a page",
)
def get_seo_meta(
    page_type: str,
    slug: str,
    db: Session = Depends(get_db),
) -> SEOMetaResponse:
    """Return computed SEO meta tags for a given page type and slug.

    Supported page types: board, card, category.

    The endpoint computes:
    - title (uses meta_title override if set, otherwise generates from resource title)
    - description (uses meta_description override if set, otherwise from resource description)
    - og:title
    - og:description
    - canonical URL

    Args:
        page_type: The resource type (board, card, or category).
        slug: The URL slug identifying the specific resource.
        db: Database session (injected).

    Returns:
        SEOMetaResponse with all computed meta tags.

    Raises:
        HTTPException: 400 if page_type is not supported.
        HTTPException: 404 if the resource is not found.
    """
    handler = _PAGE_TYPE_HANDLERS.get(page_type)
    if handler is None:
        supported = ", ".join(sorted(_PAGE_TYPE_HANDLERS.keys()))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported page type '{page_type}'. Supported types: {supported}.",
        )

    model, slug_field, compute_fn = handler
    column = getattr(model, slug_field)
    stmt = select(model).where(column == slug)
    entity = db.execute(stmt).scalar_one_or_none()

    if entity is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{page_type.capitalize()} with slug '{slug}' not found.",
        )

    return compute_fn(entity)
