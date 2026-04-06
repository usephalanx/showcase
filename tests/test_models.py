"""Tests for SQLAlchemy ORM models.

Uses an in-memory SQLite database for isolation and speed.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Generator

import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session, sessionmaker

from models import Base, Board, Card, Column, Tag, card_tags


@pytest.fixture()
def db_session() -> Generator[Session, None, None]:
    """Create a fresh in-memory SQLite database and session for each test."""
    engine = create_engine("sqlite:///:memory:", echo=False)

    @event.listens_for(engine, "connect")
    def _set_pragma(dbapi_conn: object, rec: object) -> None:
        """Enable foreign keys for the test database."""
        cursor = dbapi_conn.cursor()  # type: ignore[union-attr]
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    Base.metadata.create_all(bind=engine)
    TestSession = sessionmaker(bind=engine)
    session = TestSession()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


class TestBoardModel:
    """Tests for the Board model."""

    def test_create_board(self, db_session: Session) -> None:
        """Test creating a board with required fields."""
        board = Board(title="Test Board", slug="test-board")
        db_session.add(board)
        db_session.commit()
        db_session.refresh(board)

        assert board.id is not None
        assert board.title == "Test Board"
        assert board.slug == "test-board"
        assert board.description is None
        assert board.meta_title is None
        assert board.meta_description is None
        assert isinstance(board.created_at, datetime)
        assert isinstance(board.updated_at, datetime)

    def test_board_slug_unique(self, db_session: Session) -> None:
        """Test that board slugs must be unique."""
        board1 = Board(title="Board 1", slug="same-slug")
        board2 = Board(title="Board 2", slug="same-slug")
        db_session.add(board1)
        db_session.commit()
        db_session.add(board2)
        with pytest.raises(Exception):  # IntegrityError
            db_session.commit()

    def test_board_with_all_fields(self, db_session: Session) -> None:
        """Test creating a board with all optional fields."""
        board = Board(
            title="Full Board",
            slug="full-board",
            description="A detailed description",
            meta_title="SEO Title",
            meta_description="SEO Description for search engines",
        )
        db_session.add(board)
        db_session.commit()
        db_session.refresh(board)

        assert board.description == "A detailed description"
        assert board.meta_title == "SEO Title"
        assert board.meta_description == "SEO Description for search engines"

    def test_board_repr(self, db_session: Session) -> None:
        """Test the Board __repr__ method."""
        board = Board(title="Test", slug="test")
        db_session.add(board)
        db_session.commit()
        db_session.refresh(board)

        assert "test" in repr(board)
        assert "Board" in repr(board)


class TestColumnModel:
    """Tests for the Column model."""

    def test_create_column(self, db_session: Session) -> None:
        """Test creating a column linked to a board."""
        board = Board(title="Board", slug="board")
        db_session.add(board)
        db_session.commit()

        col = Column(title="To Do", board_id=board.id, position=0)
        db_session.add(col)
        db_session.commit()
        db_session.refresh(col)

        assert col.id is not None
        assert col.board_id == board.id
        assert col.title == "To Do"
        assert col.position == 0

    def test_column_default_position(self, db_session: Session) -> None:
        """Test that column position defaults to 0."""
        board = Board(title="Board", slug="board")
        db_session.add(board)
        db_session.commit()

        col = Column(title="Backlog", board_id=board.id)
        db_session.add(col)
        db_session.commit()
        db_session.refresh(col)

        assert col.position == 0

    def test_column_board_relationship(self, db_session: Session) -> None:
        """Test the bidirectional relationship between Column and Board."""
        board = Board(title="Board", slug="board")
        db_session.add(board)
        db_session.commit()

        col = Column(title="In Progress", board_id=board.id, position=1)
        db_session.add(col)
        db_session.commit()
        db_session.refresh(board)

        assert len(board.columns) == 1
        assert board.columns[0].title == "In Progress"
        assert col.board.title == "Board"

    def test_column_cascade_delete(self, db_session: Session) -> None:
        """Test that deleting a board cascades to its columns."""
        board = Board(title="Board", slug="board")
        db_session.add(board)
        db_session.commit()

        col = Column(title="Done", board_id=board.id, position=0)
        db_session.add(col)
        db_session.commit()

        col_id = col.id
        db_session.delete(board)
        db_session.commit()

        result = db_session.get(Column, col_id)
        assert result is None

    def test_column_repr(self, db_session: Session) -> None:
        """Test the Column __repr__ method."""
        board = Board(title="Board", slug="board")
        db_session.add(board)
        db_session.commit()

        col = Column(title="To Do", board_id=board.id, position=0)
        db_session.add(col)
        db_session.commit()

        assert "To Do" in repr(col)
        assert "Column" in repr(col)


class TestCardModel:
    """Tests for the Card model."""

    def _create_board_and_column(self, db_session: Session) -> Column:
        """Helper to create a board with a column."""
        board = Board(title="Board", slug="board")
        db_session.add(board)
        db_session.commit()
        col = Column(title="To Do", board_id=board.id, position=0)
        db_session.add(col)
        db_session.commit()
        return col

    def test_create_card(self, db_session: Session) -> None:
        """Test creating a card with required fields."""
        col = self._create_board_and_column(db_session)
        card = Card(
            title="My Task",
            slug="my-task",
            column_id=col.id,
            position=0,
        )
        db_session.add(card)
        db_session.commit()
        db_session.refresh(card)

        assert card.id is not None
        assert card.title == "My Task"
        assert card.slug == "my-task"
        assert card.column_id == col.id
        assert card.position == 0
        assert card.description is None
        assert isinstance(card.created_at, datetime)
        assert isinstance(card.updated_at, datetime)

    def test_card_slug_globally_unique(self, db_session: Session) -> None:
        """Test that card slugs are unique across all columns."""
        board = Board(title="Board", slug="board")
        db_session.add(board)
        db_session.commit()

        col1 = Column(title="Col 1", board_id=board.id, position=0)
        col2 = Column(title="Col 2", board_id=board.id, position=1)
        db_session.add_all([col1, col2])
        db_session.commit()

        card1 = Card(title="Task", slug="task", column_id=col1.id, position=0)
        card2 = Card(title="Task", slug="task", column_id=col2.id, position=0)
        db_session.add(card1)
        db_session.commit()
        db_session.add(card2)

        with pytest.raises(Exception):  # IntegrityError
            db_session.commit()

    def test_card_with_description(self, db_session: Session) -> None:
        """Test creating a card with a description."""
        col = self._create_board_and_column(db_session)
        card = Card(
            title="Detailed Task",
            slug="detailed-task",
            column_id=col.id,
            position=0,
            description="This is a detailed description.",
        )
        db_session.add(card)
        db_session.commit()
        db_session.refresh(card)

        assert card.description == "This is a detailed description."

    def test_card_column_relationship(self, db_session: Session) -> None:
        """Test the bidirectional relationship between Card and Column."""
        col = self._create_board_and_column(db_session)
        card = Card(title="Task", slug="task", column_id=col.id, position=0)
        db_session.add(card)
        db_session.commit()
        db_session.refresh(col)

        assert len(col.cards) == 1
        assert col.cards[0].title == "Task"
        assert card.column.title == "To Do"

    def test_card_cascade_delete_column(self, db_session: Session) -> None:
        """Test that deleting a column cascades to its cards."""
        col = self._create_board_and_column(db_session)
        card = Card(title="Task", slug="task", column_id=col.id, position=0)
        db_session.add(card)
        db_session.commit()

        card_id = card.id
        db_session.delete(col)
        db_session.commit()

        result = db_session.get(Card, card_id)
        assert result is None

    def test_card_cascade_delete_board(self, db_session: Session) -> None:
        """Test that deleting a board cascades through columns to cards."""
        board = Board(title="Board", slug="board")
        db_session.add(board)
        db_session.commit()
        col = Column(title="Col", board_id=board.id, position=0)
        db_session.add(col)
        db_session.commit()
        card = Card(title="Task", slug="task", column_id=col.id, position=0)
        db_session.add(card)
        db_session.commit()

        card_id = card.id
        db_session.delete(board)
        db_session.commit()

        result = db_session.get(Card, card_id)
        assert result is None

    def test_card_repr(self, db_session: Session) -> None:
        """Test the Card __repr__ method."""
        col = self._create_board_and_column(db_session)
        card = Card(title="Task", slug="task", column_id=col.id, position=0)
        db_session.add(card)
        db_session.commit()

        assert "task" in repr(card)
        assert "Card" in repr(card)


class TestTagModel:
    """Tests for the Tag model."""

    def test_create_tag(self, db_session: Session) -> None:
        """Test creating a tag with required fields."""
        tag = Tag(name="Urgent", slug="urgent")
        db_session.add(tag)
        db_session.commit()
        db_session.refresh(tag)

        assert tag.id is not None
        assert tag.name == "Urgent"
        assert tag.slug == "urgent"
        assert tag.color == "#6b7280"  # default

    def test_tag_custom_color(self, db_session: Session) -> None:
        """Test creating a tag with a custom color."""
        tag = Tag(name="Bug", slug="bug", color="#ef4444")
        db_session.add(tag)
        db_session.commit()
        db_session.refresh(tag)

        assert tag.color == "#ef4444"

    def test_tag_slug_unique(self, db_session: Session) -> None:
        """Test that tag slugs must be unique."""
        tag1 = Tag(name="Bug", slug="bug")
        tag2 = Tag(name="Another Bug", slug="bug")
        db_session.add(tag1)
        db_session.commit()
        db_session.add(tag2)

        with pytest.raises(Exception):  # IntegrityError
            db_session.commit()

    def test_tag_repr(self, db_session: Session) -> None:
        """Test the Tag __repr__ method."""
        tag = Tag(name="Feature", slug="feature")
        db_session.add(tag)
        db_session.commit()

        assert "Feature" in repr(tag)
        assert "Tag" in repr(tag)


class TestCardTagsAssociation:
    """Tests for the Card <-> Tag many-to-many relationship."""

    def _setup_card_and_tag(
        self, db_session: Session
    ) -> tuple[Card, Tag]:
        """Helper to create a card and a tag."""
        board = Board(title="Board", slug="board")
        db_session.add(board)
        db_session.commit()
        col = Column(title="To Do", board_id=board.id, position=0)
        db_session.add(col)
        db_session.commit()
        card = Card(title="Task", slug="task", column_id=col.id, position=0)
        tag = Tag(name="Urgent", slug="urgent", color="#ef4444")
        db_session.add_all([card, tag])
        db_session.commit()
        return card, tag

    def test_add_tag_to_card(self, db_session: Session) -> None:
        """Test attaching a tag to a card."""
        card, tag = self._setup_card_and_tag(db_session)

        card.tags.append(tag)
        db_session.commit()
        db_session.refresh(card)

        assert len(card.tags) == 1
        assert card.tags[0].name == "Urgent"

    def test_tag_cards_relationship(self, db_session: Session) -> None:
        """Test the reverse relationship from tag to cards."""
        card, tag = self._setup_card_and_tag(db_session)

        card.tags.append(tag)
        db_session.commit()
        db_session.refresh(tag)

        assert len(tag.cards) == 1
        assert tag.cards[0].slug == "task"

    def test_multiple_tags_on_card(self, db_session: Session) -> None:
        """Test attaching multiple tags to a single card."""
        card, tag1 = self._setup_card_and_tag(db_session)
        tag2 = Tag(name="Feature", slug="feature", color="#3b82f6")
        tag3 = Tag(name="Bug", slug="bug", color="#ef4444")
        db_session.add_all([tag2, tag3])
        db_session.commit()

        card.tags.extend([tag1, tag2, tag3])
        db_session.commit()
        db_session.refresh(card)

        assert len(card.tags) == 3
        tag_names = {t.name for t in card.tags}
        assert tag_names == {"Urgent", "Feature", "Bug"}

    def test_tag_on_multiple_cards(self, db_session: Session) -> None:
        """Test that a single tag can be attached to multiple cards."""
        board = Board(title="Board", slug="board")
        db_session.add(board)
        db_session.commit()
        col = Column(title="Col", board_id=board.id, position=0)
        db_session.add(col)
        db_session.commit()

        card1 = Card(title="Task 1", slug="task-1", column_id=col.id, position=0)
        card2 = Card(title="Task 2", slug="task-2", column_id=col.id, position=1)
        tag = Tag(name="Shared", slug="shared")
        db_session.add_all([card1, card2, tag])
        db_session.commit()

        card1.tags.append(tag)
        card2.tags.append(tag)
        db_session.commit()
        db_session.refresh(tag)

        assert len(tag.cards) == 2

    def test_remove_tag_from_card(self, db_session: Session) -> None:
        """Test removing a tag from a card."""
        card, tag = self._setup_card_and_tag(db_session)
        card.tags.append(tag)
        db_session.commit()

        card.tags.remove(tag)
        db_session.commit()
        db_session.refresh(card)

        assert len(card.tags) == 0

    def test_delete_tag_removes_association(self, db_session: Session) -> None:
        """Test that deleting a tag removes it from cards but doesn't delete the card."""
        card, tag = self._setup_card_and_tag(db_session)
        card.tags.append(tag)
        db_session.commit()

        card_id = card.id
        db_session.delete(tag)
        db_session.commit()

        card_after = db_session.get(Card, card_id)
        assert card_after is not None
        assert len(card_after.tags) == 0

    def test_delete_card_removes_association(self, db_session: Session) -> None:
        """Test that deleting a card removes associations but doesn't delete the tag."""
        card, tag = self._setup_card_and_tag(db_session)
        card.tags.append(tag)
        db_session.commit()

        tag_id = tag.id
        db_session.delete(card)
        db_session.commit()

        tag_after = db_session.get(Tag, tag_id)
        assert tag_after is not None
        assert len(tag_after.cards) == 0


class TestColumnOrdering:
    """Tests for column ordering within a board."""

    def test_columns_ordered_by_position(self, db_session: Session) -> None:
        """Test that board.columns are returned ordered by position."""
        board = Board(title="Board", slug="board")
        db_session.add(board)
        db_session.commit()

        col3 = Column(title="Done", board_id=board.id, position=2)
        col1 = Column(title="To Do", board_id=board.id, position=0)
        col2 = Column(title="In Progress", board_id=board.id, position=1)
        db_session.add_all([col3, col1, col2])
        db_session.commit()
        db_session.refresh(board)

        titles = [c.title for c in board.columns]
        assert titles == ["To Do", "In Progress", "Done"]


class TestCardOrdering:
    """Tests for card ordering within a column."""

    def test_cards_ordered_by_position(self, db_session: Session) -> None:
        """Test that column.cards are returned ordered by position."""
        board = Board(title="Board", slug="board")
        db_session.add(board)
        db_session.commit()
        col = Column(title="Col", board_id=board.id, position=0)
        db_session.add(col)
        db_session.commit()

        card_c = Card(title="C", slug="c", column_id=col.id, position=2)
        card_a = Card(title="A", slug="a", column_id=col.id, position=0)
        card_b = Card(title="B", slug="b", column_id=col.id, position=1)
        db_session.add_all([card_c, card_a, card_b])
        db_session.commit()
        db_session.refresh(col)

        titles = [c.title for c in col.cards]
        assert titles == ["A", "B", "C"]
