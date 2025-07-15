"""add_salary_history_table

Revision ID: fc3f619610bd
Revises: 37beb8956a6e
Create Date: 2024-03-19 12:34:56.789012

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fc3f619610bd'
down_revision: Union[str, None] = '37beb8956a6e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create salary_histories table
    op.create_table('salary_histories',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('previous_salary', sa.Float(), nullable=False),
        sa.Column('new_salary', sa.Float(), nullable=False),
        sa.Column('change_percentage', sa.Float(), nullable=False),
        sa.Column('change_type', sa.String(), nullable=False),
        sa.Column('change_reason', sa.Text(), nullable=True),
        sa.Column('effective_date', sa.Date(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column('employee_id', sa.Integer(), nullable=False),
        sa.Column('previous_rank_id', sa.Integer(), nullable=False),
        sa.Column('new_rank_id', sa.Integer(), nullable=False),
        sa.Column('department_id', sa.Integer(), nullable=False),
        sa.Column('created_by_user_id', sa.Integer(), nullable=False),
        sa.Column('salary_structure_id', sa.Integer(), nullable=True),
        sa.Column('employee_salary_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['created_by_user_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['department_id'], ['departments.id'], ),
        sa.ForeignKeyConstraint(['employee_id'], ['employees.id'], ),
        sa.ForeignKeyConstraint(['employee_salary_id'], ['employee_salaries.id'], ),
        sa.ForeignKeyConstraint(['new_rank_id'], ['ranks.id'], ),
        sa.ForeignKeyConstraint(['previous_rank_id'], ['ranks.id'], ),
        sa.ForeignKeyConstraint(['salary_structure_id'], ['salary_structures.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_salary_histories_id'), 'salary_histories', ['id'], unique=False)


def downgrade() -> None:
    # Drop salary_histories table
    op.drop_index(op.f('ix_salary_histories_id'), table_name='salary_histories')
    op.drop_table('salary_histories')
