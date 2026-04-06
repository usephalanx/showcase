"""FastAPI router for Card CRUD operations.

Endpoints
---------
- GET    /api/cards              List cards with optional filters.
- GET    /api/cards/{slug}       Get a single card by slug.
- POST   /api/columns/{column_id}/cards  Create a card in a column.
- PUT    /api/cards/{card_id}    Full update of a card.
- PATCH  /api/cards/{card_id}/move  Move card between columns/positions.
- DELETE /api/cards/{card_id}    Delete a card.
- POST   /api/cards/{card_id}/categories  Associate a category.
- DELETE /api/cards/{card_id}/categories/{category_id}  Remove association.
"""

from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from database import get_db
from models import Card, Category, Column, card_categories
from schemas import (
    CardCategoryAction,
    CardCreate,
    CardMove,
    CardResponse,
    CardUpdate,
    CategoryResponse,
)
from utils.slug import generate_unique_slug

router = APIRouter(tags=["cards"])


def _get_card_by_id(db: Session, card_id: int) -> Card:
    """Fetch a card by primary key or raise 404.

    Args:
        db: Active database session.
        card_id: The card's primary key.

    Returns:
        The Card instance.

    Raises:
        HTTPException: 404 if the card does not exist.
    """
    card = db.get(Card, card_id)
    if card is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Card with id {card_id} not found.",
        )
    return card


def _get_column_by_id(db: Session, column_id: int) -> Column:
    """Fetch a column by primary key or raise 404.

    Args:
        db: Active database session.
        column_id: The column's primary key.

    Returns:
        The Column instance.

    Raises:
        HTTPException: 404 if the column does not exist.
    """
    column = db.get(Column, column_id)
    if column is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Column with id {column_id} not found.",
        )
    return column


def _get_category_by_id(db: Session, category_id: int) -> Category:
    """Fetch a category by primary key or raise 404.

    Args:
        db: Active database session.
        category_id: The category's primary key.

    Returns:
        The Category instance.

    Raises:
        HTTPException: 404 if the category does not exist.
    """
    category = db.get(Category, category_id)
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with id {category_id} not found.",
        )
    return category


# ---------------------------------------------------------------------------
# List cards (with optional category filter)
# ---------------------------------------------------------------------------


@router.get(
    "/api/cards",
    response_model=List[CardResponse],
    status_code=status.HTTP_200_OK,
    summary="List cards",
    description="Retrieve all cards, optionally filtered by category slug.",
)
def list_cards(
    category: Optional[str] = Query(
        None,
        description="Filter cards by category slug.",
    ),
    column_id: Optional[int] = Query(
        None,
        description="Filter cards by column ID.",
    ),
    db: Session = Depends(get_db),
) -> List[Card]:
    """Return a list of cards, optionally filtered by category slug or column.

    Args:
        category: Optional category slug to filter by.
        column_id: Optional column ID to filter by.
        db: Active database session.

    Returns:
        List of Card instances matching the filters.
    """
    query = select(Card).options(selectinload(Card.categories))

    if category is not None:
        query = (
            query
            .join(card_categories, Card.id == card_categories.c.card_id)
            .join(Category, Category.id == card_categories.c.category_id)
            .where(Category.slug == category)
        )

    if column_id is not None:
        query = query.where(Card.column_id == column_id)

    query = query.order_by(Card.position)
    result = db.execute(query).scalars().all()
    return list(result)


# ---------------------------------------------------------------------------
# Get card by slug
# ---------------------------------------------------------------------------


@router.get(
    "/api/cards/{slug}",
    response_model=CardResponse,
    status_code=status.HTTP_200_OK,
    summary="Get card by slug",
    description="Retrieve a single card by its SEO-friendly slug.",
)
def get_card_by_slug(
    slug: str,
    db: Session = Depends(get_db),
) -> Card:
    """Return a single card identified by its unique slug.

    Args:
        slug: The card's URL-friendly slug.
        db: Active database session.

    Returns:
        The matching Card instance.

    Raises:
        HTTPException: 404 if no card with the given slug exists.
    """
    query = (
        select(Card)
        .options(selectinload(Card.categories))
        .where(Card.slug == slug)
    )
    card = db.execute(query).scalar_one_or_none()
    if card is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Card with slug '{slug}' not found.",
        )
    return card


# ---------------------------------------------------------------------------
# Create card in a column
# ---------------------------------------------------------------------------


@router.post(
    "/api/columns/{column_id}/cards",
    response_model=CardResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a card",
    description="Create a new card within the specified column.",
)
def create_card(
    column_id: int,
    payload: CardCreate,
    db: Session = Depends(get_db),
) -> Card:
    """Create a new card in the given column.

    Args:
        column_id: The parent column's primary key.
        payload: Card creation data.
        db: Active database session.

    Returns:
        The newly created Card instance.

    Raises:
        HTTPException: 404 if the column does not exist.
    """
    _get_column_by_id(db, column_id)

    slug = generate_unique_slug(db, Card, payload.title)

    card = Card(
        column_id=column_id,
        title=payload.title,
        slug=slug,
        description=payload.description,
        position=payload.position,
        meta_title=payload.meta_title,
        meta_description=payload.meta_description,
    )
    db.add(card)
    db.commit()
    db.refresh(card)
    return card


# ---------------------------------------------------------------------------
# Update card (full)
# ---------------------------------------------------------------------------


@router.put(
    "/api/cards/{card_id}",
    response_model=CardResponse,
    status_code=status.HTTP_200_OK,
    summary="Update a card",
    description="Update an existing card's fields.",
)
def update_card(
    card_id: int,
    payload: CardUpdate,
    db: Session = Depends(get_db),
) -> Card:
    """Update an existing card.

    Only fields provided in the payload are modified.

    Args:
        card_id: The card's primary key.
        payload: Fields to update.
        db: Active database session.

    Returns:
        The updated Card instance.

    Raises:
        HTTPException: 404 if the card does not exist.
    """
    card = _get_card_by_id(db, card_id)

    update_data = payload.model_dump(exclude_unset=True)

    # Regenerate slug if title changes
    if "title" in update_data and update_data["title"] is not None:
        update_data["slug"] = generate_unique_slug(
            db, Card, update_data["title"], current_id=card.id,
        )

    for field, value in update_data.items():
        setattr(card, field, value)

    db.commit()
    db.refresh(card)
    return card


# ---------------------------------------------------------------------------
# Move card
# ---------------------------------------------------------------------------


@router.patch(
    "/api/cards/{card_id}/move",
    response_model=CardResponse,
    status_code=status.HTTP_200_OK,
    summary="Move a card",
    description="Move a card to a different column and/or position.",
)
def move_card(
    card_id: int,
    payload: CardMove,
    db: Session = Depends(get_db),
) -> Card:
    """Move a card to a different column and/or position.

    Args:
        card_id: The card's primary key.
        payload: Target column_id and position.
        db: Active database session.

    Returns:
        The updated Card instance.

    Raises:
        HTTPException: 404 if the card or target column does not exist.
    """
    card = _get_card_by_id(db, card_id)
    _get_column_by_id(db, payload.column_id)

    card.column_id = payload.column_id
    card.position = payload.position

    db.commit()
    db.refresh(card)
    return card


# ---------------------------------------------------------------------------
# Delete card
# ---------------------------------------------------------------------------


@router.delete(
    "/api/cards/{card_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a card",
    description="Permanently delete a card.",
)
def delete_card(
    card_id: int,
    db: Session = Depends(get_db),
) -> None:
    """Delete a card by its primary key.

    Args:
        card_id: The card's primary key.
        db: Active database session.

    Raises:
        HTTPException: 404 if the card does not exist.
    """
    card = _get_card_by_id(db, card_id)
    db.delete(card)
    db.commit()
    return None


# ---------------------------------------------------------------------------
# Card-Category associations
# ---------------------------------------------------------------------------


@router.post(
    "/api/cards/{card_id}/categories",
    response_model=CardResponse,
    status_code=status.HTTP_200_OK,
    summary="Add category to card",
    description="Associate a category with a card.",
)
def add_category_to_card(
    card_id: int,
    payload: CardCategoryAction,
    db: Session = Depends(get_db),
) -> Card:
    """Associate a category with a card.

    Args:
        card_id: The card's primary key.
        payload: Contains the category_id to associate.
        db: Active database session.

    Returns:
        The updated Card instance with its categories.

    Raises:
        HTTPException: 404 if card or category not found.
        HTTPException: 409 if the association already exists.
    """
    card = _get_card_by_id(db, card_id)
    category = _get_category_by_id(db, payload.category_id)

    if category in card.categories:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Card {card_id} is already associated with category {payload.category_id}.",
        )

    card.categories.append(category)
    db.commit()
    db.refresh(card)
    return card


@router.delete(
    "/api/cards/{card_id}/categories/{category_id}",
    response_model=CardResponse,
    status_code=status.HTTP_200_OK,
    summary="Remove category from card",
    description="Remove the association between a card and a category.",
)
def remove_category_from_card(
    card_id: int,
    category_id: int,
    db: Session = Depends(get_db),
) -> Card:
    """Remove a category association from a card.

    Args:
        card_id: The card's primary key.
        category_id: The category's primary key.
        db: Active database session.

    Returns:
        The updated Card instance with remaining categories.

    Raises:
        HTTPException: 404 if card or category not found, or not associated.
    """
    card = _get_card_by_id(db, card_id)
    category = _get_category_by_id(db, category_id)

    if category not in card.categories:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Card {card_id} is not associated with category {category_id}.",
        )

    card.categories.remove(category)
    db.commit()
    db.refresh(card)
    return card
