"""Task Pydantic schemas."""

from datetime import datetime
from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    """Schema for creating a task."""

    title: str = Field(..., min_length=1, max_length=500)
    description: str = Field(default="", max_length=5000)
    category: str = Field(default="General", max_length=100)


class TaskUpdate(BaseModel):
    """Schema for updating a task."""

    title: str | None = Field(None, min_length=1, max_length=500)
    description: str | None = Field(None, max_length=5000)
    category: str | None = Field(None, max_length=100)


class TaskResponse(BaseModel):
    """Schema for task response."""

    id: int
    title: str
    description: str
    category: str
    completed: bool
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TaskListResponse(BaseModel):
    """Schema for task list response."""

    tasks: list[TaskResponse]
