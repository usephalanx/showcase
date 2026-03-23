"""Tests for SQLAlchemy ORM models and relationships."""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.auth import hash_password
from app.models import Board, Card, Column, User


def test_create_user(db_session: Session) -> None:
    """Should create a user and retrieve it."""
    user = User(email="u@test.com", hashed_password=hash_password("pw"))
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    assert user.id is not None
    assert user.email == "u@test.com"
    assert user.created_at is not None


def test_board_user_relationship(db_session: Session) -> None:
    """Board should belong to a user."""
    user = User(email="board@test.com", hashed_password="x")
    db_session.add(user)
    db_session.flush()

    board = Board(title="Test Board", user_id=user.id)
    db_session.add(board)
    db_session.commit()
    db_session.refresh(board)

    assert board.owner.id == user.id
    assert len(user.boards) == 1


def test_column_board_relationship(db_session: Session) -> None:
    """Columns should belong to a board and be ordered by position."""
    user = User(email="col@test.com", hashed_password="x")
    db_session.add(user)
    db_session.flush()

    board = Board(title="B", user_id=user.id)
    db_session.add(board)
    db_session.flush()

    c1 = Column(title="Done", board_id=board.id, position=2)
    c2 = Column(title="To Do", board_id=board.id, position=0)
    c3 = Column(title="In Progress", board_id=board.id, position=1)
    db_session.add_all([c1, c2, c3])
    db_session.commit()
    db_session.refresh(board)

    titles = [c.title for c in board.columns]
    assert titles == ["To Do", "In Progress", "Done"]


def test_card_column_relationship(db_session: Session) -> None:
    """Cards should belong to a column and be ordered by position."""
    user = User(email="card@test.com", hashed_password="x")
    db_session.add(user)
    db_session.flush()

    board = Board(title="B", user_id=user.id)
    db_session.add(board)
    db_session.flush()

    col = Column(title="Col", board_id=board.id, position=0)
    db_session.add(col)
    db_session.flush()

    card1 = Card(title="Second", column_id=col.id, position=1)
    card2 = Card(title="First", column_id=col.id, position=0)
    db_session.add_all([card1, card2])
    db_session.commit()
    db_session.refresh(col)

    titles = [c.title for c in col.cards]
    assert titles == ["First", "Second"]


def test_cascade_delete_user(db_session: Session) -> None:
    """Deleting a user should cascade-delete boards, columns, and cards."""
    user = User(email="cascade@test.com", hashed_password="x")
    db_session.add(user)
    db_session.flush()

    board = Board(title="B", user_id=user.id)
    db_session.add(board)
    db_session.flush()

    col = Column(title="C", board_id=board.id, position=0)
    db_session.add(col)
    db_session.flush()

    card = Card(title="Card", column_id=col.id, position=0)
    db_session.add(card)
    db_session.commit()

    db_session.delete(user)
    db_session.commit()

    assert db_session.query(Board).count() == 0
    assert db_session.query(Column).count() == 0
    assert db_session.query(Card).count() == 0
