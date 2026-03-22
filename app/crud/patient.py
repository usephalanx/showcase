"""CRUD operations for the Patient model."""

import math
from typing import Optional, Tuple, List

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.patient import Patient
from app.schemas.patient import PatientCreate, PatientUpdate


def create_patient(db: Session, data: PatientCreate) -> Patient:
    """Create a new patient record and return it."""
    patient = Patient(**data.model_dump())
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient


def get_patient(db: Session, patient_id: int) -> Optional[Patient]:
    """Return a single patient by ID or None."""
    return db.query(Patient).filter(Patient.id == patient_id).first()


def list_patients(
    db: Session,
    *,
    search: Optional[str] = None,
    gender: Optional[str] = None,
    city: Optional[str] = None,
    insurance_provider: Optional[str] = None,
    page: int = 1,
    page_size: int = 20,
) -> Tuple[List[Patient], int]:
    """Return a paginated and optionally filtered list of patients with total count."""
    query = db.query(Patient)

    # Full-text-like search across name, email, phone
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                Patient.first_name.ilike(search_term),
                Patient.last_name.ilike(search_term),
                Patient.email.ilike(search_term),
                Patient.phone.ilike(search_term),
            )
        )

    # Exact/partial filters
    if gender:
        query = query.filter(Patient.gender == gender)
    if city:
        query = query.filter(Patient.city.ilike(f"%{city}%"))
    if insurance_provider:
        query = query.filter(Patient.insurance_provider.ilike(f"%{insurance_provider}%"))

    total = query.count()
    offset = (page - 1) * page_size
    items = query.order_by(Patient.id).offset(offset).limit(page_size).all()
    return items, total


def update_patient(db: Session, patient_id: int, data: PatientUpdate) -> Optional[Patient]:
    """Update an existing patient record. Returns None if not found."""
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if patient is None:
        return None

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(patient, field, value)

    db.commit()
    db.refresh(patient)
    return patient


def delete_patient(db: Session, patient_id: int) -> bool:
    """Delete a patient by ID. Returns True if deleted, False if not found."""
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if patient is None:
        return False
    db.delete(patient)
    db.commit()
    return True
