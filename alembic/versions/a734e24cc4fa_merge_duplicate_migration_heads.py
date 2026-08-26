"""merge duplicate migration heads

Revision ID: a734e24cc4fa
Revises: 515a40d77908, f1a2b3c4d5e6
Create Date: 2026-08-22 01:50:00.292255

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a734e24cc4fa'
down_revision: Union[str, Sequence[str], None] = ('515a40d77908', 'f1a2b3c4d5e6')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
