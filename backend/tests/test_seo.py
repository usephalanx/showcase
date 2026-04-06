"""Tests for the SEO meta tag endpoint."""

from __future__ import annotations

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from models import Board, Card, Category, Column
from utils.slug import generate_unique_slug


def _create_board(db: Session, title: str = "Test Board", **kwargs: object) -> Board:
    """Helper to create a Board in the test database."""
    slug = generate_unique_slug(db, Board, title)
    board = Board(title=title, slug=slug, **kwargs)  # type: ignore[arg-type]
    db.add(board)
    db.commit()
    db.refresh(board)
    return board


def _create_column(db: Session, board_id: int, title: str = "To Do") -> Column:
    """Helper to create a Column in the test database."""
    col = Column(title=title, board_id=board_id, position=0)
    db.add(col)
    db.commit()
    db.refresh(col)
    return col


def _create_card(
    db: Session,
    column_id: int,
    title: str = "Test Card",
    **kwargs: object,
) -> Card:
    """Helper to create a Card in the test database."""
    slug = generate_unique_slug(db, Card, title)
    card = Card(title=title, slug=slug, column_id=column_id, position=0, **kwargs)  # type: ignore[arg-type]
    db.add(card)
    db.commit()
    db.refresh(card)
    return card


def _create_category(
    db: Session,
    name: str = "Test Category",
    **kwargs: object,
) -> Category:
    """Helper to create a Category in the test database."""
    slug = generate_unique_slug(db, Category, name)
    category = Category(name=name, slug=slug, **kwargs)  # type: ignore[arg-type]
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


class TestSEOBoardMeta:
    """Tests for GET /api/seo/board/:slug."""

    def test_board_default_meta(self, client: TestClient, db_session: Session) -> None:
        """Board with no meta overrides should use generated title."""
        board = _create_board(db_session, title="My Board", description="Board desc")

        response = client.get(f"/api/seo/board/{board.slug}")
        assert response.status_code == 200
        data = response.json()
        assert "My Board" in data["title"]
        assert data["description"] == "Board desc"
        assert data["og_title"] == data["title"]
        assert data["og_description"] == data["description"]
        assert board.slug in data["canonical_url"]
        assert data["page_type"] == "board"

    def test_board_custom_meta(self, client: TestClient, db_session: Session) -> None:
        """Board with meta overrides should use custom values."""
        board = _create_board(
            db_session,
            title="My Board",
            meta_title="Custom Title",
            meta_description="Custom Description",
        )

        response = client.get(f"/api/seo/board/{board.slug}")
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Custom Title"
        assert data["description"] == "Custom Description"

    def test_board_not_found(self, client: TestClient) -> None:
        """Nonexistent board slug should return 404."""
        response = client.get("/api/seo/board/nonexistent")
        assert response.status_code == 404


class TestSEOCardMeta:
    """Tests for GET /api/seo/card/:slug."""

    def test_card_default_meta(self, client: TestClient, db_session: Session) -> None:
        """Card with no meta overrides should use generated title."""
        board = _create_board(db_session, title="Board")
        col = _create_column(db_session, board.id)
        card = _create_card(
            db_session, col.id, title="Task One", description="Do something",
        )

        response = client.get(f"/api/seo/card/{card.slug}")
        assert response.status_code == 200
        data = response.json()
        assert "Task One" in data["title"]
        assert data["description"] == "Do something"
        assert data["og_type"] == "article"
        assert data["page_type"] == "card"
        assert card.slug in data["canonical_url"]

    def test_card_custom_meta(self, client: TestClient, db_session: Session) -> None:
        """Card with meta overrides should use custom values."""
        board = _create_board(db_session, title="Board")
        col = _create_column(db_session, board.id)
        card = _create_card(
            db_session,
            col.id,
            title="Task",
            meta_title="SEO Task Title",
            meta_description="SEO description",
        )

        response = client.get(f"/api/seo/card/{card.slug}")
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "SEO Task Title"
        assert data["description"] == "SEO description"

    def test_card_not_found(self, client: TestClient) -> None:
        """Nonexistent card slug should return 404."""
        response = client.get("/api/seo/card/nonexistent")
        assert response.status_code == 404


class TestSEOCategoryMeta:
    """Tests for GET /api/seo/category/:slug."""

    def test_category_default_meta(self, client: TestClient, db_session: Session) -> None:
        """Category with no meta overrides should use generated title."""
        category = _create_category(
            db_session, name="Engineering", description="All engineering tasks",
        )

        response = client.get(f"/api/seo/category/{category.slug}")
        assert response.status_code == 200
        data = response.json()
        assert "Engineering" in data["title"]
        assert data["description"] == "All engineering tasks"
        assert data["page_type"] == "category"
        assert category.slug in data["canonical_url"]

    def test_category_custom_meta(self, client: TestClient, db_session: Session) -> None:
        """Category with meta overrides should use custom values."""
        category = _create_category(
            db_session,
            name="Design",
            meta_title="Design Hub",
            meta_description="All design resources",
        )

        response = client.get(f"/api/seo/category/{category.slug}")
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Design Hub"
        assert data["description"] == "All design resources"

    def test_category_not_found(self, client: TestClient) -> None:
        """Nonexistent category slug should return 404."""
        response = client.get("/api/seo/category/nonexistent")
        assert response.status_code == 404


class TestSEOUnsupportedPageType:
    """Tests for unsupported page types."""

    def test_unsupported_type(self, client: TestClient) -> None:
        """Unsupported page type should return 400."""
        response = client.get("/api/seo/invalid-type/some-slug")
        assert response.status_code == 400
        assert "Unsupported page type" in response.json()["detail"]


class TestSEODescriptionTruncation:
    """Tests for meta description truncation."""

    def test_long_description_truncated(self, client: TestClient, db_session: Session) -> None:
        """A very long description should be truncated with ellipsis."""
        long_desc = "A" * 300
        board = _create_board(db_session, title="Long Desc Board", description=long_desc)

        response = client.get(f"/api/seo/board/{board.slug}")
        assert response.status_code == 200
        data = response.json()
        assert len(data["description"]) <= 160
        assert data["description"].endswith("...")

    def test_short_description_not_truncated(
        self, client: TestClient, db_session: Session,
    ) -> None:
        """A short description should not be truncated."""
        board = _create_board(db_session, title="Short Board", description="Short")

        response = client.get(f"/api/seo/board/{board.slug}")
        assert response.status_code == 200
        assert response.json()["description"] == "Short"


class TestSEODefaultDescription:
    """Tests for default description fallback."""

    def test_no_description_uses_default(
        self, client: TestClient, db_session: Session,
    ) -> None:
        """A resource with no description should use the default."""
        board = _create_board(db_session, title="No Desc")

        response = client.get(f"/api/seo/board/{board.slug}")
        assert response.status_code == 200
        data = response.json()
        assert len(data["description"]) > 0
        assert data["description"] != ""
