"""Pydantic schemas for patient CRUD operations."""

from pydantic import BaseModel, EmailStr, Field
from datetime import date, datetime
from typing import Optional, List


class PatientBase(BaseModel):
    """Shared patient fields used across multiple schemas."""

    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    date_of_birth: date
    gender: Optional[str] = Field(None, max_length=20)

    # Contact details
    email: Optional[str] = Field(None, max_length=255)
    phone: Optional[str] = Field(None, max_length=30)
    address_line1: Optional[str] = Field(None, max_length=255)
    address_line2: Optional[str] = Field(None, max_length=255)
    city: Optional[str] = Field(None, max_length=100)
    state: Optional[str] = Field(None, max_length=100)
    zip_code: Optional[str] = Field(None, max_length=20)
    country: Optional[str] = Field("US", max_length=100)

    # Medical
    medical_history: Optional[str] = ""
    allergies: Optional[str] = ""
    current_medications: Optional[str] = ""

    # Insurance
    insurance_provider: Optional[str] = Field(None, max_length=255)
    insurance_policy_number: Optional[str] = Field(None, max_length=100)
    insurance_group_number: Optional[str] = Field(None, max_length=100)


class PatientCreate(PatientBase):
    """Schema for creating a new patient."""
    pass


class PatientUpdate(BaseModel):
    """Schema for updating a patient — all fields optional."""

    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    date_of_birth: Optional[date] = None
    gender: Optional[str] = Field(None, max_length=20)

    email: Optional[str] = Field(None, max_length=255)
    phone: Optional[str] = Field(None, max_length=30)
    address_line1: Optional[str] = Field(None, max_length=255)
    address_line2: Optional[str] = Field(None, max_length=255)
    city: Optional[str] = Field(None, max_length=100)
    state: Optional[str] = Field(None, max_length=100)
    zip_code: Optional[str] = Field(None, max_length=20)
    country: Optional[str] = Field(None, max_length=100)

    medical_history: Optional[str] = None
    allergies: Optional[str] = None
    current_medications: Optional[str] = None

    insurance_provider: Optional[str] = Field(None, max_length=255)
    insurance_policy_number: Optional[str] = Field(None, max_length=100)
    insurance_group_number: Optional[str] = Field(None, max_length=100)


class PatientResponse(PatientBase):
    """Schema for returning a patient record."""

    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class PaginatedPatientsResponse(BaseModel):
    """Paginated list response for patients."""

    items: List[PatientResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
