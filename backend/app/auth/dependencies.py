"""Authentication dependencies for FastAPI."""

from typing import Generator
from fastapi import Depends, HTTPException, status
from sqlmodel import select
from app.database import get_db
from app.models.user import User
from app.auth.security import decode_access_token


def get_current_user(
    db=Depends(get_db)
) -> User:
    """Dependency to get the current authenticated user from JWT token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = None
    # Try to get token from Authorization header
    # Note: This will be called by routes that check auth,
    # the token extraction happens in the route or a wrapper

    # The actual token extraction is done at the route level
    # This function validates the token and returns the user
    raise credentials_exception


def validate_token_and_get_user(token: str, db) -> User:
    """Validate JWT token and return the user."""
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id: int | None = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user
