"""Tests for authentication endpoints."""

import pytest
from sqlmodel import select
from app.models.user import User
from app.auth.security import hash_password, create_access_token


def test_register_success(client):
    """Test successful user registration."""
    response = client.post(
        "/api/v1/auth/register",
        json={"email": "test@example.com", "password": "password123"}
    )
    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_register_duplicate_email(client, db_session):
    """Test registration with duplicate email fails."""
    # Create existing user
    user = User(
        email="existing@example.com",
        hashed_password=hash_password("password123")
    )
    db_session.add(user)
    db_session.commit()

    # Try to register with same email
    response = client.post(
        "/api/v1/auth/register",
        json={"email": "existing@example.com", "password": "password123"}
    )
    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]


def test_register_short_password(client):
    """Test registration with short password fails."""
    response = client.post(
        "/api/v1/auth/register",
        json={"email": "test@example.com", "password": "short"}
    )
    assert response.status_code == 400
    assert "at least 8 characters" in response.json()["detail"]


def test_login_success(client, db_session):
    """Test successful login."""
    # Create user
    user = User(
        email="login@example.com",
        hashed_password=hash_password("password123")
    )
    db_session.add(user)
    db_session.commit()

    # Login
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "login@example.com", "password": "password123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data


def test_login_wrong_password(client, db_session):
    """Test login with wrong password fails."""
    user = User(
        email="wrong@example.com",
        hashed_password=hash_password("correctpassword")
    )
    db_session.add(user)
    db_session.commit()

    response = client.post(
        "/api/v1/auth/login",
        json={"email": "wrong@example.com", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    assert "Invalid email or password" in response.json()["detail"]


def test_login_nonexistent_user(client):
    """Test login with nonexistent user fails."""
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "nonexistent@example.com", "password": "password123"}
    )
    assert response.status_code == 401
    assert "Invalid email or password" in response.json()["detail"]
