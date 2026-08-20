"""add role requests and audit logs

Revision ID: add_role_requests_and_audit_logs
Revises: 
Create Date: 2026-08-12 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'add_role_requests_and_audit_logs'
down_revision = '9d3032e53223'
branch_labels = None
depends_on = None


def upgrade():
    # Create enum type for role request status
    role_status = postgresql.ENUM('PENDING', 'APPROVED', 'REJECTED', name='rolerequeststatus')
    role_status.create(op.get_bind(), checkfirst=True)

    op.create_table(
        'role_change_requests',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('requested_role', postgresql.ENUM('REGULAR', 'ADMIN', 'SUPER_USER', 'MEGA_USER', name='userrole', create_type=False), nullable=False),
        sa.Column('status', postgresql.ENUM('PENDING', 'APPROVED', 'REJECTED', name='rolerequeststatus', create_type=False), nullable=False),
        sa.Column('document_filename', sa.String(length=200), nullable=True),
        sa.Column('admin_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('admin_notes', sa.String(length=1000), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('reviewed_at', sa.TIMESTAMP(timezone=True), nullable=True),
    )

    op.create_table(
        'audit_logs',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('actor_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('target_user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('action', sa.String(length=200), nullable=False),
        sa.Column('details', sa.String(length=2000), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    )


def downgrade():
    op.drop_table('audit_logs')
    op.drop_table('role_change_requests')
    # drop enum type
    role_status = postgresql.ENUM('PENDING', 'APPROVED', 'REJECTED', name='rolerequeststatus')
    role_status.drop(op.get_bind(), checkfirst=True)
