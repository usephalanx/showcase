"""Slug generation utilities with collision handling.

Uses python-slugify to create URL-friendly slugs from arbitrary text
and handles uniqueness by appending numeric suffixes when collisions
are detected.
"""

from __future__ import annotations

from typing import Optional, Type

from slugify import slugify
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import Base


def generate_unique_slug(
    db: Session,
    model: Type[Base],  # type: ignore[type-arg]
    value: str,
    slug_field: str = "slug",
    max_length: int = 280,
    current_id: Optional[int] = None,
) -> str:
    """Generate a unique slug for a given model.

    Creates a slug from *value* using python-slugify and checks the
    database for existing records.  If a collision is found, a numeric
    suffix (-1, -2, …) is appended until a unique value is produced.

    Args:
        db: Active SQLAlchemy session.
        model: The ORM model class to check against.
        value: The human-readable text to slugify.
        slug_field: Name of the slug column on the model.
        max_length: Maximum allowed length for the slug.
        current_id: If updating an existing record, its ID is excluded
                    from the collision check.

    Returns:
        A unique slug string.

    Raises:
        ValueError: If *value* produces an empty slug.
    """
    base_slug = slugify(value, max_length=max_length)
    if not base_slug:
        raise ValueError(f"Cannot generate slug from value: {value!r}")

    candidate = base_slug
    counter = 1
    column = getattr(model, slug_field)
    pk_column = getattr(model, "id", None)

    while True:
        query = select(model).where(column == candidate)
        if current_id is not None and pk_column is not None:
            query = query.where(pk_column != current_id)

        existing = db.execute(query).scalar_one_or_none()
        if existing is None:
            return candidate

        candidate = f"{base_slug}-{counter}"
        if len(candidate) > max_length:
            # Trim the base to make room for the suffix
            suffix = f"-{counter}"
            candidate = base_slug[: max_length - len(suffix)] + suffix
        counter += 1
