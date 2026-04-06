"""Category (taxonomy) CRUD routes.

Provides endpoints for managing hierarchical categories:
- GET    /api/categories       — list all categories as a tree structure
- GET    /api/categories/:slug — retrieve a single category by slug
- POST   /api/categories       — create a new category
- PUT    /api/categories/:id   — update an existing category
- DELETE /api/categories/:id   — delete a category
"""

from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db
from models import Category
from schemas import (
    CategoryCreate,
    CategoryResponse,
    CategoryTreeResponse,
    CategoryUpdate,
)
from utils.slug import generate_unique_slug

MAX_CATEGORY_DEPTH = 5

router = APIRouter(prefix="/api/categories", tags=["categories"])


def _build_tree(categories: List[Category]) -> List[CategoryTreeResponse]:
    """Build a nested tree structure from a flat list of Category objects.

    Constructs parent-child relationships by mapping each category's id
    to its tree response node, then nesting children under parents.

    Args:
        categories: Flat list of all Category ORM objects.

    Returns:
        A list of root-level CategoryTreeResponse nodes with nested children.
    """
    node_map: dict[int, CategoryTreeResponse] = {}
    roots: List[CategoryTreeResponse] = []

    # First pass: create all nodes
    for cat in categories:
        node = CategoryTreeResponse(
            id=cat.id,
            name=cat.name,
            slug=cat.slug,
            description=cat.description,
            parent_id=cat.parent_id,
            meta_title=cat.meta_title,
            meta_description=cat.meta_description,
            created_at=cat.created_at,
            updated_at=cat.updated_at,
            children=[],
        )
        node_map[cat.id] = node

    # Second pass: wire children to parents
    for cat in categories:
        node = node_map[cat.id]
        if cat.parent_id is not None and cat.parent_id in node_map:
            node_map[cat.parent_id].children.append(node)
        else:
            roots.append(node)

    return roots


def _get_depth(db: Session, parent_id: int | None) -> int:
    """Calculate the depth of a category by traversing up the parent chain.

    Args:
        db: Active SQLAlchemy session.
        parent_id: The parent_id to start traversal from.

    Returns:
        The depth (0 for root, 1 for direct child of root, etc.).
    """
    depth = 0
    current_id = parent_id
    visited: set[int] = set()
    while current_id is not None:
        if current_id in visited:
            break  # Circular reference protection
        visited.add(current_id)
        parent = db.execute(
            select(Category).where(Category.id == current_id)
        ).scalar_one_or_none()
        if parent is None:
            break
        depth += 1
        current_id = parent.parent_id
    return depth


def _would_create_cycle(db: Session, category_id: int, new_parent_id: int | None) -> bool:
    """Check if setting new_parent_id on category_id would create a cycle.

    Traverses up the parent chain from new_parent_id to see if it
    eventually reaches category_id.

    Args:
        db: Active SQLAlchemy session.
        category_id: The category being updated.
        new_parent_id: The proposed new parent_id.

    Returns:
        True if a cycle would be created, False otherwise.
    """
    if new_parent_id is None:
        return False
    current_id: int | None = new_parent_id
    visited: set[int] = set()
    while current_id is not None:
        if current_id == category_id:
            return True
        if current_id in visited:
            break
        visited.add(current_id)
        parent = db.execute(
            select(Category).where(Category.id == current_id)
        ).scalar_one_or_none()
        if parent is None:
            break
        current_id = parent.parent_id
    return False


@router.get(
    "",
    response_model=List[CategoryTreeResponse],
    summary="List all categories as a tree",
)
def list_categories(db: Session = Depends(get_db)) -> List[CategoryTreeResponse]:
    """Return all categories organized as a nested tree structure.

    Root categories (those with no parent) are top-level nodes.
    Each node includes its children recursively.
    """
    stmt = select(Category).order_by(Category.name)
    categories = list(db.execute(stmt).scalars().all())
    return _build_tree(categories)


@router.get(
    "/{slug}",
    response_model=CategoryTreeResponse,
    summary="Get a category by slug",
)
def get_category(
    slug: str,
    db: Session = Depends(get_db),
) -> CategoryTreeResponse:
    """Return a single category identified by its slug.

    The response includes the category's direct children.

    Raises:
        HTTPException: 404 if no category with the given slug exists.
    """
    stmt = select(Category).where(Category.slug == slug)
    category = db.execute(stmt).scalar_one_or_none()
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with slug '{slug}' not found.",
        )

    # Build children list (direct children only for single lookup)
    children_nodes: List[CategoryTreeResponse] = []
    for child in category.children:
        children_nodes.append(
            CategoryTreeResponse(
                id=child.id,
                name=child.name,
                slug=child.slug,
                description=child.description,
                parent_id=child.parent_id,
                meta_title=child.meta_title,
                meta_description=child.meta_description,
                created_at=child.created_at,
                updated_at=child.updated_at,
                children=[],
            )
        )

    return CategoryTreeResponse(
        id=category.id,
        name=category.name,
        slug=category.slug,
        description=category.description,
        parent_id=category.parent_id,
        meta_title=category.meta_title,
        meta_description=category.meta_description,
        created_at=category.created_at,
        updated_at=category.updated_at,
        children=children_nodes,
    )


@router.post(
    "",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new category",
)
def create_category(
    payload: CategoryCreate,
    db: Session = Depends(get_db),
) -> CategoryResponse:
    """Create a new category.

    Automatically generates a unique slug from the name.
    Validates that the parent exists (if specified) and that the
    maximum nesting depth is not exceeded.

    Raises:
        HTTPException: 404 if parent_id references a non-existent category.
        HTTPException: 400 if maximum nesting depth would be exceeded.
    """
    if payload.parent_id is not None:
        parent = db.execute(
            select(Category).where(Category.id == payload.parent_id)
        ).scalar_one_or_none()
        if parent is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Parent category with id {payload.parent_id} not found.",
            )
        depth = _get_depth(db, payload.parent_id) + 1
        if depth >= MAX_CATEGORY_DEPTH:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Maximum category nesting depth of {MAX_CATEGORY_DEPTH} exceeded.",
            )

    slug = generate_unique_slug(db, Category, payload.name)

    category = Category(
        name=payload.name,
        slug=slug,
        description=payload.description,
        parent_id=payload.parent_id,
        meta_title=payload.meta_title,
        meta_description=payload.meta_description,
    )
    db.add(category)
    db.commit()
    db.refresh(category)
    return CategoryResponse.model_validate(category)


@router.put(
    "/{category_id}",
    response_model=CategoryResponse,
    summary="Update an existing category",
)
def update_category(
    category_id: int,
    payload: CategoryUpdate,
    db: Session = Depends(get_db),
) -> CategoryResponse:
    """Update an existing category by ID.

    Only supplied fields are updated. If the name changes, a new
    unique slug is regenerated. Validates parent relationships to
    prevent circular references and depth violations.

    Raises:
        HTTPException: 404 if the category does not exist.
        HTTPException: 404 if new parent_id references a non-existent category.
        HTTPException: 400 if the update would create a circular reference.
        HTTPException: 400 if maximum nesting depth would be exceeded.
    """
    category = db.execute(
        select(Category).where(Category.id == category_id)
    ).scalar_one_or_none()
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with id {category_id} not found.",
        )

    update_data = payload.model_dump(exclude_unset=True)

    # Validate parent_id changes
    if "parent_id" in update_data:
        new_parent_id = update_data["parent_id"]
        if new_parent_id is not None:
            if new_parent_id == category_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="A category cannot be its own parent.",
                )
            parent = db.execute(
                select(Category).where(Category.id == new_parent_id)
            ).scalar_one_or_none()
            if parent is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Parent category with id {new_parent_id} not found.",
                )
            if _would_create_cycle(db, category_id, new_parent_id):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Setting this parent would create a circular reference.",
                )
            depth = _get_depth(db, new_parent_id) + 1
            if depth >= MAX_CATEGORY_DEPTH:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Maximum category nesting depth of {MAX_CATEGORY_DEPTH} exceeded.",
                )

    # Regenerate slug if name changed
    if "name" in update_data and update_data["name"] is not None:
        update_data["slug"] = generate_unique_slug(
            db, Category, update_data["name"], current_id=category_id,
        )

    for field, value in update_data.items():
        setattr(category, field, value)

    db.commit()
    db.refresh(category)
    return CategoryResponse.model_validate(category)


@router.delete(
    "/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a category",
)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
) -> None:
    """Delete a category by ID.

    Children categories are also deleted via cascade.
    Card associations are removed but cards themselves are preserved.

    Raises:
        HTTPException: 404 if the category does not exist.
    """
    category = db.execute(
        select(Category).where(Category.id == category_id)
    ).scalar_one_or_none()
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with id {category_id} not found.",
        )

    db.delete(category)
    db.commit()
