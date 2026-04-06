"""Column CRUD routes for the Kanban application.

Provides endpoints for listing columns of a board, creating columns,
updating columns, reordering a column, and deleting columns.
"""

from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from database import get_db
from models import Board, Column
from schemas import ColumnCreate, ColumnResponse, ColumnUpdate

router = APIRouter(tags=["columns"])


class ColumnReorder(BaseModel):
    """Schema for reordering a column to a new position."""

    position: int = Field(..., ge=0, description="New ordering position.")


@router.get(
    "/api/boards/{board_id}/columns",
    response_model=List[ColumnResponse],
)
def list_columns(
    board_id: int,
    db: Session = Depends(get_db),
) -> List[Column]:
    """Return all columns for a given board, ordered by position.

    Args:
        board_id: Primary key of the parent board.
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
    columns = (
        db.query(Column)
        .filter(Column.board_id == board_id)
        .order_by(Column.position)
        .all()
    )
    return columns


@router.post(
    "/api/boards/{board_id}/columns",
    response_model=ColumnResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_column(
    board_id: int,
    payload: ColumnCreate,
    db: Session = Depends(get_db),
) -> Column:
    """Create a new column within a board.

    If position is not specified, the column is appended at the end.
    The board_id in the URL takes precedence over the payload body.

    Args:
        board_id: Primary key of the parent board.
        payload: Column creation data.
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

    # Auto-calculate position if not provided (append at end)
    position = payload.position
    if position == 0:
        max_pos = (
            db.query(Column.position)
            .filter(Column.board_id == board_id)
            .order_by(Column.position.desc())
            .first()
        )
        position = (max_pos[0] + 1) if max_pos else 0

    # Shift existing columns to make room
    _shift_columns_up(db, board_id, position)

    column = Column(
        board_id=board_id,
        title=payload.title,
        position=position,
    )
    db.add(column)
    db.commit()
    db.refresh(column)
    return column


@router.put("/api/columns/{column_id}", response_model=ColumnResponse)
def update_column(
    column_id: int,
    payload: ColumnUpdate,
    db: Session = Depends(get_db),
) -> Column:
    """Update an existing column by its primary key.

    Only supplied fields are updated.

    Args:
        column_id: Primary key of the column.
        payload: Partial update data.
        db: Database session dependency.

    Raises:
        HTTPException: 404 if the column does not exist.
    """
    column = db.query(Column).filter(Column.id == column_id).first()
    if column is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Column with id {column_id} not found.",
        )

    update_data = payload.model_dump(exclude_unset=True)

    if "position" in update_data and update_data["position"] is not None:
        new_pos = update_data["position"]
        if new_pos != column.position:
            _reorder_column(db, column, new_pos)
            # Position already set by reorder helper
            del update_data["position"]

    for field, value in update_data.items():
        setattr(column, field, value)

    db.commit()
    db.refresh(column)
    return column


@router.patch(
    "/api/columns/{column_id}/reorder",
    response_model=ColumnResponse,
)
def reorder_column(
    column_id: int,
    payload: ColumnReorder,
    db: Session = Depends(get_db),
) -> Column:
    """Move a column to a new position within its board.

    Sibling columns are shifted automatically to maintain a
    contiguous ordering sequence.

    Args:
        column_id: Primary key of the column.
        payload: The desired new position.
        db: Database session dependency.

    Raises:
        HTTPException: 404 if the column does not exist.
    """
    column = db.query(Column).filter(Column.id == column_id).first()
    if column is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Column with id {column_id} not found.",
        )

    if payload.position != column.position:
        _reorder_column(db, column, payload.position)

    db.commit()
    db.refresh(column)
    return column


@router.delete(
    "/api/columns/{column_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_column(
    column_id: int,
    db: Session = Depends(get_db),
) -> None:
    """Delete a column and all of its cards (cascade).

    Remaining columns are re-indexed to keep positions contiguous.

    Args:
        column_id: Primary key of the column.
        db: Database session dependency.

    Raises:
        HTTPException: 404 if the column does not exist.
    """
    column = db.query(Column).filter(Column.id == column_id).first()
    if column is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Column with id {column_id} not found.",
        )
    board_id = column.board_id
    old_position = column.position
    db.delete(column)
    db.flush()

    # Shift remaining columns down to fill the gap
    siblings = (
        db.query(Column)
        .filter(Column.board_id == board_id, Column.position > old_position)
        .order_by(Column.position)
        .all()
    )
    for sibling in siblings:
        sibling.position -= 1

    db.commit()


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------


def _shift_columns_up(
    db: Session,
    board_id: int,
    from_position: int,
) -> None:
    """Shift columns at or above *from_position* up by one.

    Used when inserting a new column at a specific position.

    Args:
        db: Active database session.
        board_id: Board whose columns to shift.
        from_position: Position from which to start shifting.
    """
    siblings = (
        db.query(Column)
        .filter(Column.board_id == board_id, Column.position >= from_position)
        .order_by(Column.position.desc())
        .all()
    )
    for sibling in siblings:
        sibling.position += 1


def _reorder_column(
    db: Session,
    column: Column,
    new_position: int,
) -> None:
    """Move a column to a new position and shift siblings accordingly.

    Args:
        db: Active database session.
        column: The column being moved.
        new_position: The desired new position.
    """
    old_position = column.position
    board_id = column.board_id

    if new_position > old_position:
        # Moving down: shift items in (old, new] up by one
        siblings = (
            db.query(Column)
            .filter(
                Column.board_id == board_id,
                Column.position > old_position,
                Column.position <= new_position,
                Column.id != column.id,
            )
            .order_by(Column.position)
            .all()
        )
        for sibling in siblings:
            sibling.position -= 1
    elif new_position < old_position:
        # Moving up: shift items in [new, old) down by one
        siblings = (
            db.query(Column)
            .filter(
                Column.board_id == board_id,
                Column.position >= new_position,
                Column.position < old_position,
                Column.id != column.id,
            )
            .order_by(Column.position.desc())
            .all()
        )
        for sibling in siblings:
            sibling.position += 1

    column.position = new_position
