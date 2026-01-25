"""Initial schema for users and tasks

Revision ID: 001
Revises:
Create Date: 2026-01-07

"""

from typing import Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create users table
    op.create_table(
        'user',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('hashed_password', sa.String(255), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_user_email', 'user', ['email'], unique=True)

    # Create tasks table
    op.create_table(
        'task',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(500), nullable=False),
        sa.Column('description', sa.String(5000), nullable=True),
        sa.Column('completed', sa.Boolean(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_task_user_id', 'task', ['user_id'])


def downgrade() -> None:
    op.drop_index('ix_task_user_id', table_name='task')
    op.drop_table('task')
    op.drop_index('ix_user_email', table_name='user')
    op.drop_table('user')
