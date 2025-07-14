"""add_leave_management_table

Revision ID: 2a64eb969a9c
Revises: 070700d9f55c
Create Date: 2024-03-19 12:34:56.789012

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2a64eb969a9c'
down_revision: Union[str, None] = None  # Changed to None to make it independent
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create leave_type enum
    op.create_table('leaves',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('start_date', sa.DateTime(), nullable=False),
        sa.Column('end_date', sa.DateTime(), nullable=False),
        sa.Column('leave_type', sa.String(), nullable=False),
        sa.Column('reason', sa.String(), nullable=False),
        sa.Column('status', sa.String(), server_default='pending', nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column('employee_id', sa.Integer(), nullable=False),
        sa.Column('approved_by_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['employee_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['approved_by_id'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_leaves_id'), 'leaves', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_leaves_id'), table_name='leaves')
    op.drop_table('leaves')
