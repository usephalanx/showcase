"""SQLite database connection and session management for the Kanban application.

Provides engine creation, session factory, and schema initialization
using SQLAlchemy 2.0. Uses a file-based SQLite database (kanban.db)
with WAL mode and foreign key enforcement enabled.
"""

from __future__ import annotations

from typing import Generator

from sqlalchemy import Engine, event, create_engine
from sqlalchemy.orm import Session, sessionmaker

from models import Base

DATABASE_URL: str = "sqlite:///kanban.db"

engine: Engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False,
)

SessionLocal: sessionmaker[Session] = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


@event.listens_for(engine, "connect")
def _set_sqlite_pragma(dbapi_connection: object, connection_record: object) -> None:
    """Enable SQLite WAL mode and foreign key enforcement on every connection.

    Args:
        dbapi_connection: The raw DBAPI connection.
        connection_record: The connection record (unused).
    """
    cursor = dbapi_connection.cursor()  # type: ignore[union-attr]
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


def init_db() -> None:
    """Create all tables defined in the ORM metadata.

    This is idempotent — tables that already exist are not recreated.
    Should be called once at application startup.
    """
    Base.metadata.create_all(bind=engine)


def get_db() -> Generator[Session, None, None]:
    """Yield a SQLAlchemy session for dependency injection.

    Intended for use with FastAPI's ``Depends()`` mechanism. The session
    is automatically closed after the request completes.

    Yields:
        A SQLAlchemy Session instance.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
