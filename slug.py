"""Slug generation utilities for SEO-friendly URLs.

Provides functions to convert titles into URL-safe slugs and handle
slug uniqueness by appending numeric suffixes on collision.
"""

from __future__ import annotations

import re
from typing import Callable


def generate_slug(title: str) -> str:
    """Convert a title string into a URL-safe slug.

    The transformation pipeline:
    1. Convert to lowercase
    2. Strip leading/trailing whitespace
    3. Replace spaces and underscores with hyphens
    4. Remove all characters that are not alphanumeric or hyphens
    5. Collapse consecutive hyphens into a single hyphen
    6. Strip leading and trailing hyphens

    Args:
        title: The input string to convert.

    Returns:
        A URL-safe slug string. Returns empty string if title produces
        no valid characters.

    Examples:
        >>> generate_slug("My Board Title")
        'my-board-title'
        >>> generate_slug("  Hello   World!!  ")
        'hello-world'
        >>> generate_slug("Über Cool Böard")
        'ber-cool-bard'
    """
    slug = title.lower().strip()
    slug = re.sub(r"[\s_]+", "-", slug)
    slug = re.sub(r"[^a-z0-9\-]", "", slug)
    slug = re.sub(r"-{2,}", "-", slug)
    slug = slug.strip("-")
    return slug


def generate_unique_slug(
    title: str,
    exists_fn: Callable[[str], bool],
) -> str:
    """Generate a slug that is unique according to the provided check function.

    First generates a base slug from the title. If that slug already exists
    (as determined by ``exists_fn``), appends an incrementing numeric suffix
    (``-2``, ``-3``, etc.) until a unique slug is found.

    Args:
        title: The input string to convert into a slug.
        exists_fn: A callable that takes a slug string and returns ``True``
            if that slug is already in use, ``False`` otherwise.

    Returns:
        A unique slug string.

    Raises:
        ValueError: If the title produces an empty base slug.

    Examples:
        >>> generate_unique_slug("My Board", lambda s: s == "my-board")
        'my-board-2'
        >>> generate_unique_slug("New Board", lambda s: False)
        'new-board'
    """
    base_slug = generate_slug(title)
    if not base_slug:
        raise ValueError(f"Cannot generate slug from title: {title!r}")

    if not exists_fn(base_slug):
        return base_slug

    counter = 2
    while True:
        candidate = f"{base_slug}-{counter}"
        if not exists_fn(candidate):
            return candidate
        counter += 1
