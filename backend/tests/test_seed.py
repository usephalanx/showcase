"""Tests for the seed module."""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.models import Board, Card, Column, User
from app.seed import DEMO_EMAIL, run_seed


def test_seed_creates_demo_data(db_session: Session) -> None:
    """Running seed should create the demo user, board, columns, and cards."""
    run_seed(db_session)

    user = db_session.query(User).filter(User.email == DEMO_EMAIL).first()
    assert user is not None

    boards = db_session.query(Board).filter(Board.user_id == user.id).all()
    assert len(boards) == 1
    assert boards[0].title == "My First Board"

    columns = db_session.query(Column).filter(Column.board_id == boards[0].id).all()
    assert len(columns) == 3

    cards = db_session.query(Card).all()
    assert len(cards) == 3


def test_seed_is_idempotent(db_session: Session) -> None:
    """Running seed twice should not create duplicate data."""
    run_seed(db_session)
    run_seed(db_session)

    users = db_session.query(User).filter(User.email == DEMO_EMAIL).all()
    assert len(users) == 1

    boards = db_session.query(Board).all()
    assert len(boards) == 1
