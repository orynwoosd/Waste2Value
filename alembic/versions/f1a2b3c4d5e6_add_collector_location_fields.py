"""add collector location fields

Revision ID: f1a2b3c4d5e6
Revises: c0f3d7a5201d
Create Date: 2026-08-21 00:00:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "f1a2b3c4d5e6"
down_revision: Union[str, Sequence[str], None] = "c0f3d7a5201d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("last_longitude", sa.Float(), nullable=True))
    op.add_column("users", sa.Column("last_latitude", sa.Float(), nullable=True))
    op.add_column("users", sa.Column("location_updated_at", sa.TIMESTAMP(timezone=True), nullable=True))
    op.add_column("users", sa.Column("is_available", sa.Boolean(), server_default="false", nullable=False))


def downgrade() -> None:
    op.drop_column("users", "is_available")
    op.drop_column("users", "location_updated_at")
    op.drop_column("users", "last_latitude")
    op.drop_column("users", "last_longitude")
