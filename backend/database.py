"""SQLAlchemy engine and session setup for the Todo application.

Uses SQLite as the backing store (todo.db) with SQLAlchemy ORM.
Provides a session factory and a dependency-injection helper for
FastAPI route handlers.
"""

from __future__ import annotations

from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

DATABASE_URL: str = "sqlite:///./todo.db"

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

Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency that yields a SQLAlchemy session.

    The session is automatically closed after the request completes,
    regardless of whether the request succeeded or raised an exception.

    Yields:
        A SQLAlchemy :class:`Session` instance bound to the application
        database engine.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """Create all tables defined by models inheriting from :data:`Base`.

    This function is idempotent — tables that already exist are left
    untouched.
    """
    Base.metadata.create_all(bind=engine)
