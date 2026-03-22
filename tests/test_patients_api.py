"""Integration tests for the /api/patients endpoints."""

import pytest
from fastapi.testclient import TestClient

from tests.conftest import SAMPLE_PATIENT_DATA


# ── Helper ──────────────────────────────────────────────────────────────

def _create_patient_via_api(
    client: TestClient, headers: dict[str, str], **overrides: object
) -> dict:
    """Create a patient through the API and return the JSON response."""
    data = {**SAMPLE_PATIENT_DATA, **overrides}
    resp = client.post("/api/patients", json=data, headers=headers)
    assert resp.status_code == 201, resp.text
    return resp.json()


# ── Authentication / Authorization ──────────────────────────────────────


def test_list_patients_unauthenticated(client: TestClient) -> None:
    """Unauthenticated requests should receive 401."""
    resp = client.get("/api/patients")
    assert resp.status_code == 401


def test_patient_role_forbidden(
    client: TestClient, patient_headers: dict[str, str]
) -> None:
    """Users with 'patient' role should receive 403."""
    resp = client.get("/api/patients", headers=patient_headers)
    assert resp.status_code == 403


def test_admin_can_access(
    client: TestClient, admin_headers: dict[str, str]
) -> None:
    """Admin users should be able to list patients."""
    resp = client.get("/api/patients", headers=admin_headers)
    assert resp.status_code == 200


def test_dentist_can_access(
    client: TestClient, dentist_headers: dict[str, str]
) -> None:
    """Dentist users should be able to list patients."""
    resp = client.get("/api/patients", headers=dentist_headers)
    assert resp.status_code == 200


def test_receptionist_can_access(
    client: TestClient, receptionist_headers: dict[str, str]
) -> None:
    """Receptionist users should be able to list patients."""
    resp = client.get("/api/patients", headers=receptionist_headers)
    assert resp.status_code == 200


# ── POST /api/patients ──────────────────────────────────────────────────


def test_create_patient(
    client: TestClient, admin_headers: dict[str, str]
) -> None:
    """Creating a patient should return 201 with full patient data."""
    body = _create_patient_via_api(client, admin_headers)
    assert body["first_name"] == "John"
    assert body["last_name"] == "Doe"
    assert body["allergies"] == "Penicillin"
    assert "id" in body
    assert "created_at" in body


def test_create_patient_validation(
    client: TestClient, admin_headers: dict[str, str]
) -> None:
    """Missing required fields should return 422."""
    resp = client.post("/api/patients", json={}, headers=admin_headers)
    assert resp.status_code == 422


# ── GET /api/patients/:id ───────────────────────────────────────────────


def test_get_patient_by_id(
    client: TestClient, admin_headers: dict[str, str]
) -> None:
    """Should return the patient with matching ID."""
    created = _create_patient_via_api(client, admin_headers)
    resp = client.get(f"/api/patients/{created['id']}", headers=admin_headers)
    assert resp.status_code == 200
    assert resp.json()["id"] == created["id"]


def test_get_patient_not_found(
    client: TestClient, admin_headers: dict[str, str]
) -> None:
    """Should return 404 for non-existent patient."""
    resp = client.get("/api/patients/99999", headers=admin_headers)
    assert resp.status_code == 404


# ── GET /api/patients (list / search / pagination) ──────────────────────


def test_list_patients_empty(
    client: TestClient, admin_headers: dict[str, str]
) -> None:
    """Empty database should return zero items."""
    resp = client.get("/api/patients", headers=admin_headers)
    body = resp.json()
    assert body["total"] == 0
    assert body["items"] == []


def test_list_patients_pagination(
    client: TestClient, admin_headers: dict[str, str]
) -> None:
    """Should paginate results correctly."""
    for i in range(5):
        _create_patient_via_api(
            client,
            admin_headers,
            first_name=f"P{i}",
            email=f"p{i}@test.com",
        )

    resp = client.get("/api/patients?page=1&page_size=2", headers=admin_headers)
    body = resp.json()
    assert len(body["items"]) == 2
    assert body["total"] == 5
    assert body["page"] == 1
    assert body["page_size"] == 2
    assert body["total_pages"] == 3


def test_list_patients_search(
    client: TestClient, admin_headers: dict[str, str]
) -> None:
    """Search query should filter by name."""
    _create_patient_via_api(client, admin_headers, first_name="Alice", email="a@t.com")
    _create_patient_via_api(client, admin_headers, first_name="Bob", email="b@t.com")

    resp = client.get("/api/patients?search=Alice", headers=admin_headers)
    body = resp.json()
    assert body["total"] == 1
    assert body["items"][0]["first_name"] == "Alice"


def test_list_patients_filter_gender(
    client: TestClient, admin_headers: dict[str, str]
) -> None:
    """Gender filter should return matching patients."""
    _create_patient_via_api(
        client, admin_headers, first_name="F1", gender="female", email="f1@t.com"
    )
    _create_patient_via_api(
        client, admin_headers, first_name="M1", gender="male", email="m1@t.com"
    )

    resp = client.get("/api/patients?gender=female", headers=admin_headers)
    assert resp.json()["total"] == 1


# ── PUT /api/patients/:id ───────────────────────────────────────────────


def test_update_patient(
    client: TestClient, admin_headers: dict[str, str]
) -> None:
    """Should update only provided fields."""
    created = _create_patient_via_api(client, admin_headers)
    resp = client.put(
        f"/api/patients/{created['id']}",
        json={"first_name": "Jane", "allergies": "Latex"},
        headers=admin_headers,
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["first_name"] == "Jane"
    assert body["allergies"] == "Latex"
    assert body["last_name"] == "Doe"  # unchanged


def test_update_patient_not_found(
    client: TestClient, admin_headers: dict[str, str]
) -> None:
    """Should return 404 when updating non-existent patient."""
    resp = client.put(
        "/api/patients/99999",
        json={"first_name": "Nope"},
        headers=admin_headers,
    )
    assert resp.status_code == 404


# ── DELETE /api/patients/:id ────────────────────────────────────────────


def test_delete_patient(
    client: TestClient, admin_headers: dict[str, str]
) -> None:
    """Should delete an existing patient and return 204."""
    created = _create_patient_via_api(client, admin_headers)
    resp = client.delete(
        f"/api/patients/{created['id']}", headers=admin_headers
    )
    assert resp.status_code == 204

    # Confirm deletion
    resp2 = client.get(
        f"/api/patients/{created['id']}", headers=admin_headers
    )
    assert resp2.status_code == 404


def test_delete_patient_not_found(
    client: TestClient, admin_headers: dict[str, str]
) -> None:
    """Should return 404 when deleting non-existent patient."""
    resp = client.delete("/api/patients/99999", headers=admin_headers)
    assert resp.status_code == 404


# ── RBAC for write operations ───────────────────────────────────────────


def test_patient_role_cannot_create(
    client: TestClient, patient_headers: dict[str, str]
) -> None:
    """Patient role should not be able to create patients."""
    resp = client.post(
        "/api/patients", json=SAMPLE_PATIENT_DATA, headers=patient_headers
    )
    assert resp.status_code == 403


def test_patient_role_cannot_update(
    client: TestClient,
    admin_headers: dict[str, str],
    patient_headers: dict[str, str],
) -> None:
    """Patient role should not be able to update patients."""
    created = _create_patient_via_api(client, admin_headers)
    resp = client.put(
        f"/api/patients/{created['id']}",
        json={"first_name": "Hacked"},
        headers=patient_headers,
    )
    assert resp.status_code == 403


def test_patient_role_cannot_delete(
    client: TestClient,
    admin_headers: dict[str, str],
    patient_headers: dict[str, str],
) -> None:
    """Patient role should not be able to delete patients."""
    created = _create_patient_via_api(client, admin_headers)
    resp = client.delete(
        f"/api/patients/{created['id']}", headers=patient_headers
    )
    assert resp.status_code == 403
