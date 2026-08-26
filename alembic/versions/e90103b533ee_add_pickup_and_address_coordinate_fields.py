"""add pickup and address coordinate fields

Revision ID: e90103b533ee
Revises: a734e24cc4fa
Create Date: 2026-08-22 01:52:51.278733

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e90103b533ee'
down_revision: Union[str, Sequence[str], None] = 'a734e24cc4fa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('addressdata', sa.Column('longitude', sa.Float(), nullable=True))
    op.add_column('addressdata', sa.Column('latitude', sa.Float(), nullable=True))

    op.add_column('pickups', sa.Column('longitude', sa.Float(), nullable=True))
    op.add_column('pickups', sa.Column('latitude', sa.Float(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('pickups', 'latitude')
    op.drop_column('pickups', 'longitude')
    op.drop_column('addressdata', 'latitude')
    op.drop_column('addressdata', 'longitude')
