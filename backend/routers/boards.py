"""Board CRUD routes for the Kanban application.

Provides endpoints for listing, retrieving (by slug), creating,
updating, and deleting boards.  Slugs are auto-generated from the
board title on create and update.
"""

from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models import Board
from schemas import BoardCreate, BoardResponse, BoardUpdate
from utils.slug import generate_unique_slug

router = APIRouter(prefix="/api/boards", tags=["boards"])


@router.get("", response_model=List[BoardResponse])
def list_boards(db: Session = Depends(get_db)) -> List[Board]:
    """Return all boards ordered by creation date descending."""
    boards = db.query(Board).order_by(Board.created_at.desc()).all()
    return boards


@router.get("/{slug}", response_model=BoardResponse)
def get_board_by_slug(slug: str, db: Session = Depends(get_db)) -> Board:
    """Return a single board looked up by its SEO-friendly slug.

    Args:
        slug: The unique URL slug of the board.
        db: Database session dependency.

    Raises:
        HTTPException: 404 if no board matches the slug.
    """
    board = db.query(Board).filter(Board.slug == slug).first()
    if board is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Board with slug '{slug}' not found.",
        )
    return board


@router.post("", response_model=BoardResponse, status_code=status.HTTP_201_CREATED)
def create_board(
    payload: BoardCreate,
    db: Session = Depends(get_db),
) -> Board:
    """Create a new board with an auto-generated slug.

    The slug is derived from the board title.  If a collision exists a
    numeric suffix (-1, -2, …) is appended automatically.

    Args:
        payload: Board creation data.
        db: Database session dependency.
    """
    slug = generate_unique_slug(db=db, model=Board, value=payload.title)
    board = Board(
        title=payload.title,
        slug=slug,
        description=payload.description,
        meta_title=payload.meta_title,
        meta_description=payload.meta_description,
    )
    db.add(board)
    db.commit()
    db.refresh(board)
    return board


@router.put("/{board_id}", response_model=BoardResponse)
def update_board(
    board_id: int,
    payload: BoardUpdate,
    db: Session = Depends(get_db),
) -> Board:
    """Update an existing board by its primary key.

    If the title changes the slug is regenerated.  Only supplied fields
    are updated.

    Args:
        board_id: Primary key of the board.
        payload: Partial update data.
        db: Database session dependency.

    Raises:
        HTTPException: 404 if the board does not exist.
    """
    board = db.query(Board).filter(Board.id == board_id).first()
    if board is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Board with id {board_id} not found.",
        )

    update_data = payload.model_dump(exclude_unset=True)

    # Regenerate slug when the title changes
    if "title" in update_data and update_data["title"] is not None:
        update_data["slug"] = generate_unique_slug(
            db=db,
            model=Board,
            value=update_data["title"],
            current_id=board_id,
        )

    for field, value in update_data.items():
        setattr(board, field, value)

    db.commit()
    db.refresh(board)
    return board


@router.delete("/{board_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_board(
    board_id: int,
    db: Session = Depends(get_db),
) -> None:
    """Delete a board and all of its columns/cards (cascade).

    Args:
        board_id: Primary key of the board.
        db: Database session dependency.

    Raises:
        HTTPException: 404 if the board does not exist.
    """
    board = db.query(Board).filter(Board.id == board_id).first()
    if board is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Board with id {board_id} not found.",
        )
    db.delete(board)
    db.commit()
