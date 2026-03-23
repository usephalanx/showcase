"""Tests for board CRUD endpoints."""

from __future__ import annotations

from typing import Any, Dict

from fastapi.testclient import TestClient


def _register_user(
    client: TestClient,
    email: str = "test@example.com",
    password: str = "testpass123",
) -> Dict[str, Any]:
    """Register a user and return the response JSON with access token."""
    resp = client.post("/auth/register", json={"email": email, "password": password})
    assert resp.status_code == 201
    return resp.json()


def _auth_header(token: str) -> Dict[str, str]:
    """Build an Authorization header dict."""
    return {"Authorization": f"Bearer {token}"}


def test_create_board_with_default_columns(client: TestClient) -> None:
    """POST /boards should create a board with 3 default columns."""
    auth = _register_user(client)
    headers = _auth_header(auth["access_token"])

    resp = client.post("/boards", json={"title": "My Board"}, headers=headers)
    assert resp.status_code == 201
    data = resp.json()
    assert data["title"] == "My Board"
    assert len(data["columns"]) == 3
    assert data["columns"][0]["title"] == "To Do"
    assert data["columns"][1]["title"] == "In Progress"
    assert data["columns"][2]["title"] == "Done"


def test_list_boards(client: TestClient) -> None:
    """GET /boards should return only the authenticated user's boards."""
    auth = _register_user(client)
    headers = _auth_header(auth["access_token"])

    # Create two boards
    client.post("/boards", json={"title": "Board 1"}, headers=headers)
    client.post("/boards", json={"title": "Board 2"}, headers=headers)

    resp = client.get("/boards", headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 2


def test_list_boards_excludes_other_users(client: TestClient) -> None:
    """GET /boards should not return boards owned by other users."""
    auth1 = _register_user(client, email="user1@test.com")
    auth2 = _register_user(client, email="user2@test.com")
    headers1 = _auth_header(auth1["access_token"])
    headers2 = _auth_header(auth2["access_token"])

    client.post("/boards", json={"title": "User1 Board"}, headers=headers1)
    client.post("/boards", json={"title": "User2 Board"}, headers=headers2)

    resp = client.get("/boards", headers=headers1)
    data = resp.json()
    assert len(data) == 1
    assert data[0]["title"] == "User1 Board"


def test_get_board_detail(client: TestClient) -> None:
    """GET /boards/{id} should return board with columns and cards."""
    auth = _register_user(client)
    headers = _auth_header(auth["access_token"])

    create_resp = client.post("/boards", json={"title": "Detail Board"}, headers=headers)
    board_id = create_resp.json()["id"]

    resp = client.get(f"/boards/{board_id}", headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == board_id
    assert data["title"] == "Detail Board"
    assert len(data["columns"]) == 3


def test_get_board_not_found(client: TestClient) -> None:
    """GET /boards/{id} with invalid ID should return 404."""
    auth = _register_user(client)
    headers = _auth_header(auth["access_token"])

    resp = client.get("/boards/9999", headers=headers)
    assert resp.status_code == 404


def test_get_board_wrong_user(client: TestClient) -> None:
    """GET /boards/{id} should return 404 for a board owned by another user."""
    auth1 = _register_user(client, email="owner@test.com")
    auth2 = _register_user(client, email="other@test.com")
    headers1 = _auth_header(auth1["access_token"])
    headers2 = _auth_header(auth2["access_token"])

    create_resp = client.post("/boards", json={"title": "Private"}, headers=headers1)
    board_id = create_resp.json()["id"]

    resp = client.get(f"/boards/{board_id}", headers=headers2)
    assert resp.status_code == 404


def test_delete_board(client: TestClient) -> None:
    """DELETE /boards/{id} should delete board and cascade to columns."""
    auth = _register_user(client)
    headers = _auth_header(auth["access_token"])

    create_resp = client.post("/boards", json={"title": "To Delete"}, headers=headers)
    board_id = create_resp.json()["id"]

    resp = client.delete(f"/boards/{board_id}", headers=headers)
    assert resp.status_code == 200

    # Verify it's gone
    resp = client.get(f"/boards/{board_id}", headers=headers)
    assert resp.status_code == 404


def test_delete_board_wrong_user(client: TestClient) -> None:
    """DELETE /boards/{id} should return 404 for boards owned by another user."""
    auth1 = _register_user(client, email="owner@test.com")
    auth2 = _register_user(client, email="intruder@test.com")
    headers1 = _auth_header(auth1["access_token"])
    headers2 = _auth_header(auth2["access_token"])

    create_resp = client.post("/boards", json={"title": "Protected"}, headers=headers1)
    board_id = create_resp.json()["id"]

    resp = client.delete(f"/boards/{board_id}", headers=headers2)
    assert resp.status_code == 404


def test_create_column(client: TestClient) -> None:
    """POST /boards/{id}/columns should add a new column."""
    auth = _register_user(client)
    headers = _auth_header(auth["access_token"])

    create_resp = client.post("/boards", json={"title": "Col Board"}, headers=headers)
    board_id = create_resp.json()["id"]

    resp = client.post(
        f"/boards/{board_id}/columns",
        json={"title": "Review"},
        headers=headers,
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["title"] == "Review"
    assert data["board_id"] == board_id
    # Position should be auto-assigned after existing 3 defaults
    assert data["position"] == 3


def test_create_column_wrong_user(client: TestClient) -> None:
    """POST /boards/{id}/columns should return 404 for another user's board."""
    auth1 = _register_user(client, email="owner@test.com")
    auth2 = _register_user(client, email="hacker@test.com")
    headers1 = _auth_header(auth1["access_token"])
    headers2 = _auth_header(auth2["access_token"])

    create_resp = client.post("/boards", json={"title": "Owned"}, headers=headers1)
    board_id = create_resp.json()["id"]

    resp = client.post(
        f"/boards/{board_id}/columns",
        json={"title": "Hack"},
        headers=headers2,
    )
    assert resp.status_code == 404


def test_get_board_cards(client: TestClient) -> None:
    """GET /boards/{id}/cards should return columns with cards."""
    auth = _register_user(client)
    headers = _auth_header(auth["access_token"])

    create_resp = client.post("/boards", json={"title": "Cards Board"}, headers=headers)
    board = create_resp.json()
    board_id = board["id"]
    col_id = board["columns"][0]["id"]

    # Create a card in the first column
    client.post(
        f"/cards?column_id={col_id}",
        json={"title": "Test Card"},
        headers=headers,
    )

    resp = client.get(f"/boards/{board_id}/cards", headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 3  # 3 default columns
    # First column should have 1 card
    first_col = [c for c in data if c["id"] == col_id][0]
    assert len(first_col["cards"]) == 1


def test_boards_require_auth(client: TestClient) -> None:
    """Board endpoints should return 403 without auth token."""
    resp = client.get("/boards")
    assert resp.status_code == 403

    resp = client.post("/boards", json={"title": "test"})
    assert resp.status_code == 403
