"""Card CRUD and move endpoints with JWT authentication and ownership validation."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models import Board, Card, Column, User
from app.schemas import CardCreate, CardMoveRequest, CardResponse, CardUpdate

router = APIRouter(prefix="/cards", tags=["cards"])


def _verify_column_ownership(
    column_id: int,
    user: User,
    db: Session,
) -> Column:
    """Verify that a column exists and belongs to a board owned by the user.

    Args:
        column_id: The column primary key.
        user: The authenticated user.
        db: Database session.

    Returns:
        The Column ORM instance.

    Raises:
        HTTPException: 404 if not found or not owned by the user.
    """
    column = db.query(Column).filter(Column.id == column_id).first()
    if column is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Column not found",
        )
    board = db.query(Board).filter(Board.id == column.board_id).first()
    if board is None or board.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Column not found",
        )
    return column


def _get_card_or_404(
    card_id: int,
    user: User,
    db: Session,
) -> Card:
    """Fetch a card by ID and verify ownership through column -> board -> user.

    Args:
        card_id: The card primary key.
        user: The authenticated user.
        db: Database session.

    Returns:
        The Card ORM instance.

    Raises:
        HTTPException: 404 if not found or not owned by the user.
    """
    card = db.query(Card).filter(Card.id == card_id).first()
    if card is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Card not found",
        )
    column = db.query(Column).filter(Column.id == card.column_id).first()
    if column is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Card not found",
        )
    board = db.query(Board).filter(Board.id == column.board_id).first()
    if board is None or board.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Card not found",
        )
    return card


def _reindex_column(column_id: int, db: Session) -> None:
    """Reindex card positions in a column sequentially (0, 1, 2, ...).

    Args:
        column_id: The column to reindex.
        db: Database session.
    """
    cards = (
        db.query(Card)
        .filter(Card.column_id == column_id)
        .order_by(Card.position)
        .all()
    )
    for idx, card in enumerate(cards):
        if card.position != idx:
            card.position = idx


@router.post("", response_model=CardResponse, status_code=status.HTTP_201_CREATED)
def create_card(
    payload: CardCreate,
    column_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Card:
    """Create a new card in a specific column. Auto-assigns position to end."""
    column = _verify_column_ownership(column_id, current_user, db)

    # Auto-assign position: append to end
    max_pos = (
        db.query(Card.position)
        .filter(Card.column_id == column.id)
        .order_by(Card.position.desc())
        .first()
    )
    next_position = (max_pos[0] + 1) if max_pos else 0

    card = Card(
        title=payload.title,
        description=payload.description,
        column_id=column.id,
        position=next_position,
    )
    db.add(card)
    db.commit()
    db.refresh(card)
    return card


@router.patch("/{card_id}", response_model=CardResponse)
def update_card(
    card_id: int,
    payload: CardUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Card:
    """Update a card's title and/or description."""
    card = _get_card_or_404(card_id, current_user, db)

    if payload.title is not None:
        card.title = payload.title
    if payload.description is not None:
        card.description = payload.description

    db.commit()
    db.refresh(card)
    return card


@router.delete("/{card_id}", status_code=status.HTTP_200_OK)
def delete_card(
    card_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict[str, str]:
    """Delete a card and reorder remaining positions in the column."""
    card = _get_card_or_404(card_id, current_user, db)
    column_id = card.column_id

    db.delete(card)
    db.flush()

    # Reindex remaining cards in the column
    _reindex_column(column_id, db)
    db.commit()

    return {"detail": "Card deleted successfully"}


@router.post("/{card_id}/move", response_model=CardResponse)
def move_card(
    card_id: int,
    payload: CardMoveRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Card:
    """Move a card to a target column and position.

    Reorders affected cards in both source and target columns atomically.
    """
    card = _get_card_or_404(card_id, current_user, db)

    # Validate target column ownership
    target_column = _verify_column_ownership(payload.column_id, current_user, db)

    source_column_id = card.column_id
    target_column_id = target_column.id
    target_position = payload.position

    if source_column_id == target_column_id:
        # Moving within the same column
        cards_in_column = (
            db.query(Card)
            .filter(Card.column_id == source_column_id)
            .order_by(Card.position)
            .all()
        )

        # Remove card from its current position
        cards_in_column = [c for c in cards_in_column if c.id != card.id]

        # Clamp target position
        target_position = min(target_position, len(cards_in_column))

        # Insert card at target position
        cards_in_column.insert(target_position, card)

        # Reindex
        for idx, c in enumerate(cards_in_column):
            c.position = idx
    else:
        # Moving between columns

        # Remove card from source column and reindex
        card.column_id = target_column_id

        # Get remaining cards in source column (excluding moved card)
        source_cards = (
            db.query(Card)
            .filter(Card.column_id == source_column_id, Card.id != card.id)
            .order_by(Card.position)
            .all()
        )
        for idx, c in enumerate(source_cards):
            c.position = idx

        # Get current cards in target column (excluding the moved card which now has new column_id)
        target_cards = (
            db.query(Card)
            .filter(Card.column_id == target_column_id, Card.id != card.id)
            .order_by(Card.position)
            .all()
        )

        # Clamp target position
        target_position = min(target_position, len(target_cards))

        # Insert card into target list
        target_cards.insert(target_position, card)

        # Reindex target column
        for idx, c in enumerate(target_cards):
            c.position = idx

    db.commit()
    db.refresh(card)
    return card
