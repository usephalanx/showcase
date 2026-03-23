"""Seed the database with demo data.

Creates a demo user (demo@phalanx.dev / demo1234) with a sample board,
3 default columns, and 3 sample cards. Runs idempotently — skips if
the demo user already exists.
"""

from __future__ import annotations

import logging

from sqlalchemy.orm import Session

from app.auth import hash_password
from app.models import Board, Card, Column, User

logger = logging.getLogger(__name__)

DEMO_EMAIL = "demo@phalanx.dev"
DEMO_PASSWORD = "demo1234"


def run_seed(db: Session) -> None:
    """Insert demo data if it does not already exist.

    Args:
        db: An active SQLAlchemy session.
    """
    existing = db.query(User).filter(User.email == DEMO_EMAIL).first()
    if existing is not None:
        logger.info("Demo user already exists — skipping seed.")
        return

    logger.info("Seeding demo data…")

    # Create demo user
    user = User(
        email=DEMO_EMAIL,
        hashed_password=hash_password(DEMO_PASSWORD),
    )
    db.add(user)
    db.flush()  # Populate user.id

    # Create sample board
    board = Board(title="My First Board", user_id=user.id)
    db.add(board)
    db.flush()

    # Create 3 default columns
    col_todo = Column(title="To Do", board_id=board.id, position=0)
    col_in_progress = Column(title="In Progress", board_id=board.id, position=1)
    col_done = Column(title="Done", board_id=board.id, position=2)
    db.add_all([col_todo, col_in_progress, col_done])
    db.flush()

    # Create 3 sample cards
    cards = [
        Card(
            title="Set up project structure",
            description="Initialize the backend and frontend project scaffolding.",
            column_id=col_done.id,
            position=0,
        ),
        Card(
            title="Implement authentication",
            description="Add JWT-based register and login endpoints.",
            column_id=col_in_progress.id,
            position=0,
        ),
        Card(
            title="Build the board UI",
            description="Create the drag-and-drop Kanban board interface.",
            column_id=col_todo.id,
            position=0,
        ),
    ]
    db.add_all(cards)
    db.commit()

    logger.info("Demo data seeded successfully.")
