"""merge all heads

Revision ID: b71c898d4c34
Revises: 8d0363f15064, 2a64eb969a9c
Create Date: 2025-07-10 12:04:10.207201

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b71c898d4c34'
down_revision: Union[str, Sequence[str], None] = ('8d0363f15064', '2a64eb969a9c')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
