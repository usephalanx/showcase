"""FastAPI router for Column CRUD operations.

Endpoints
---------
- GET    /api/boards/{board_id}/columns          List columns for a board.
- POST   /api/boards/{board_id}/columns          Create a column in a board.
- PUT    /api/columns/{column_id}                Update a column.
- DELETE /api/columns/{column_id}                Delete a column.
- PATCH  /api/columns/{column_id}/move           Reposition a column.
"""

from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models import Board, Column

router = APIRouter(tags=["columns"])


def _get_board_or_404(db: Session, board_id: int) -> Board:
    """Return a Board by id or raise 404.

    Args:
        db: Active database session.
        board_id: Primary key of the board.

    Returns:
        The Board instance.

    Raises:
        HTTPException: 404 if board not found.
    """
    board = db.get(Board, board_id)
    if board is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Board with id {board_id} not found.",
        )
    return board


def _get_column_or_404(db: Session, column_id: int) -> Column:
    """Return a Column by id or raise 404.

    Args:
        db: Active database session.
        column_id: Primary key of the column.

    Returns:
        The Column instance.

    Raises:
        HTTPException: 404 if column not found.
    """
    column = db.get(Column, column_id)
    if column is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Column with id {column_id} not found.",
        )
    return column


@router.get("/api/boards/{board_id}/columns", tags=["columns"])
def list_columns(board_id: int, db: Session = Depends(get_db)) -> List[dict]:
    """Return all columns for a board ordered by position."""
    _get_board_or_404(db, board_id)
    columns = (
        db.query(Column)
        .filter(Column.board_id == board_id)
        .order_by(Column.position)
        .all()
    )
    return [
        {"id": c.id, "board_id": c.board_id, "title": c.title, "position": c.position}
        for c in columns
    ]


@router.post(
    "/api/boards/{board_id}/columns",
    status_code=status.HTTP_201_CREATED,
    tags=["columns"],
)
def create_column(board_id: int, payload: dict, db: Session = Depends(get_db)) -> dict:
    """Create a new column within a board.

    Args:
        board_id: Parent board primary key.
        payload: Must contain ``title`` and ``position``.
        db: Database session dependency.
    """
    _get_board_or_404(db, board_id)
    column = Column(
        board_id=board_id,
        title=payload["title"],
        position=payload.get("position", 0),
    )
    db.add(column)
    db.commit()
    db.refresh(column)
    return {"id": column.id, "board_id": column.board_id, "title": column.title, "position": column.position}


@router.put("/api/columns/{column_id}", tags=["columns"])
def update_column(column_id: int, payload: dict, db: Session = Depends(get_db)) -> dict:
    """Update a column's title or position.

    Args:
        column_id: Primary key of the column.
        payload: Fields to update (title, position).
        db: Database session dependency.
    """
    column = _get_column_or_404(db, column_id)
    if "title" in payload:
        column.title = payload["title"]
    if "position" in payload:
        column.position = payload["position"]
    db.commit()
    db.refresh(column)
    return {"id": column.id, "board_id": column.board_id, "title": column.title, "position": column.position}


@router.delete("/api/columns/{column_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["columns"])
def delete_column(column_id: int, db: Session = Depends(get_db)) -> None:
    """Delete a column and all its cards (cascade).

    Args:
        column_id: Primary key of the column.
        db: Database session dependency.
    """
    column = _get_column_or_404(db, column_id)
    db.delete(column)
    db.commit()
