"""Tests for card CRUD and move endpoints."""

from __future__ import annotations

from typing import Any, Dict, List

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


def _create_board_and_get_columns(
    client: TestClient,
    headers: Dict[str, str],
    title: str = "Test Board",
) -> Dict[str, Any]:
    """Create a board and return the full response including columns."""
    resp = client.post("/boards", json={"title": title}, headers=headers)
    assert resp.status_code == 201
    return resp.json()


def test_create_card(client: TestClient) -> None:
    """POST /cards should create a card in the specified column."""
    auth = _register_user(client)
    headers = _auth_header(auth["access_token"])
    board = _create_board_and_get_columns(client, headers)
    col_id = board["columns"][0]["id"]

    resp = client.post(
        f"/cards?column_id={col_id}",
        json={"title": "New Card", "description": "A description"},
        headers=headers,
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["title"] == "New Card"
    assert data["description"] == "A description"
    assert data["column_id"] == col_id
    assert data["position"] == 0


def test_create_card_auto_position(client: TestClient) -> None:
    """Cards should auto-assign incrementing positions."""
    auth = _register_user(client)
    headers = _auth_header(auth["access_token"])
    board = _create_board_and_get_columns(client, headers)
    col_id = board["columns"][0]["id"]

    resp1 = client.post(
        f"/cards?column_id={col_id}",
        json={"title": "Card 1"},
        headers=headers,
    )
    resp2 = client.post(
        f"/cards?column_id={col_id}",
        json={"title": "Card 2"},
        headers=headers,
    )
    assert resp1.json()["position"] == 0
    assert resp2.json()["position"] == 1


def test_create_card_invalid_column(client: TestClient) -> None:
    """POST /cards with an invalid column_id should return 404."""
    auth = _register_user(client)
    headers = _auth_header(auth["access_token"])

    resp = client.post(
        "/cards?column_id=99999",
        json={"title": "Orphan Card"},
        headers=headers,
    )
    assert resp.status_code == 404


def test_create_card_wrong_user(client: TestClient) -> None:
    """POST /cards should return 404 when column belongs to another user."""
    auth1 = _register_user(client, email="owner@test.com")
    auth2 = _register_user(client, email="hacker@test.com")
    headers1 = _auth_header(auth1["access_token"])
    headers2 = _auth_header(auth2["access_token"])

    board = _create_board_and_get_columns(client, headers1)
    col_id = board["columns"][0]["id"]

    resp = client.post(
        f"/cards?column_id={col_id}",
        json={"title": "Hacked Card"},
        headers=headers2,
    )
    assert resp.status_code == 404


def test_update_card(client: TestClient) -> None:
    """PATCH /cards/{id} should update title and/or description."""
    auth = _register_user(client)
    headers = _auth_header(auth["access_token"])
    board = _create_board_and_get_columns(client, headers)
    col_id = board["columns"][0]["id"]

    create_resp = client.post(
        f"/cards?column_id={col_id}",
        json={"title": "Original"},
        headers=headers,
    )
    card_id = create_resp.json()["id"]

    resp = client.patch(
        f"/cards/{card_id}",
        json={"title": "Updated", "description": "New desc"},
        headers=headers,
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["title"] == "Updated"
    assert data["description"] == "New desc"


def test_update_card_partial(client: TestClient) -> None:
    """PATCH /cards/{id} should allow partial updates."""
    auth = _register_user(client)
    headers = _auth_header(auth["access_token"])
    board = _create_board_and_get_columns(client, headers)
    col_id = board["columns"][0]["id"]

    create_resp = client.post(
        f"/cards?column_id={col_id}",
        json={"title": "Original", "description": "Keep me"},
        headers=headers,
    )
    card_id = create_resp.json()["id"]

    resp = client.patch(
        f"/cards/{card_id}",
        json={"title": "Changed"},
        headers=headers,
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["title"] == "Changed"
    assert data["description"] == "Keep me"


def test_update_card_not_found(client: TestClient) -> None:
    """PATCH /cards/{id} with invalid ID should return 404."""
    auth = _register_user(client)
    headers = _auth_header(auth["access_token"])

    resp = client.patch(
        "/cards/99999",
        json={"title": "Ghost"},
        headers=headers,
    )
    assert resp.status_code == 404


def test_update_card_wrong_user(client: TestClient) -> None:
    """PATCH /cards/{id} should return 404 for another user's card."""
    auth1 = _register_user(client, email="owner@test.com")
    auth2 = _register_user(client, email="intruder@test.com")
    headers1 = _auth_header(auth1["access_token"])
    headers2 = _auth_header(auth2["access_token"])

    board = _create_board_and_get_columns(client, headers1)
    col_id = board["columns"][0]["id"]

    create_resp = client.post(
        f"/cards?column_id={col_id}",
        json={"title": "Private Card"},
        headers=headers1,
    )
    card_id = create_resp.json()["id"]

    resp = client.patch(
        f"/cards/{card_id}",
        json={"title": "Hacked"},
        headers=headers2,
    )
    assert resp.status_code == 404


def test_delete_card(client: TestClient) -> None:
    """DELETE /cards/{id} should delete the card."""
    auth = _register_user(client)
    headers = _auth_header(auth["access_token"])
    board = _create_board_and_get_columns(client, headers)
    col_id = board["columns"][0]["id"]

    create_resp = client.post(
        f"/cards?column_id={col_id}",
        json={"title": "Doomed"},
        headers=headers,
    )
    card_id = create_resp.json()["id"]

    resp = client.delete(f"/cards/{card_id}", headers=headers)
    assert resp.status_code == 200

    # Verify card is gone by trying to update it
    resp = client.patch(
        f"/cards/{card_id}",
        json={"title": "Ghost"},
        headers=headers,
    )
    assert resp.status_code == 404


def test_delete_card_reorders_positions(client: TestClient) -> None:
    """DELETE /cards/{id} should reindex remaining cards' positions."""
    auth = _register_user(client)
    headers = _auth_header(auth["access_token"])
    board = _create_board_and_get_columns(client, headers)
    col_id = board["columns"][0]["id"]

    # Create 3 cards
    card_ids: List[int] = []
    for i in range(3):
        resp = client.post(
            f"/cards?column_id={col_id}",
            json={"title": f"Card {i}"},
            headers=headers,
        )
        card_ids.append(resp.json()["id"])

    # Delete the middle card (position 1)
    client.delete(f"/cards/{card_ids[1]}", headers=headers)

    # Check remaining cards have positions 0 and 1
    board_resp = client.get(f"/boards/{board['id']}/cards", headers=headers)
    cols = board_resp.json()
    target_col = [c for c in cols if c["id"] == col_id][0]
    positions = sorted([card["position"] for card in target_col["cards"]])
    assert positions == [0, 1]


def test_move_card_within_same_column(client: TestClient) -> None:
    """POST /cards/{id}/move should reorder within the same column."""
    auth = _register_user(client)
    headers = _auth_header(auth["access_token"])
    board = _create_board_and_get_columns(client, headers)
    col_id = board["columns"][0]["id"]

    # Create 3 cards
    card_ids: List[int] = []
    for i in range(3):
        resp = client.post(
            f"/cards?column_id={col_id}",
            json={"title": f"Card {i}"},
            headers=headers,
        )
        card_ids.append(resp.json()["id"])

    # Move Card 0 (position 0) to position 2
    resp = client.post(
        f"/cards/{card_ids[0]}/move",
        json={"column_id": col_id, "position": 2},
        headers=headers,
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["position"] == 2
    assert data["column_id"] == col_id

    # Verify all positions
    board_resp = client.get(f"/boards/{board['id']}/cards", headers=headers)
    cols = board_resp.json()
    target_col = [c for c in cols if c["id"] == col_id][0]
    card_positions = {card["id"]: card["position"] for card in target_col["cards"]}
    assert card_positions[card_ids[0]] == 2
    assert card_positions[card_ids[1]] == 0
    assert card_positions[card_ids[2]] == 1


def test_move_card_between_columns(client: TestClient) -> None:
    """POST /cards/{id}/move should move card to a different column."""
    auth = _register_user(client)
    headers = _auth_header(auth["access_token"])
    board = _create_board_and_get_columns(client, headers)
    col_1_id = board["columns"][0]["id"]
    col_2_id = board["columns"][1]["id"]

    # Create 2 cards in column 1
    card_ids: List[int] = []
    for i in range(2):
        resp = client.post(
            f"/cards?column_id={col_1_id}",
            json={"title": f"Card {i}"},
            headers=headers,
        )
        card_ids.append(resp.json()["id"])

    # Move card 0 to column 2, position 0
    resp = client.post(
        f"/cards/{card_ids[0]}/move",
        json={"column_id": col_2_id, "position": 0},
        headers=headers,
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["column_id"] == col_2_id
    assert data["position"] == 0

    # Verify source column: card 1 should be at position 0
    board_resp = client.get(f"/boards/{board['id']}/cards", headers=headers)
    cols = board_resp.json()
    source_col = [c for c in cols if c["id"] == col_1_id][0]
    target_col = [c for c in cols if c["id"] == col_2_id][0]

    assert len(source_col["cards"]) == 1
    assert source_col["cards"][0]["id"] == card_ids[1]
    assert source_col["cards"][0]["position"] == 0

    assert len(target_col["cards"]) == 1
    assert target_col["cards"][0]["id"] == card_ids[0]
    assert target_col["cards"][0]["position"] == 0


def test_move_card_between_columns_with_existing_cards(client: TestClient) -> None:
    """Moving a card into a column that already has cards should reindex correctly."""
    auth = _register_user(client)
    headers = _auth_header(auth["access_token"])
    board = _create_board_and_get_columns(client, headers)
    col_1_id = board["columns"][0]["id"]
    col_2_id = board["columns"][1]["id"]

    # Create card in column 1
    resp = client.post(
        f"/cards?column_id={col_1_id}",
        json={"title": "Mover"},
        headers=headers,
    )
    mover_id = resp.json()["id"]

    # Create 2 cards in column 2
    existing_ids: List[int] = []
    for i in range(2):
        resp = client.post(
            f"/cards?column_id={col_2_id}",
            json={"title": f"Existing {i}"},
            headers=headers,
        )
        existing_ids.append(resp.json()["id"])

    # Move mover into column 2 at position 1 (between existing cards)
    resp = client.post(
        f"/cards/{mover_id}/move",
        json={"column_id": col_2_id, "position": 1},
        headers=headers,
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["column_id"] == col_2_id
    assert data["position"] == 1

    # Verify target column ordering
    board_resp = client.get(f"/boards/{board['id']}/cards", headers=headers)
    cols = board_resp.json()
    target_col = [c for c in cols if c["id"] == col_2_id][0]
    cards_by_pos = sorted(target_col["cards"], key=lambda c: c["position"])
    assert len(cards_by_pos) == 3
    assert cards_by_pos[0]["id"] == existing_ids[0]
    assert cards_by_pos[0]["position"] == 0
    assert cards_by_pos[1]["id"] == mover_id
    assert cards_by_pos[1]["position"] == 1
    assert cards_by_pos[2]["id"] == existing_ids[1]
    assert cards_by_pos[2]["position"] == 2


def test_move_card_wrong_user(client: TestClient) -> None:
    """POST /cards/{id}/move should return 404 for another user's card."""
    auth1 = _register_user(client, email="owner@test.com")
    auth2 = _register_user(client, email="mover@test.com")
    headers1 = _auth_header(auth1["access_token"])
    headers2 = _auth_header(auth2["access_token"])

    board = _create_board_and_get_columns(client, headers1)
    col_id = board["columns"][0]["id"]

    create_resp = client.post(
        f"/cards?column_id={col_id}",
        json={"title": "Private Card"},
        headers=headers1,
    )
    card_id = create_resp.json()["id"]

    resp = client.post(
        f"/cards/{card_id}/move",
        json={"column_id": col_id, "position": 0},
        headers=headers2,
    )
    assert resp.status_code == 404


def test_move_card_to_invalid_column(client: TestClient) -> None:
    """POST /cards/{id}/move should return 404 for invalid target column."""
    auth = _register_user(client)
    headers = _auth_header(auth["access_token"])
    board = _create_board_and_get_columns(client, headers)
    col_id = board["columns"][0]["id"]

    create_resp = client.post(
        f"/cards?column_id={col_id}",
        json={"title": "Homeless Card"},
        headers=headers,
    )
    card_id = create_resp.json()["id"]

    resp = client.post(
        f"/cards/{card_id}/move",
        json={"column_id": 99999, "position": 0},
        headers=headers,
    )
    assert resp.status_code == 404


def test_cards_require_auth(client: TestClient) -> None:
    """Card endpoints should return 403 without auth token."""
    resp = client.post("/cards?column_id=1", json={"title": "test"})
    assert resp.status_code == 403

    resp = client.patch("/cards/1", json={"title": "test"})
    assert resp.status_code == 403

    resp = client.delete("/cards/1")
    assert resp.status_code == 403

    resp = client.post("/cards/1/move", json={"column_id": 1, "position": 0})
    assert resp.status_code == 403
