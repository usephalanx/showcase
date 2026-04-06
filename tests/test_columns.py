"""Tests for the Column CRUD routes."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
def board_id(client: TestClient) -> int:
    """Create a board and return its id for column tests."""
    resp = client.post("/api/boards", json={"title": "Test Board"})
    return resp.json()["id"]


class TestListColumns:
    """GET /api/boards/{board_id}/columns"""

    def test_empty_list(self, client: TestClient, board_id: int) -> None:
        """Returns an empty list for a board with no columns."""
        resp = client.get(f"/api/boards/{board_id}/columns")
        assert resp.status_code == 200
        assert resp.json() == []

    def test_board_not_found(self, client: TestClient) -> None:
        """Returns 404 for a non-existent board."""
        resp = client.get("/api/boards/9999/columns")
        assert resp.status_code == 404

    def test_ordered_by_position(self, client: TestClient, board_id: int) -> None:
        """Columns are returned in position order."""
        client.post(
            f"/api/boards/{board_id}/columns",
            json={"title": "Second", "board_id": board_id, "position": 1},
        )
        client.post(
            f"/api/boards/{board_id}/columns",
            json={"title": "First", "board_id": board_id, "position": 0},
        )
        resp = client.get(f"/api/boards/{board_id}/columns")
        data = resp.json()
        assert len(data) == 2
        assert data[0]["title"] == "First"
        assert data[1]["title"] == "Second"


class TestCreateColumn:
    """POST /api/boards/{board_id}/columns"""

    def test_create_column(self, client: TestClient, board_id: int) -> None:
        """Creates a column and returns 201."""
        resp = client.post(
            f"/api/boards/{board_id}/columns",
            json={"title": "To Do", "board_id": board_id, "position": 0},
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["title"] == "To Do"
        assert data["board_id"] == board_id
        assert "id" in data

    def test_create_board_not_found(self, client: TestClient) -> None:
        """Returns 404 if the board does not exist."""
        resp = client.post(
            "/api/boards/9999/columns",
            json={"title": "Col", "board_id": 9999},
        )
        assert resp.status_code == 404

    def test_auto_position(self, client: TestClient, board_id: int) -> None:
        """Auto-assigns position when not explicitly provided."""
        resp1 = client.post(
            f"/api/boards/{board_id}/columns",
            json={"title": "Col 1", "board_id": board_id},
        )
        resp2 = client.post(
            f"/api/boards/{board_id}/columns",
            json={"title": "Col 2", "board_id": board_id},
        )
        assert resp1.json()["position"] == 0
        assert resp2.json()["position"] == 1

    def test_cards_empty_on_create(self, client: TestClient, board_id: int) -> None:
        """A new column has an empty cards list."""
        resp = client.post(
            f"/api/boards/{board_id}/columns",
            json={"title": "Empty Col", "board_id": board_id},
        )
        assert resp.json()["cards"] == []


class TestUpdateColumn:
    """PUT /api/columns/{id}"""

    def test_update_title(self, client: TestClient, board_id: int) -> None:
        """Updates the column title."""
        create_resp = client.post(
            f"/api/boards/{board_id}/columns",
            json={"title": "Old", "board_id": board_id},
        )
        col_id = create_resp.json()["id"]
        resp = client.put(f"/api/columns/{col_id}", json={"title": "New"})
        assert resp.status_code == 200
        assert resp.json()["title"] == "New"

    def test_update_not_found(self, client: TestClient) -> None:
        """Returns 404 for a non-existent column."""
        resp = client.put("/api/columns/9999", json={"title": "X"})
        assert resp.status_code == 404


class TestReorderColumn:
    """PATCH /api/columns/{id}/reorder"""

    def test_reorder_forward(self, client: TestClient, board_id: int) -> None:
        """Moves a column from position 0 to position 2."""
        ids = []
        for title in ["A", "B", "C"]:
            resp = client.post(
                f"/api/boards/{board_id}/columns",
                json={"title": title, "board_id": board_id},
            )
            ids.append(resp.json()["id"])

        # Move A (pos 0) to pos 2
        resp = client.patch(f"/api/columns/{ids[0]}/reorder", json={"position": 2})
        assert resp.status_code == 200
        assert resp.json()["position"] == 2

        # Verify ordering
        list_resp = client.get(f"/api/boards/{board_id}/columns")
        positions = [(c["title"], c["position"]) for c in list_resp.json()]
        titles_ordered = [t for t, _ in sorted(positions, key=lambda x: x[1])]
        assert titles_ordered == ["B", "C", "A"]

    def test_reorder_backward(self, client: TestClient, board_id: int) -> None:
        """Moves a column from position 2 to position 0."""
        ids = []
        for title in ["A", "B", "C"]:
            resp = client.post(
                f"/api/boards/{board_id}/columns",
                json={"title": title, "board_id": board_id},
            )
            ids.append(resp.json()["id"])

        # Move C (pos 2) to pos 0
        resp = client.patch(f"/api/columns/{ids[2]}/reorder", json={"position": 0})
        assert resp.status_code == 200
        assert resp.json()["position"] == 0

        # Verify ordering
        list_resp = client.get(f"/api/boards/{board_id}/columns")
        positions = [(c["title"], c["position"]) for c in list_resp.json()]
        titles_ordered = [t for t, _ in sorted(positions, key=lambda x: x[1])]
        assert titles_ordered == ["C", "A", "B"]

    def test_reorder_not_found(self, client: TestClient) -> None:
        """Returns 404 for a non-existent column."""
        resp = client.patch("/api/columns/9999/reorder", json={"position": 0})
        assert resp.status_code == 404

    def test_reorder_same_position(self, client: TestClient, board_id: int) -> None:
        """No-op when reordering to the same position."""
        create_resp = client.post(
            f"/api/boards/{board_id}/columns",
            json={"title": "Only", "board_id": board_id},
        )
        col_id = create_resp.json()["id"]
        resp = client.patch(
            f"/api/columns/{col_id}/reorder",
            json={"position": create_resp.json()["position"]},
        )
        assert resp.status_code == 200


class TestDeleteColumn:
    """DELETE /api/columns/{id}"""

    def test_delete_existing(self, client: TestClient, board_id: int) -> None:
        """Deletes a column and returns 204."""
        create_resp = client.post(
            f"/api/boards/{board_id}/columns",
            json={"title": "Gone", "board_id": board_id},
        )
        col_id = create_resp.json()["id"]
        resp = client.delete(f"/api/columns/{col_id}")
        assert resp.status_code == 204

        # Verify it's gone
        list_resp = client.get(f"/api/boards/{board_id}/columns")
        assert len(list_resp.json()) == 0

    def test_delete_not_found(self, client: TestClient) -> None:
        """Returns 404 for a non-existent column."""
        resp = client.delete("/api/columns/9999")
        assert resp.status_code == 404

    def test_delete_reindexes_positions(self, client: TestClient, board_id: int) -> None:
        """Remaining columns are re-indexed after deletion."""
        ids = []
        for title in ["A", "B", "C"]:
            resp = client.post(
                f"/api/boards/{board_id}/columns",
                json={"title": title, "board_id": board_id},
            )
            ids.append(resp.json()["id"])

        # Delete B (position 1)
        client.delete(f"/api/columns/{ids[1]}")

        list_resp = client.get(f"/api/boards/{board_id}/columns")
        data = list_resp.json()
        assert len(data) == 2
        assert data[0]["title"] == "A"
        assert data[0]["position"] == 0
        assert data[1]["title"] == "C"
        assert data[1]["position"] == 1
