"""Token response schemas."""

from pydantic import BaseModel


class Token(BaseModel):
    """Token response schema."""

    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """Token payload for JWT."""

    sub: int  # User ID
    email: str | None = None
    exp: int | None = None
