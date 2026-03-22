"""RESTful API router for patient management."""

import math
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.auth import require_patient_management_role
from app.database import get_db
from app.crud.patient import (
    create_patient,
    delete_patient,
    get_patient,
    list_patients,
    update_patient,
)
from app.models.user import User
from app.schemas.patient import (
    PaginatedPatientsResponse,
    PatientCreate,
    PatientResponse,
    PatientUpdate,
)

router = APIRouter(prefix="/api/patients", tags=["patients"])


@router.get("", response_model=PaginatedPatientsResponse)
def api_list_patients(
    search: Optional[str] = Query(None, description="Search by name, email or phone"),
    gender: Optional[str] = Query(None, description="Filter by gender"),
    city: Optional[str] = Query(None, description="Filter by city"),
    insurance_provider: Optional[str] = Query(None, description="Filter by insurance provider"),
    page: int = Query(1, ge=1, description="Page number (1-indexed)"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_patient_management_role),
) -> PaginatedPatientsResponse:
    """List patients with optional search, filter, and pagination."""
    items, total = list_patients(
        db,
        search=search,
        gender=gender,
        city=city,
        insurance_provider=insurance_provider,
        page=page,
        page_size=page_size,
    )
    total_pages = math.ceil(total / page_size) if total > 0 else 0
    return PaginatedPatientsResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )


@router.get("/{patient_id}", response_model=PatientResponse)
def api_get_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_patient_management_role),
) -> PatientResponse:
    """Retrieve a single patient by ID."""
    patient = get_patient(db, patient_id)
    if patient is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found",
        )
    return patient  # type: ignore[return-value]


@router.post("", response_model=PatientResponse, status_code=status.HTTP_201_CREATED)
def api_create_patient(
    data: PatientCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_patient_management_role),
) -> PatientResponse:
    """Create a new patient record."""
    patient = create_patient(db, data)
    return patient  # type: ignore[return-value]


@router.put("/{patient_id}", response_model=PatientResponse)
def api_update_patient(
    patient_id: int,
    data: PatientUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_patient_management_role),
) -> PatientResponse:
    """Update an existing patient record."""
    patient = update_patient(db, patient_id, data)
    if patient is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found",
        )
    return patient  # type: ignore[return-value]


@router.delete("/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
def api_delete_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_patient_management_role),
) -> None:
    """Delete a patient record by ID."""
    deleted = delete_patient(db, patient_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found",
        )
