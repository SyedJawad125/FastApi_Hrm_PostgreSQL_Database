"""add_payslips_table

Revision ID: 37beb8956a6e
Revises: b83b7a8d2fd4
Create Date: 2025-07-15 17:06:14.593681

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '37beb8956a6e'
down_revision: Union[str, Sequence[str], None] = 'b83b7a8d2fd4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
