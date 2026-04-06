"""SQLite database configuration using SQLAlchemy.

Provides the engine, session factory, and declarative base for the
Todo application.  Uses ``check_same_thread=False`` so the SQLite
connection can be shared across ASGI worker threads.
"""

from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

SQLALCHEMY_DATABASE_URL: str = "sqlite:///./todos.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """Declarative base class for all ORM models."""

    pass


def get_db():
    """Yield a database session and ensure it is closed after use.

    Yields:
        sqlalchemy.orm.Session: An active database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
