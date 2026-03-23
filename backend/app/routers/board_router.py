"""Board CRUD endpoints with JWT authentication and ownership validation."""

from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models import Board, Column, User
from app.schemas import BoardCreate, BoardDetailResponse, BoardResponse, ColumnCreate, ColumnResponse

router = APIRouter(prefix="/boards", tags=["boards"])

DEFAULT_COLUMNS = ["To Do", "In Progress", "Done"]


def _get_board_or_404(
    board_id: int,
    user: User,
    db: Session,
) -> Board:
    """Fetch a board by ID and verify ownership.

    Args:
        board_id: The board primary key.
        user: The authenticated user.
        db: Database session.

    Returns:
        The Board ORM instance.

    Raises:
        HTTPException: 404 if not found or not owned by the user.
    """
    board = db.query(Board).filter(Board.id == board_id).first()
    if board is None or board.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Board not found",
        )
    return board


@router.get("", response_model=List[BoardResponse])
def list_boards(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[Board]:
    """List all boards for the authenticated user."""
    boards = (
        db.query(Board)
        .filter(Board.user_id == current_user.id)
        .order_by(Board.created_at.desc())
        .all()
    )
    return boards


@router.post("", response_model=BoardDetailResponse, status_code=status.HTTP_201_CREATED)
def create_board(
    payload: BoardCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Board:
    """Create a new board with default columns (To Do, In Progress, Done)."""
    board = Board(title=payload.title, user_id=current_user.id)
    db.add(board)
    db.flush()

    for position, title in enumerate(DEFAULT_COLUMNS):
        col = Column(title=title, board_id=board.id, position=position)
        db.add(col)

    db.commit()
    db.refresh(board)
    return board


@router.get("/{board_id}", response_model=BoardDetailResponse)
def get_board(
    board_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Board:
    """Get a board with its columns and cards. Verifies ownership."""
    board = _get_board_or_404(board_id, current_user, db)
    return board


@router.delete("/{board_id}", status_code=status.HTTP_200_OK)
def delete_board(
    board_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict[str, str]:
    """Delete a board and cascade-delete its columns and cards."""
    board = _get_board_or_404(board_id, current_user, db)
    db.delete(board)
    db.commit()
    return {"detail": "Board deleted successfully"}


@router.post("/{board_id}/columns", response_model=ColumnResponse, status_code=status.HTTP_201_CREATED)
def create_column(
    board_id: int,
    payload: ColumnCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Column:
    """Add a new column to a board."""
    board = _get_board_or_404(board_id, current_user, db)

    # Auto-assign position if not explicitly set to a meaningful value.
    # Default: append to the end.
    max_position = (
        db.query(Column.position)
        .filter(Column.board_id == board.id)
        .order_by(Column.position.desc())
        .first()
    )
    next_position = (max_position[0] + 1) if max_position else 0

    # Use provided position or auto-assign
    position = payload.position if payload.position > 0 else next_position
    # If position == 0 and there are already columns, still auto-assign to end
    # unless explicitly requested
    if payload.position == 0 and max_position is not None:
        position = next_position

    column = Column(title=payload.title, board_id=board.id, position=position)
    db.add(column)
    db.commit()
    db.refresh(column)
    return column


@router.get("/{board_id}/cards", response_model=List[ColumnResponse])
def get_board_cards(
    board_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[Column]:
    """Get all cards for a board grouped by column, including card count per column."""
    board = _get_board_or_404(board_id, current_user, db)
    columns = (
        db.query(Column)
        .filter(Column.board_id == board.id)
        .order_by(Column.position)
        .all()
    )
    return columns
