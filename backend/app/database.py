"""Database connection and session management."""

from sqlmodel import SQLModel, create_engine, Session
from app.config import get_settings

settings = get_settings()

# Create SQLModel engine
# We only use connect_args={"check_same_thread": False} for SQLite.
# PostgreSQL (Neon) does not support or need this option.
if settings.database_url.startswith("sqlite"):
    connect_args = {"check_same_thread": False}
else:
    connect_args = {}

engine = create_engine(
    settings.database_url,
    echo=False,  # Set to True for SQL debugging
    connect_args=connect_args
)


def get_db():
    """Dependency for getting a database session."""
    with Session(engine) as session:
        try:
            yield session
        finally:
            session.close()


def init_db():
    """Initialize database tables."""
    SQLModel.metadata.create_all(engine)