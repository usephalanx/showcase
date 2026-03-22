"""Unit tests for the patient CRUD operations (database layer)."""

import pytest
from sqlalchemy.orm import Session

from app.crud.patient import (
    create_patient,
    delete_patient,
    get_patient,
    list_patients,
    update_patient,
)
from app.schemas.patient import PatientCreate, PatientUpdate
from tests.conftest import SAMPLE_PATIENT_DATA


def _make_patient(db: Session, **overrides: object) -> object:
    """Helper to create a patient with optional field overrides."""
    data = {**SAMPLE_PATIENT_DATA, **overrides}
    return create_patient(db, PatientCreate(**data))


def test_create_patient(db_session: Session) -> None:
    """Creating a patient should persist and return all fields."""
    patient = _make_patient(db_session)
    assert patient.id is not None
    assert patient.first_name == "John"
    assert patient.last_name == "Doe"
    assert patient.allergies == "Penicillin"
    assert patient.insurance_provider == "BlueCross"


def test_get_patient(db_session: Session) -> None:
    """Should retrieve a patient by ID."""
    created = _make_patient(db_session)
    fetched = get_patient(db_session, created.id)
    assert fetched is not None
    assert fetched.id == created.id


def test_get_patient_not_found(db_session: Session) -> None:
    """Should return None for a non-existent ID."""
    assert get_patient(db_session, 99999) is None


def test_list_patients_empty(db_session: Session) -> None:
    """Should return empty list when no patients exist."""
    items, total = list_patients(db_session)
    assert items == []
    assert total == 0


def test_list_patients_pagination(db_session: Session) -> None:
    """Should respect page and page_size parameters."""
    for i in range(5):
        _make_patient(db_session, first_name=f"Patient{i}", email=f"p{i}@test.com")

    items, total = list_patients(db_session, page=1, page_size=2)
    assert len(items) == 2
    assert total == 5

    items2, _ = list_patients(db_session, page=3, page_size=2)
    assert len(items2) == 1


def test_list_patients_search(db_session: Session) -> None:
    """Should filter patients by search query."""
    _make_patient(db_session, first_name="Alice", last_name="Smith", email="alice@test.com")
    _make_patient(db_session, first_name="Bob", last_name="Jones", email="bob@test.com")

    items, total = list_patients(db_session, search="Alice")
    assert total == 1
    assert items[0].first_name == "Alice"


def test_list_patients_filter_gender(db_session: Session) -> None:
    """Should filter by gender."""
    _make_patient(db_session, first_name="F1", gender="female", email="f1@test.com")
    _make_patient(db_session, first_name="M1", gender="male", email="m1@test.com")

    items, total = list_patients(db_session, gender="female")
    assert total == 1
    assert items[0].gender == "female"


def test_list_patients_filter_city(db_session: Session) -> None:
    """Should filter by city (case-insensitive partial)."""
    _make_patient(db_session, first_name="C1", city="Chicago", email="c1@test.com")
    _make_patient(db_session, first_name="N1", city="New York", email="n1@test.com")

    items, total = list_patients(db_session, city="chic")
    assert total == 1


def test_list_patients_filter_insurance(db_session: Session) -> None:
    """Should filter by insurance provider."""
    _make_patient(db_session, first_name="I1", insurance_provider="Aetna", email="i1@test.com")
    _make_patient(db_session, first_name="I2", insurance_provider="BlueCross", email="i2@test.com")

    items, total = list_patients(db_session, insurance_provider="Aetna")
    assert total == 1


def test_update_patient(db_session: Session) -> None:
    """Should update only the provided fields."""
    patient = _make_patient(db_session)
    updated = update_patient(
        db_session,
        patient.id,
        PatientUpdate(first_name="Jane", allergies="Latex"),
    )
    assert updated is not None
    assert updated.first_name == "Jane"
    assert updated.allergies == "Latex"
    # Unchanged field
    assert updated.last_name == "Doe"


def test_update_patient_not_found(db_session: Session) -> None:
    """Updating a non-existent patient should return None."""
    result = update_patient(db_session, 99999, PatientUpdate(first_name="Nope"))
    assert result is None


def test_delete_patient(db_session: Session) -> None:
    """Should delete an existing patient and return True."""
    patient = _make_patient(db_session)
    assert delete_patient(db_session, patient.id) is True
    assert get_patient(db_session, patient.id) is None


def test_delete_patient_not_found(db_session: Session) -> None:
    """Deleting a non-existent patient should return False."""
    assert delete_patient(db_session, 99999) is False
