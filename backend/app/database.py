"""SQLite database configuration using SQLAlchemy.

Provides the engine, session factory, and declarative Base for the
Todo application.  Tables are auto-created on startup via
:func:`init_db`.
"""

from __future__ import annotations

import os
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./tasks.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False,
)

SessionLocal: sessionmaker[Session] = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


class Base(DeclarativeBase):
    """Declarative base class for all ORM models."""


def init_db() -> None:
    """Create all tables that do not yet exist in the database.

    Must be called **after** all model modules have been imported so
    that :attr:`Base.metadata` contains the full schema.
    """
    Base.metadata.create_all(bind=engine)


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency that yields a database session.

    The session is automatically closed when the request finishes.

    Yields:
        A SQLAlchemy :class:`Session` instance.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
