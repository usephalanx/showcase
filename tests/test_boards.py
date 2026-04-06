"""Tests for the Board CRUD routes."""

from __future__ import annotations

from fastapi.testclient import TestClient


class TestListBoards:
    """GET /api/boards"""

    def test_empty_list(self, client: TestClient) -> None:
        """Returns an empty list when no boards exist."""
        resp = client.get("/api/boards")
        assert resp.status_code == 200
        assert resp.json() == []

    def test_returns_created_boards(self, client: TestClient) -> None:
        """Returns boards after creation."""
        client.post("/api/boards", json={"title": "Board A"})
        client.post("/api/boards", json={"title": "Board B"})
        resp = client.get("/api/boards")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 2


class TestGetBoardBySlug:
    """GET /api/boards/{slug}"""

    def test_found(self, client: TestClient) -> None:
        """Returns a board when the slug exists."""
        create_resp = client.post("/api/boards", json={"title": "My Board"})
        slug = create_resp.json()["slug"]
        resp = client.get(f"/api/boards/{slug}")
        assert resp.status_code == 200
        assert resp.json()["slug"] == slug
        assert resp.json()["title"] == "My Board"

    def test_not_found(self, client: TestClient) -> None:
        """Returns 404 for a non-existent slug."""
        resp = client.get("/api/boards/no-such-board")
        assert resp.status_code == 404


class TestCreateBoard:
    """POST /api/boards"""

    def test_create_minimal(self, client: TestClient) -> None:
        """Creates a board with only a title."""
        resp = client.post("/api/boards", json={"title": "New Board"})
        assert resp.status_code == 201
        data = resp.json()
        assert data["title"] == "New Board"
        assert data["slug"] == "new-board"
        assert "id" in data
        assert "created_at" in data

    def test_create_with_all_fields(self, client: TestClient) -> None:
        """Creates a board with all optional fields."""
        payload = {
            "title": "Full Board",
            "description": "A description",
            "meta_title": "SEO Title",
            "meta_description": "SEO Desc",
        }
        resp = client.post("/api/boards", json=payload)
        assert resp.status_code == 201
        data = resp.json()
        assert data["description"] == "A description"
        assert data["meta_title"] == "SEO Title"
        assert data["meta_description"] == "SEO Desc"

    def test_slug_collision_appends_suffix(self, client: TestClient) -> None:
        """Duplicate titles get unique slugs with numeric suffixes."""
        client.post("/api/boards", json={"title": "Duplicate"})
        resp2 = client.post("/api/boards", json={"title": "Duplicate"})
        assert resp2.status_code == 201
        assert resp2.json()["slug"] == "duplicate-1"

    def test_empty_title_rejected(self, client: TestClient) -> None:
        """An empty title is rejected with 422."""
        resp = client.post("/api/boards", json={"title": ""})
        assert resp.status_code == 422

    def test_columns_empty_on_create(self, client: TestClient) -> None:
        """A new board has an empty columns list."""
        resp = client.post("/api/boards", json={"title": "Empty"})
        assert resp.json()["columns"] == []


class TestUpdateBoard:
    """PUT /api/boards/{id}"""

    def test_update_title_regenerates_slug(self, client: TestClient) -> None:
        """Changing the title regenerates the slug."""
        create_resp = client.post("/api/boards", json={"title": "Old Title"})
        board_id = create_resp.json()["id"]
        resp = client.put(f"/api/boards/{board_id}", json={"title": "New Title"})
        assert resp.status_code == 200
        assert resp.json()["title"] == "New Title"
        assert resp.json()["slug"] == "new-title"

    def test_update_description_only(self, client: TestClient) -> None:
        """Updating non-title fields keeps the slug."""
        create_resp = client.post("/api/boards", json={"title": "Keep Slug"})
        board_id = create_resp.json()["id"]
        original_slug = create_resp.json()["slug"]
        resp = client.put(
            f"/api/boards/{board_id}",
            json={"description": "Updated desc"},
        )
        assert resp.status_code == 200
        assert resp.json()["slug"] == original_slug
        assert resp.json()["description"] == "Updated desc"

    def test_update_not_found(self, client: TestClient) -> None:
        """Returns 404 for a non-existent board."""
        resp = client.put("/api/boards/9999", json={"title": "X"})
        assert resp.status_code == 404

    def test_update_same_title_keeps_slug(self, client: TestClient) -> None:
        """Updating with the same title keeps the same slug (no collision with self)."""
        create_resp = client.post("/api/boards", json={"title": "Same"})
        board_id = create_resp.json()["id"]
        resp = client.put(f"/api/boards/{board_id}", json={"title": "Same"})
        assert resp.status_code == 200
        assert resp.json()["slug"] == "same"


class TestDeleteBoard:
    """DELETE /api/boards/{id}"""

    def test_delete_existing(self, client: TestClient) -> None:
        """Deletes a board and returns 204."""
        create_resp = client.post("/api/boards", json={"title": "To Delete"})
        board_id = create_resp.json()["id"]
        resp = client.delete(f"/api/boards/{board_id}")
        assert resp.status_code == 204

        # Verify it's gone
        list_resp = client.get("/api/boards")
        assert len(list_resp.json()) == 0

    def test_delete_not_found(self, client: TestClient) -> None:
        """Returns 404 for a non-existent board."""
        resp = client.delete("/api/boards/9999")
        assert resp.status_code == 404

    def test_delete_cascades_columns(self, client: TestClient) -> None:
        """Deleting a board removes its columns."""
        create_resp = client.post("/api/boards", json={"title": "Cascade Test"})
        board_id = create_resp.json()["id"]
        client.post(
            f"/api/boards/{board_id}/columns",
            json={"title": "Col 1", "board_id": board_id},
        )
        client.delete(f"/api/boards/{board_id}")
        # Attempting to list columns for deleted board should 404
        resp = client.get(f"/api/boards/{board_id}/columns")
        assert resp.status_code == 404
