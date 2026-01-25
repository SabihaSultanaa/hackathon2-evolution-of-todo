"""User Pydantic schemas."""

from datetime import datetime
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    """Schema for creating a new user."""

    email: EmailStr
    password: str  # Min 8 chars (validated at route level)


class UserLogin(BaseModel):
    """Schema for user login."""

    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """Schema for user response."""

    id: int
    email: str
    created_at: datetime

    class Config:
        from_attributes = True
