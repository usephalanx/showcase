"""Pydantic request and response schemas for the Task API.

These schemas handle validation, serialisation and OpenAPI documentation
for every endpoint.  They are deliberately separate from the SQLAlchemy
ORM models (:mod:`backend.models`) so that the API contract can evolve
independently of the database schema.
"""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class TaskCreate(BaseModel):
    """Request body for ``POST /tasks``."""

    title: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Short summary of the task",
    )
    description: str = Field(
        default="",
        max_length=1000,
        description="Optional longer description",
    )

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "title": "Buy groceries",
                    "description": "Milk, eggs, bread",
                }
            ]
        }
    )


class TaskUpdate(BaseModel):
    """Request body for ``PATCH /tasks/{id}``."""

    status: Literal["pending", "done"] = Field(
        ...,
        description="New status for the task",
    )

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {"status": "done"}
            ]
        }
    )


class TaskResponse(BaseModel):
    """Response body representing a single task."""

    id: int
    title: str
    description: str
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
