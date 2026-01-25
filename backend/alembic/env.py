"""Alembic environment configuration."""

import os
from logging.config import fileConfig
from sqlalchemy import pool, create_engine
from sqlalchemy.engine import Connection
from sqlmodel import SQLModel
from alembic import context

# Add backend to path
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.config import get_settings
from app.models.user import User
from app.models.task import Task
from app.models.message import Message

settings = get_settings()

# this is the Alembic Config object
config = context.config
config.set_main_option("sqlalchemy.url", settings.database_url)

# Interpret the config file for Python logging
# if config.config_file_name is not None:
#     fileConfig(config.config_file_name)

# add your model's MetaData object here for 'autogenerate' support
target_metadata = SQLModel.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = create_engine(settings.database_url, echo=False)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
