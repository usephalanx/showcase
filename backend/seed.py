"""Seed script that populates the database with sample data for demo purposes.

Usage:
    python seed.py          # Seed the default database
    python seed.py --drop   # Drop existing tables before seeding

The script creates sample boards, columns, cards, and categories with
properly generated slugs.
"""

from __future__ import annotations

import argparse
import sys
from typing import Dict, List

from slugify import slugify
from sqlalchemy.orm import Session

from database import Base, SessionLocal, engine, init_db
from models import Board, Card, Category, Column


# ---------------------------------------------------------------------------
# Slug helpers
# ---------------------------------------------------------------------------


def _unique_slug(db: Session, model: type, value: str) -> str:
    """Generate a unique slug for the given model and value.

    Appends a numeric suffix (-1, -2, …) when a collision is detected.

    Args:
        db: Active database session.
        model: The SQLAlchemy model class (must have a ``slug`` column).
        value: The human-readable string to slugify.

    Returns:
        A unique slug string.
    """
    base_slug = slugify(value, max_length=250)
    slug = base_slug
    counter = 1
    while db.query(model).filter(model.slug == slug).first() is not None:
        slug = f"{base_slug}-{counter}"
        counter += 1
    return slug


# ---------------------------------------------------------------------------
# Seed data definitions
# ---------------------------------------------------------------------------

CATEGORIES_DATA: List[Dict[str, object]] = [
    {
        "name": "Feature",
        "description": "New feature requests and enhancements.",
        "children": [
            {"name": "UI Feature", "description": "Frontend / user-interface features."},
            {"name": "API Feature", "description": "Backend / API-level features."},
        ],
    },
    {
        "name": "Bug",
        "description": "Bug reports and defect tracking.",
        "children": [
            {"name": "Critical Bug", "description": "Showstopper bugs that block releases."},
            {"name": "Minor Bug", "description": "Low-severity cosmetic or edge-case bugs."},
        ],
    },
    {
        "name": "Documentation",
        "description": "Documentation tasks and improvements.",
        "children": [],
    },
    {
        "name": "DevOps",
        "description": "Infrastructure, CI/CD, and deployment tasks.",
        "children": [],
    },
]

BOARDS_DATA = [
    {
        "title": "Product Development",
        "description": "Main product development board tracking features, bugs, and releases.",
        "meta_title": "Product Development Board | Kanban",
        "meta_description": "Track product development tasks across columns from backlog to done.",
        "columns": [
            {
                "title": "Backlog",
                "position": 0,
                "cards": [
                    {
                        "title": "User authentication flow",
                        "description": "Implement login, registration, and password reset screens with proper validation.",
                        "position": 0,
                        "category_names": ["UI Feature"],
                    },
                    {
                        "title": "API rate limiting",
                        "description": "Add rate limiting middleware to protect public API endpoints.",
                        "position": 1,
                        "category_names": ["API Feature", "DevOps"],
                    },
                    {
                        "title": "Write onboarding guide",
                        "description": "Create a step-by-step onboarding guide for new users.",
                        "position": 2,
                        "category_names": ["Documentation"],
                    },
                ],
            },
            {
                "title": "In Progress",
                "position": 1,
                "cards": [
                    {
                        "title": "Dashboard redesign",
                        "description": "Redesign the main dashboard with improved data visualization widgets.",
                        "position": 0,
                        "category_names": ["UI Feature"],
                    },
                    {
                        "title": "Fix pagination offset bug",
                        "description": "Pagination returns duplicate rows when offset equals total count.",
                        "position": 1,
                        "category_names": ["Critical Bug"],
                    },
                ],
            },
            {
                "title": "Review",
                "position": 2,
                "cards": [
                    {
                        "title": "Update API documentation",
                        "description": "Regenerate OpenAPI spec and update endpoint descriptions.",
                        "position": 0,
                        "category_names": ["Documentation", "API Feature"],
                    },
                ],
            },
            {
                "title": "Done",
                "position": 3,
                "cards": [
                    {
                        "title": "Setup CI pipeline",
                        "description": "Configure GitHub Actions for lint, test, and deploy stages.",
                        "position": 0,
                        "category_names": ["DevOps"],
                    },
                ],
            },
        ],
    },
    {
        "title": "Marketing Campaign",
        "description": "Q1 marketing campaign planning and execution tracking board.",
        "meta_title": "Marketing Campaign Board | Kanban",
        "meta_description": "Plan and track marketing campaigns from ideation to completion.",
        "columns": [
            {
                "title": "Ideas",
                "position": 0,
                "cards": [
                    {
                        "title": "Social media content calendar",
                        "description": "Plan a month of social media posts across all platforms.",
                        "position": 0,
                        "category_names": ["Feature"],
                    },
                    {
                        "title": "Email newsletter template",
                        "description": "Design a reusable HTML email template for weekly newsletters.",
                        "position": 1,
                        "category_names": ["UI Feature"],
                    },
                ],
            },
            {
                "title": "In Progress",
                "position": 1,
                "cards": [
                    {
                        "title": "Landing page A/B test",
                        "description": "Set up A/B variants for the product landing page hero section.",
                        "position": 0,
                        "category_names": ["UI Feature"],
                    },
                ],
            },
            {
                "title": "Completed",
                "position": 2,
                "cards": [
                    {
                        "title": "Brand style guide",
                        "description": "Finalize brand colours, typography, and logo usage guidelines.",
                        "position": 0,
                        "category_names": ["Documentation"],
                    },
                ],
            },
        ],
    },
    {
        "title": "Personal Tasks",
        "description": "A simple personal task tracker for day-to-day items.",
        "meta_title": None,
        "meta_description": None,
        "columns": [
            {
                "title": "To Do",
                "position": 0,
                "cards": [
                    {
                        "title": "Grocery shopping",
                        "description": "Buy vegetables, fruits, and pantry staples for the week.",
                        "position": 0,
                        "category_names": [],
                    },
                    {
                        "title": "Read SQLAlchemy docs",
                        "description": "Review the SQLAlchemy 2.0 migration guide and new-style queries.",
                        "position": 1,
                        "category_names": ["Documentation"],
                    },
                ],
            },
            {
                "title": "Doing",
                "position": 1,
                "cards": [
                    {
                        "title": "Fix leaky faucet",
                        "description": "Replace the washer in the kitchen faucet to stop the drip.",
                        "position": 0,
                        "category_names": ["Minor Bug"],
                    },
                ],
            },
            {
                "title": "Done",
                "position": 2,
                "cards": [],
            },
        ],
    },
]


# ---------------------------------------------------------------------------
# Seed functions
# ---------------------------------------------------------------------------


def seed_categories(db: Session) -> Dict[str, Category]:
    """Create sample categories (with children) and return a lookup dict.

    Args:
        db: Active database session.

    Returns:
        A dict mapping category name to Category ORM instance.
    """
    lookup: Dict[str, Category] = {}
    for cat_data in CATEGORIES_DATA:
        name: str = cat_data["name"]  # type: ignore[assignment]
        slug = _unique_slug(db, Category, name)
        parent = Category(
            name=name,
            slug=slug,
            description=cat_data.get("description"),
        )
        db.add(parent)
        db.flush()  # get the id for children FK
        lookup[name] = parent

        children: List[Dict[str, str]] = cat_data.get("children", [])  # type: ignore[assignment]
        for child_data in children:
            child_name: str = child_data["name"]
            child_slug = _unique_slug(db, Category, child_name)
            child = Category(
                name=child_name,
                slug=child_slug,
                description=child_data.get("description"),
                parent_id=parent.id,
            )
            db.add(child)
            db.flush()
            lookup[child_name] = child

    return lookup


def seed_boards(db: Session, category_lookup: Dict[str, Category]) -> List[Board]:
    """Create sample boards with columns and cards.

    Args:
        db: Active database session.
        category_lookup: Dict mapping category name to Category instance.

    Returns:
        List of created Board instances.
    """
    boards: List[Board] = []

    for board_data in BOARDS_DATA:
        board_slug = _unique_slug(db, Board, board_data["title"])
        board = Board(
            title=board_data["title"],
            slug=board_slug,
            description=board_data.get("description"),
            meta_title=board_data.get("meta_title"),
            meta_description=board_data.get("meta_description"),
        )
        db.add(board)
        db.flush()

        for col_data in board_data["columns"]:
            column = Column(
                board_id=board.id,
                title=col_data["title"],
                position=col_data["position"],
            )
            db.add(column)
            db.flush()

            for card_data in col_data.get("cards", []):
                card_slug = _unique_slug(db, Card, card_data["title"])
                card = Card(
                    column_id=column.id,
                    title=card_data["title"],
                    slug=card_slug,
                    description=card_data.get("description"),
                    position=card_data["position"],
                )
                db.add(card)
                db.flush()

                # Associate categories
                for cat_name in card_data.get("category_names", []):
                    category = category_lookup.get(cat_name)
                    if category is not None:
                        card.categories.append(category)

                db.flush()

        boards.append(board)

    return boards


def run_seed(drop: bool = False) -> None:
    """Execute the full seed process.

    Args:
        drop: If True, drop all tables before re-creating and seeding.
    """
    if drop:
        print("Dropping all tables…")
        Base.metadata.drop_all(bind=engine)

    print("Creating tables…")
    init_db()

    db = SessionLocal()
    try:
        # Check if data already exists
        existing_boards = db.query(Board).count()
        if existing_boards > 0:
            print(f"Database already contains {existing_boards} board(s). Skipping seed.")
            print("Use --drop flag to reset and re-seed.")
            return

        print("Seeding categories…")
        category_lookup = seed_categories(db)
        print(f"  Created {len(category_lookup)} categories.")

        print("Seeding boards, columns, and cards…")
        boards = seed_boards(db, category_lookup)

        total_columns = sum(len(b.columns) for b in boards)
        total_cards = sum(
            len(col.cards) for b in boards for col in b.columns
        )
        print(f"  Created {len(boards)} boards, {total_columns} columns, {total_cards} cards.")

        db.commit()
        print("Seed complete.")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def main() -> None:
    """Parse CLI arguments and run the seed script."""
    parser = argparse.ArgumentParser(
        description="Populate the Kanban database with sample data.",
    )
    parser.add_argument(
        "--drop",
        action="store_true",
        default=False,
        help="Drop all existing tables before seeding.",
    )
    args = parser.parse_args()
    run_seed(drop=args.drop)


if __name__ == "__main__":
    main()
