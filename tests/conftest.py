"""Shared test fixtures for the test suite."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

from app.database import Base, get_db
from app.main import app
from app.models.user import User, UserRole
from app.auth import hash_password, create_access_token


TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(autouse=True)
def setup_database() -> Generator[None, None, None]:
    """Create all tables before each test and drop them after."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def db_session() -> Generator[Session, None, None]:
    """Provide a transactional database session for tests."""
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture()
def client(db_session: Session) -> Generator[TestClient, None, None]:
    """Return a TestClient wired to the test database."""

    def _override_get_db() -> Generator[Session, None, None]:
        """Override get_db with the test session."""
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


def _create_user(db: Session, role: UserRole, username: str) -> User:
    """Helper to create a user with a given role."""
    user = User(
        username=username,
        email=f"{username}@test.com",
        hashed_password=hash_password("password123"),
        role=role,
        full_name=f"Test {username}",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def _get_auth_header(user: User) -> dict[str, str]:
    """Generate an Authorization header for the given user."""
    token = create_access_token(
        data={"sub": user.username, "role": user.role.value if isinstance(user.role, UserRole) else user.role, "user_id": user.id}
    )
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture()
def admin_user(db_session: Session) -> User:
    """Create and return an admin user."""
    return _create_user(db_session, UserRole.ADMIN, "admin")


@pytest.fixture()
def dentist_user(db_session: Session) -> User:
    """Create and return a dentist user."""
    return _create_user(db_session, UserRole.DENTIST, "dentist")


@pytest.fixture()
def receptionist_user(db_session: Session) -> User:
    """Create and return a receptionist user."""
    return _create_user(db_session, UserRole.RECEPTIONIST, "receptionist")


@pytest.fixture()
def patient_user(db_session: Session) -> User:
    """Create and return a patient user (should NOT have access)."""
    return _create_user(db_session, UserRole.PATIENT, "patientuser")


@pytest.fixture()
def admin_headers(admin_user: User) -> dict[str, str]:
    """Auth headers for admin user."""
    return _get_auth_header(admin_user)


@pytest.fixture()
def dentist_headers(dentist_user: User) -> dict[str, str]:
    """Auth headers for dentist user."""
    return _get_auth_header(dentist_user)


@pytest.fixture()
def receptionist_headers(receptionist_user: User) -> dict[str, str]:
    """Auth headers for receptionist user."""
    return _get_auth_header(receptionist_user)


@pytest.fixture()
def patient_headers(patient_user: User) -> dict[str, str]:
    """Auth headers for patient user."""
    return _get_auth_header(patient_user)


SAMPLE_PATIENT_DATA: dict = {
    "first_name": "John",
    "last_name": "Doe",
    "date_of_birth": "1990-05-15",
    "gender": "male",
    "email": "john.doe@example.com",
    "phone": "+1-555-0100",
    "address_line1": "123 Main St",
    "address_line2": "Apt 4",
    "city": "Springfield",
    "state": "IL",
    "zip_code": "62704",
    "country": "US",
    "medical_history": "No significant history",
    "allergies": "Penicillin",
    "current_medications": "None",
    "insurance_provider": "BlueCross",
    "insurance_policy_number": "BC123456",
    "insurance_group_number": "GRP789",
}
