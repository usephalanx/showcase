"""Tests for the Card CRUD API routes.

Covers all card endpoints including creation, retrieval by slug,
listing with filters, update, move, delete, and category associations.
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from models import Board, Card, Category, Column
from utils.slug import generate_unique_slug


# ---------------------------------------------------------------------------
# Helper fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def board(db_session: Session) -> Board:
    """Create a test board."""
    b = Board(title="Test Board", slug="test-board")
    db_session.add(b)
    db_session.commit()
    db_session.refresh(b)
    return b


@pytest.fixture()
def column(db_session: Session, board: Board) -> Column:
    """Create a test column within the test board."""
    c = Column(board_id=board.id, title="To Do", position=0)
    db_session.add(c)
    db_session.commit()
    db_session.refresh(c)
    return c


@pytest.fixture()
def column2(db_session: Session, board: Board) -> Column:
    """Create a second test column within the test board."""
    c = Column(board_id=board.id, title="In Progress", position=1)
    db_session.add(c)
    db_session.commit()
    db_session.refresh(c)
    return c


@pytest.fixture()
def category(db_session: Session) -> Category:
    """Create a test category."""
    cat = Category(name="Bug", slug="bug")
    db_session.add(cat)
    db_session.commit()
    db_session.refresh(cat)
    return cat


@pytest.fixture()
def category2(db_session: Session) -> Category:
    """Create a second test category."""
    cat = Category(name="Feature", slug="feature")
    db_session.add(cat)
    db_session.commit()
    db_session.refresh(cat)
    return cat


@pytest.fixture()
def card(db_session: Session, column: Column) -> Card:
    """Create a test card within the test column."""
    c = Card(
        column_id=column.id,
        title="Fix login bug",
        slug="fix-login-bug",
        description="Users cannot login with special chars.",
        position=0,
    )
    db_session.add(c)
    db_session.commit()
    db_session.refresh(c)
    return c


# ---------------------------------------------------------------------------
# POST /api/columns/{column_id}/cards
# ---------------------------------------------------------------------------


class TestCreateCard:
    """Tests for the card creation endpoint."""

    def test_create_card_success(self, client: TestClient, column: Column) -> None:
        """Creating a card returns 201 with correct data."""
        response = client.post(
            f"/api/columns/{column.id}/cards",
            json={
                "title": "Implement auth",
                "description": "Add JWT authentication.",
                "position": 0,
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Implement auth"
        assert data["slug"] == "implement-auth"
        assert data["column_id"] == column.id
        assert data["description"] == "Add JWT authentication."
        assert data["position"] == 0
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data
        assert data["categories"] == []

    def test_create_card_nonexistent_column(self, client: TestClient) -> None:
        """Creating a card in a non-existent column returns 404."""
        response = client.post(
            "/api/columns/9999/cards",
            json={"title": "Ghost card", "position": 0},
        )
        assert response.status_code == 404

    def test_create_card_empty_title(self, client: TestClient, column: Column) -> None:
        """Creating a card with empty title returns 422."""
        response = client.post(
            f"/api/columns/{column.id}/cards",
            json={"title": "", "position": 0},
        )
        assert response.status_code == 422

    def test_create_card_slug_collision(
        self, client: TestClient, column: Column, card: Card,
    ) -> None:
        """Creating a card with a duplicate title generates a unique slug."""
        response = client.post(
            f"/api/columns/{column.id}/cards",
            json={"title": "Fix login bug", "position": 1},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["slug"] != card.slug
        assert data["slug"].startswith("fix-login-bug")

    def test_create_card_with_meta_fields(
        self, client: TestClient, column: Column,
    ) -> None:
        """Creating a card with SEO meta fields stores them."""
        response = client.post(
            f"/api/columns/{column.id}/cards",
            json={
                "title": "SEO Card",
                "position": 0,
                "meta_title": "Custom SEO Title",
                "meta_description": "Custom SEO Description",
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["meta_title"] == "Custom SEO Title"
        assert data["meta_description"] == "Custom SEO Description"


# ---------------------------------------------------------------------------
# GET /api/cards
# ---------------------------------------------------------------------------


class TestListCards:
    """Tests for the card listing endpoint."""

    def test_list_cards_empty(self, client: TestClient) -> None:
        """Listing cards when none exist returns empty list."""
        response = client.get("/api/cards")
        assert response.status_code == 200
        assert response.json() == []

    def test_list_cards_returns_all(self, client: TestClient, card: Card) -> None:
        """Listing cards returns all existing cards."""
        response = client.get("/api/cards")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["id"] == card.id

    def test_list_cards_filter_by_column(
        self,
        client: TestClient,
        db_session: Session,
        column: Column,
        column2: Column,
    ) -> None:
        """Filtering by column_id returns only cards in that column."""
        c1 = Card(column_id=column.id, title="Card A", slug="card-a", position=0)
        c2 = Card(column_id=column2.id, title="Card B", slug="card-b", position=0)
        db_session.add_all([c1, c2])
        db_session.commit()

        response = client.get(f"/api/cards?column_id={column.id}")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["title"] == "Card A"

    def test_list_cards_filter_by_category(
        self,
        client: TestClient,
        db_session: Session,
        column: Column,
        category: Category,
    ) -> None:
        """Filtering by category slug returns only associated cards."""
        c1 = Card(column_id=column.id, title="Bug Card", slug="bug-card", position=0)
        c2 = Card(column_id=column.id, title="Other Card", slug="other-card", position=1)
        c1.categories.append(category)
        db_session.add_all([c1, c2])
        db_session.commit()

        response = client.get(f"/api/cards?category={category.slug}")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["title"] == "Bug Card"


# ---------------------------------------------------------------------------
# GET /api/cards/{slug}
# ---------------------------------------------------------------------------


class TestGetCardBySlug:
    """Tests for the get-card-by-slug endpoint."""

    def test_get_card_by_slug_success(self, client: TestClient, card: Card) -> None:
        """Getting a card by its slug returns 200 with correct data."""
        response = client.get(f"/api/cards/{card.slug}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == card.id
        assert data["slug"] == card.slug
        assert data["title"] == card.title

    def test_get_card_by_slug_not_found(self, client: TestClient) -> None:
        """Getting a card with a non-existent slug returns 404."""
        response = client.get("/api/cards/non-existent-slug")
        assert response.status_code == 404


# ---------------------------------------------------------------------------
# PUT /api/cards/{card_id}
# ---------------------------------------------------------------------------


class TestUpdateCard:
    """Tests for the card update endpoint."""

    def test_update_card_title(self, client: TestClient, card: Card) -> None:
        """Updating a card's title also regenerates the slug."""
        response = client.put(
            f"/api/cards/{card.id}",
            json={"title": "Fix logout bug"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Fix logout bug"
        assert data["slug"] == "fix-logout-bug"

    def test_update_card_description_only(
        self, client: TestClient, card: Card,
    ) -> None:
        """Updating only the description preserves other fields."""
        response = client.put(
            f"/api/cards/{card.id}",
            json={"description": "Updated description."},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["description"] == "Updated description."
        assert data["title"] == card.title
        assert data["slug"] == card.slug

    def test_update_card_not_found(self, client: TestClient) -> None:
        """Updating a non-existent card returns 404."""
        response = client.put(
            "/api/cards/9999",
            json={"title": "Does not exist"},
        )
        assert response.status_code == 404

    def test_update_card_meta_fields(self, client: TestClient, card: Card) -> None:
        """Updating SEO meta fields works correctly."""
        response = client.put(
            f"/api/cards/{card.id}",
            json={
                "meta_title": "New Meta Title",
                "meta_description": "New meta description.",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["meta_title"] == "New Meta Title"
        assert data["meta_description"] == "New meta description."


# ---------------------------------------------------------------------------
# PATCH /api/cards/{card_id}/move
# ---------------------------------------------------------------------------


class TestMoveCard:
    """Tests for the card move endpoint."""

    def test_move_card_to_different_column(
        self, client: TestClient, card: Card, column2: Column,
    ) -> None:
        """Moving a card to a different column updates column_id and position."""
        response = client.patch(
            f"/api/cards/{card.id}/move",
            json={"column_id": column2.id, "position": 3},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["column_id"] == column2.id
        assert data["position"] == 3

    def test_move_card_same_column(
        self, client: TestClient, card: Card, column: Column,
    ) -> None:
        """Moving a card within the same column updates only position."""
        response = client.patch(
            f"/api/cards/{card.id}/move",
            json={"column_id": column.id, "position": 5},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["column_id"] == column.id
        assert data["position"] == 5

    def test_move_card_not_found(self, client: TestClient, column: Column) -> None:
        """Moving a non-existent card returns 404."""
        response = client.patch(
            "/api/cards/9999/move",
            json={"column_id": column.id, "position": 0},
        )
        assert response.status_code == 404

    def test_move_card_to_nonexistent_column(
        self, client: TestClient, card: Card,
    ) -> None:
        """Moving a card to a non-existent column returns 404."""
        response = client.patch(
            f"/api/cards/{card.id}/move",
            json={"column_id": 9999, "position": 0},
        )
        assert response.status_code == 404


# ---------------------------------------------------------------------------
# DELETE /api/cards/{card_id}
# ---------------------------------------------------------------------------


class TestDeleteCard:
    """Tests for the card deletion endpoint."""

    def test_delete_card_success(self, client: TestClient, card: Card) -> None:
        """Deleting an existing card returns 204."""
        response = client.delete(f"/api/cards/{card.id}")
        assert response.status_code == 204

        # Verify card is gone
        response = client.get(f"/api/cards/{card.slug}")
        assert response.status_code == 404

    def test_delete_card_not_found(self, client: TestClient) -> None:
        """Deleting a non-existent card returns 404."""
        response = client.delete("/api/cards/9999")
        assert response.status_code == 404


# ---------------------------------------------------------------------------
# POST /api/cards/{card_id}/categories
# ---------------------------------------------------------------------------


class TestAddCategoryToCard:
    """Tests for the add-category-to-card endpoint."""

    def test_add_category_success(
        self, client: TestClient, card: Card, category: Category,
    ) -> None:
        """Adding a category to a card returns 200 with updated categories."""
        response = client.post(
            f"/api/cards/{card.id}/categories",
            json={"category_id": category.id},
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["categories"]) == 1
        assert data["categories"][0]["id"] == category.id
        assert data["categories"][0]["slug"] == category.slug

    def test_add_multiple_categories(
        self,
        client: TestClient,
        card: Card,
        category: Category,
        category2: Category,
    ) -> None:
        """Adding multiple categories to a card accumulates them."""
        client.post(
            f"/api/cards/{card.id}/categories",
            json={"category_id": category.id},
        )
        response = client.post(
            f"/api/cards/{card.id}/categories",
            json={"category_id": category2.id},
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["categories"]) == 2

    def test_add_duplicate_category(
        self, client: TestClient, card: Card, category: Category,
    ) -> None:
        """Adding a duplicate category returns 409 conflict."""
        client.post(
            f"/api/cards/{card.id}/categories",
            json={"category_id": category.id},
        )
        response = client.post(
            f"/api/cards/{card.id}/categories",
            json={"category_id": category.id},
        )
        assert response.status_code == 409

    def test_add_category_card_not_found(
        self, client: TestClient, category: Category,
    ) -> None:
        """Adding a category to a non-existent card returns 404."""
        response = client.post(
            "/api/cards/9999/categories",
            json={"category_id": category.id},
        )
        assert response.status_code == 404

    def test_add_category_not_found(
        self, client: TestClient, card: Card,
    ) -> None:
        """Adding a non-existent category returns 404."""
        response = client.post(
            f"/api/cards/{card.id}/categories",
            json={"category_id": 9999},
        )
        assert response.status_code == 404


# ---------------------------------------------------------------------------
# DELETE /api/cards/{card_id}/categories/{category_id}
# ---------------------------------------------------------------------------


class TestRemoveCategoryFromCard:
    """Tests for the remove-category-from-card endpoint."""

    def test_remove_category_success(
        self,
        client: TestClient,
        card: Card,
        category: Category,
    ) -> None:
        """Removing an associated category returns 200 with updated list."""
        # First add the category
        client.post(
            f"/api/cards/{card.id}/categories",
            json={"category_id": category.id},
        )
        # Then remove it
        response = client.delete(
            f"/api/cards/{card.id}/categories/{category.id}",
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["categories"]) == 0

    def test_remove_category_not_associated(
        self, client: TestClient, card: Card, category: Category,
    ) -> None:
        """Removing a non-associated category returns 404."""
        response = client.delete(
            f"/api/cards/{card.id}/categories/{category.id}",
        )
        assert response.status_code == 404

    def test_remove_category_card_not_found(
        self, client: TestClient, category: Category,
    ) -> None:
        """Removing a category from a non-existent card returns 404."""
        response = client.delete(
            f"/api/cards/9999/categories/{category.id}",
        )
        assert response.status_code == 404

    def test_remove_category_category_not_found(
        self, client: TestClient, card: Card,
    ) -> None:
        """Removing a non-existent category from a card returns 404."""
        response = client.delete(
            f"/api/cards/{card.id}/categories/9999",
        )
        assert response.status_code == 404


# ---------------------------------------------------------------------------
# Integration / edge-case tests
# ---------------------------------------------------------------------------


class TestCardIntegration:
    """Integration and edge-case tests for card operations."""

    def test_full_lifecycle(
        self,
        client: TestClient,
        column: Column,
        column2: Column,
        category: Category,
    ) -> None:
        """Test the full card lifecycle: create, read, update, move, delete."""
        # Create
        resp = client.post(
            f"/api/columns/{column.id}/cards",
            json={"title": "Lifecycle Card", "position": 0},
        )
        assert resp.status_code == 201
        card_data = resp.json()
        card_id = card_data["id"]
        card_slug = card_data["slug"]

        # Read by slug
        resp = client.get(f"/api/cards/{card_slug}")
        assert resp.status_code == 200
        assert resp.json()["id"] == card_id

        # List
        resp = client.get("/api/cards")
        assert resp.status_code == 200
        assert any(c["id"] == card_id for c in resp.json())

        # Update
        resp = client.put(
            f"/api/cards/{card_id}",
            json={"title": "Updated Lifecycle Card"},
        )
        assert resp.status_code == 200
        assert resp.json()["title"] == "Updated Lifecycle Card"

        # Add category
        resp = client.post(
            f"/api/cards/{card_id}/categories",
            json={"category_id": category.id},
        )
        assert resp.status_code == 200
        assert len(resp.json()["categories"]) == 1

        # Filter by category
        resp = client.get(f"/api/cards?category={category.slug}")
        assert resp.status_code == 200
        assert len(resp.json()) == 1

        # Move
        resp = client.patch(
            f"/api/cards/{card_id}/move",
            json={"column_id": column2.id, "position": 0},
        )
        assert resp.status_code == 200
        assert resp.json()["column_id"] == column2.id

        # Remove category
        resp = client.delete(
            f"/api/cards/{card_id}/categories/{category.id}",
        )
        assert resp.status_code == 200
        assert len(resp.json()["categories"]) == 0

        # Delete
        resp = client.delete(f"/api/cards/{card_id}")
        assert resp.status_code == 204

        # Verify gone
        resp = client.get(f"/api/cards/{card_slug}")
        assert resp.status_code == 404

    def test_card_ordered_by_position(
        self, client: TestClient, column: Column,
    ) -> None:
        """Cards are returned ordered by position."""
        client.post(
            f"/api/columns/{column.id}/cards",
            json={"title": "Third", "position": 2},
        )
        client.post(
            f"/api/columns/{column.id}/cards",
            json={"title": "First", "position": 0},
        )
        client.post(
            f"/api/columns/{column.id}/cards",
            json={"title": "Second", "position": 1},
        )

        resp = client.get("/api/cards")
        assert resp.status_code == 200
        data = resp.json()
        positions = [c["position"] for c in data]
        assert positions == sorted(positions)
