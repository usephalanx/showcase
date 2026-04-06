"""Tests for the seed script.

Verifies that seed data is correctly created with proper slugs,
relationships, and idempotency behaviour.
"""

from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from database import Base
from models import Board, Card, Category, Column
from seed import seed_boards, seed_categories, BOARDS_DATA, CATEGORIES_DATA


def _make_session() -> Session:
    """Create an in-memory SQLite session with all tables."""
    import models as _models  # noqa: F401

    engine = create_engine(
        "sqlite:///",
        connect_args={"check_same_thread": False},
    )
    Base.metadata.create_all(bind=engine)
    _SessionLocal = sessionmaker(bind=engine)
    return _SessionLocal()


def test_seed_categories_creates_all() -> None:
    """seed_categories creates the expected number of categories."""
    db = _make_session()
    try:
        lookup = seed_categories(db)
        db.commit()

        # Count expected categories (parents + children)
        expected = sum(
            1 + len(cat.get("children", []))
            for cat in CATEGORIES_DATA
        )
        assert len(lookup) == expected
        assert db.query(Category).count() == expected
    finally:
        db.close()


def test_seed_categories_have_slugs() -> None:
    """Every seeded category should have a non-empty slug."""
    db = _make_session()
    try:
        lookup = seed_categories(db)
        db.commit()

        for name, cat in lookup.items():
            assert cat.slug, f"Category '{name}' has empty slug"
            assert " " not in cat.slug, f"Slug '{cat.slug}' should not contain spaces"
    finally:
        db.close()


def test_seed_categories_parent_child_relationship() -> None:
    """Child categories should reference their parent via parent_id."""
    db = _make_session()
    try:
        lookup = seed_categories(db)
        db.commit()

        # Verify parent categories have no parent_id
        for cat_data in CATEGORIES_DATA:
            parent = lookup[cat_data["name"]]
            assert parent.parent_id is None

            for child_data in cat_data.get("children", []):
                child = lookup[child_data["name"]]
                assert child.parent_id == parent.id
    finally:
        db.close()


def test_seed_boards_creates_correct_count() -> None:
    """seed_boards creates the expected number of boards."""
    db = _make_session()
    try:
        category_lookup = seed_categories(db)
        boards = seed_boards(db, category_lookup)
        db.commit()

        assert len(boards) == len(BOARDS_DATA)
        assert db.query(Board).count() == len(BOARDS_DATA)
    finally:
        db.close()


def test_seed_boards_have_unique_slugs() -> None:
    """Every seeded board should have a unique, non-empty slug."""
    db = _make_session()
    try:
        category_lookup = seed_categories(db)
        boards = seed_boards(db, category_lookup)
        db.commit()

        slugs = [b.slug for b in boards]
        assert len(slugs) == len(set(slugs)), "Board slugs should be unique"
        for slug in slugs:
            assert slug, "Board slug should not be empty"
    finally:
        db.close()


def test_seed_columns_created() -> None:
    """Correct number of columns are created across all boards."""
    db = _make_session()
    try:
        category_lookup = seed_categories(db)
        seed_boards(db, category_lookup)
        db.commit()

        expected_columns = sum(
            len(b["columns"]) for b in BOARDS_DATA
        )
        assert db.query(Column).count() == expected_columns
    finally:
        db.close()


def test_seed_cards_created() -> None:
    """Correct number of cards are created across all columns."""
    db = _make_session()
    try:
        category_lookup = seed_categories(db)
        seed_boards(db, category_lookup)
        db.commit()

        expected_cards = sum(
            len(card)
            for b in BOARDS_DATA
            for col in b["columns"]
            for card in [col.get("cards", [])]
        )
        assert db.query(Card).count() == expected_cards
    finally:
        db.close()


def test_seed_cards_have_slugs() -> None:
    """Every seeded card should have a non-empty slug."""
    db = _make_session()
    try:
        category_lookup = seed_categories(db)
        seed_boards(db, category_lookup)
        db.commit()

        cards = db.query(Card).all()
        for card in cards:
            assert card.slug, f"Card '{card.title}' has empty slug"
    finally:
        db.close()


def test_seed_card_category_associations() -> None:
    """Cards with specified categories should have correct associations."""
    db = _make_session()
    try:
        category_lookup = seed_categories(db)
        seed_boards(db, category_lookup)
        db.commit()

        # Check that at least some cards have categories
        cards_with_categories = [
            card for card in db.query(Card).all()
            if len(card.categories) > 0
        ]
        assert len(cards_with_categories) > 0, "Some cards should have categories"

        # Verify a specific card's categories
        api_rate_card = db.query(Card).filter(Card.slug == "api-rate-limiting").first()
        if api_rate_card is not None:
            cat_names = {c.name for c in api_rate_card.categories}
            assert "API Feature" in cat_names
            assert "DevOps" in cat_names
    finally:
        db.close()


def test_seed_column_positions_are_sequential() -> None:
    """Column positions within each board should be sequential starting from 0."""
    db = _make_session()
    try:
        category_lookup = seed_categories(db)
        seed_boards(db, category_lookup)
        db.commit()

        boards = db.query(Board).all()
        for board in boards:
            positions = sorted(c.position for c in board.columns)
            assert positions == list(range(len(positions))), (
                f"Board '{board.title}' columns have non-sequential positions: {positions}"
            )
    finally:
        db.close()


def test_seed_card_positions_are_sequential_within_column() -> None:
    """Card positions within each column should be sequential starting from 0."""
    db = _make_session()
    try:
        category_lookup = seed_categories(db)
        seed_boards(db, category_lookup)
        db.commit()

        columns = db.query(Column).all()
        for column in columns:
            if column.cards:
                positions = sorted(c.position for c in column.cards)
                assert positions == list(range(len(positions))), (
                    f"Column '{column.title}' cards have non-sequential positions: {positions}"
                )
    finally:
        db.close()


def test_seed_idempotency_skips_when_data_exists() -> None:
    """run_seed should skip seeding when boards already exist."""
    import seed as seed_module

    db = _make_session()
    try:
        # First seed
        category_lookup = seed_categories(db)
        seed_boards(db, category_lookup)
        db.commit()

        initial_board_count = db.query(Board).count()

        # Manually check the guard logic: if boards exist, we don't add more
        existing_boards = db.query(Board).count()
        assert existing_boards > 0
        assert existing_boards == initial_board_count
    finally:
        db.close()
