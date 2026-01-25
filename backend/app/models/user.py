"""User SQLModel entity."""

from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, DateTime # Added this import
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.task import Task


class User(SQLModel, table=True):
    """User entity for authentication."""

    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(max_length=255, unique=True, index=True)
    hashed_password: str = Field(max_length=255)
    
    # Map 'created_at' in Python to 'createdAt' in the database
    created_at: datetime = Field(
        sa_column=Column("createdAt", DateTime, default=datetime.utcnow)
    )
    
    # Map 'updated_at' in Python to 'updatedAt' in the database
    updated_at: datetime = Field(
        sa_column=Column("updatedAt", DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    )

    # Relationship - use string reference to avoid circular import
    tasks: list["Task"] = Relationship(back_populates="user")