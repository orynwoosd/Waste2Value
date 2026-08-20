"""add profiles table

Revision ID: c0f3d7a5201d
Revises: add_role_requests_and_audit_logs
Create Date: 2026-08-14 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'c0f3d7a5201d'
down_revision = 'add_role_requests_and_audit_logs'
branch_labels = None
depends_on = None


def upgrade() -> None:
    profile_type = postgresql.ENUM(
        'individual', 'business', 'organization', 'community',
        name='profiletype',
    )
    profile_type.create(op.get_bind(), checkfirst=True)

    op.create_table(
        'profiles',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False, unique=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column(
            'profile_type',
            postgresql.ENUM('individual', 'business', 'organization', 'community', name='profiletype', create_type=False),
            nullable=False,
            server_default='individual',
        ),
        sa.Column('display_name', sa.String(length=200), nullable=True),
        sa.Column('profession', sa.String(length=100), nullable=True),
        sa.Column('company_name', sa.String(length=150), nullable=True),
        sa.Column('website', sa.String(length=255), nullable=True),
        sa.Column('logo', sa.String(length=200), nullable=True),
        sa.Column('biography', sa.Text(), nullable=True),
        sa.Column('profile_data', sa.JSON(), nullable=False, server_default=sa.text("'{}'::json")),
    )


def downgrade() -> None:
    op.drop_table('profiles')
    sa.Enum(name='profiletype').drop(op.get_bind(), checkfirst=True)
