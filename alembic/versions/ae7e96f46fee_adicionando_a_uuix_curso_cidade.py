"""adicionando a Uuix_curso_cidade

Revision ID: ae7e96f46fee
Revises: 384a305e9fda
Create Date: 2025-10-07 12:12:59.988551

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ae7e96f46fee'
down_revision: Union[str, Sequence[str], None] = '384a305e9fda'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
