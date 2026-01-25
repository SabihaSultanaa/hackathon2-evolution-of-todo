"""Task SQLModel entity."""

from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import User


class Task(SQLModel, table=True):
    """Task entity representing a todo item."""

    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(max_length=500)
    description: str = Field(default="", max_length=5000)
    category: str = Field(default="General", max_length=100)
    completed: bool = Field(default=False)
    user_id: int = Field(foreign_key="user.id", ondelete="CASCADE")

    # Relationship - use string reference to avoid circular import
    user: "User" = Relationship(back_populates="tasks")

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
