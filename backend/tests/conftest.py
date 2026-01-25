"""Pytest configuration and fixtures."""

import os
import pytest
from fastapi.testclient import TestClient
from sqlmodel import create_engine, Session, SQLModel
from sqlmodel.pool import StaticPool

# Set test environment variables before any imports
os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["JWT_SECRET_KEY"] = "test-secret-key-for-testing-only-min-32-chars"
os.environ["JWT_ALGORITHM"] = "HS256"
os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"] = "30"

# Now import app modules after environment is set
from app.database import get_db
from app.main import app


# Create in-memory SQLite database for testing
test_engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)


@pytest.fixture(name="db_session")
def db_session_fixture():
    """Create a test database session."""
    SQLModel.metadata.create_all(test_engine)
    with Session(test_engine) as session:
        yield session
    SQLModel.metadata.drop_all(test_engine)


@pytest.fixture(name="client")
def client_fixture(db_session):
    """Create a test client with database session override."""

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
