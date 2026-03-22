"""User ORM model."""

from sqlalchemy import Column, Integer, String, Enum as SAEnum
from app.database import Base
import enum


class UserRole(str, enum.Enum):
    """Enumeration of application user roles."""

    ADMIN = "admin"
    DENTIST = "dentist"
    RECEPTIONIST = "receptionist"
    PATIENT = "patient"


class User(Base):
    """Represents an application user with role-based access."""

    __tablename__ = "users"

    id: int = Column(Integer, primary_key=True, index=True)  # type: ignore[assignment]
    username: str = Column(String(100), unique=True, nullable=False, index=True)  # type: ignore[assignment]
    email: str = Column(String(255), unique=True, nullable=False)  # type: ignore[assignment]
    hashed_password: str = Column(String(255), nullable=False)  # type: ignore[assignment]
    role: str = Column(SAEnum(UserRole), nullable=False, default=UserRole.PATIENT)  # type: ignore[assignment]
    full_name: str = Column(String(255), nullable=False, default="")  # type: ignore[assignment]
