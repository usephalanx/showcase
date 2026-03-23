"""Tests for Pydantic schemas."""

from __future__ import annotations

from datetime import date, datetime, timezone

import pytest
from pydantic import ValidationError

from app.schemas.project import ProjectCreate, ProjectResponse
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate


# ---- ProjectCreate ----

def test_project_create_valid() -> None:
    """ProjectCreate accepts valid data."""
    schema = ProjectCreate(name="Hello", description="World")
    assert schema.name == "Hello"
    assert schema.description == "World"


def test_project_create_default_description() -> None:
    """ProjectCreate defaults description to empty string."""
    schema = ProjectCreate(name="No desc")
    assert schema.description == ""


def test_project_create_empty_name_fails() -> None:
    """ProjectCreate rejects an empty name."""
    with pytest.raises(ValidationError):
        ProjectCreate(name="")


def test_project_create_missing_name_fails() -> None:
    """ProjectCreate rejects missing name."""
    with pytest.raises(ValidationError):
        ProjectCreate()  # type: ignore[call-arg]


# ---- ProjectResponse ----

def test_project_response_from_attributes() -> None:
    """ProjectResponse can be created from ORM-like objects."""

    class FakeProject:
        """Fake ORM model."""
        id = 1
        name = "Test"
        description = "Desc"
        created_at = datetime(2025, 1, 1, tzinfo=timezone.utc)

    schema = ProjectResponse.model_validate(FakeProject())
    assert schema.id == 1
    assert schema.name == "Test"


# ---- TaskCreate ----

def test_task_create_valid() -> None:
    """TaskCreate accepts valid data with defaults."""
    schema = TaskCreate(project_id=1, title="Do stuff")
    assert schema.status.value == "todo"
    assert schema.priority.value == "medium"
    assert schema.due_date is None


def test_task_create_all_fields() -> None:
    """TaskCreate accepts all explicit fields."""
    schema = TaskCreate(
        project_id=1,
        title="Deploy",
        status="done",
        priority="high",
        due_date="2025-12-31",
    )
    assert schema.status.value == "done"
    assert schema.priority.value == "high"
    assert schema.due_date == date(2025, 12, 31)


def test_task_create_invalid_status() -> None:
    """TaskCreate rejects an invalid status value."""
    with pytest.raises(ValidationError):
        TaskCreate(project_id=1, title="Bad", status="invalid")


def test_task_create_empty_title_fails() -> None:
    """TaskCreate rejects empty title."""
    with pytest.raises(ValidationError):
        TaskCreate(project_id=1, title="")


# ---- TaskUpdate ----

def test_task_update_partial() -> None:
    """TaskUpdate allows partial updates."""
    schema = TaskUpdate(status="done")
    dumped = schema.model_dump(exclude_unset=True)
    assert dumped == {"status": "done"}


def test_task_update_empty() -> None:
    """TaskUpdate with no fields set results in empty dict."""
    schema = TaskUpdate()
    dumped = schema.model_dump(exclude_unset=True)
    assert dumped == {}


# ---- TaskResponse ----

def test_task_response_from_attributes() -> None:
    """TaskResponse can be created from ORM-like objects."""

    class FakeTask:
        """Fake ORM model."""
        id = 1
        project_id = 1
        title = "Test"
        status = "todo"
        priority = "medium"
        due_date = None
        created_at = datetime(2025, 1, 1, tzinfo=timezone.utc)

    schema = TaskResponse.model_validate(FakeTask())
    assert schema.id == 1
    assert schema.status.value == "todo"
