"""Patient ORM model."""

from sqlalchemy import Column, Integer, String, Date, Text, DateTime, func
from app.database import Base
from datetime import date, datetime


class Patient(Base):
    """Represents a patient record with personal, contact, medical, and insurance info."""

    __tablename__ = "patients"

    # Primary key
    id: int = Column(Integer, primary_key=True, index=True)  # type: ignore[assignment]

    # Personal information
    first_name: str = Column(String(100), nullable=False)  # type: ignore[assignment]
    last_name: str = Column(String(100), nullable=False)  # type: ignore[assignment]
    date_of_birth: date = Column(Date, nullable=False)  # type: ignore[assignment]
    gender: str = Column(String(20), nullable=True)  # type: ignore[assignment]

    # Contact details
    email: str = Column(String(255), nullable=True, index=True)  # type: ignore[assignment]
    phone: str = Column(String(30), nullable=True)  # type: ignore[assignment]
    address_line1: str = Column(String(255), nullable=True)  # type: ignore[assignment]
    address_line2: str = Column(String(255), nullable=True)  # type: ignore[assignment]
    city: str = Column(String(100), nullable=True)  # type: ignore[assignment]
    state: str = Column(String(100), nullable=True)  # type: ignore[assignment]
    zip_code: str = Column(String(20), nullable=True)  # type: ignore[assignment]
    country: str = Column(String(100), nullable=True, default="US")  # type: ignore[assignment]

    # Medical history
    medical_history: str = Column(Text, nullable=True, default="")  # type: ignore[assignment]
    allergies: str = Column(Text, nullable=True, default="")  # type: ignore[assignment]
    current_medications: str = Column(Text, nullable=True, default="")  # type: ignore[assignment]

    # Insurance information
    insurance_provider: str = Column(String(255), nullable=True)  # type: ignore[assignment]
    insurance_policy_number: str = Column(String(100), nullable=True)  # type: ignore[assignment]
    insurance_group_number: str = Column(String(100), nullable=True)  # type: ignore[assignment]

    # Metadata
    created_at: datetime = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)  # type: ignore[assignment]
    updated_at: datetime = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)  # type: ignore[assignment]
