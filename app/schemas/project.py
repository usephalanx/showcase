"""Pydantic schemas for the Project resource.

Defines request (create/update) and response models used by the API
routers for data validation and serialisation.
"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class ProjectCreate(BaseModel):
    """Schema for creating a new project."""

    name: str = Field(..., min_length=1, max_length=255, description="Project name")
    description: str = Field(
        default="", max_length=1024, description="Project description"
    )


class ProjectResponse(BaseModel):
    """Schema for returning a project in API responses."""

    id: int
    name: str
    description: str
    created_at: datetime

    model_config = {"from_attributes": True}
