"""adicionando a UQ_curso_cidade

Revision ID: 384a305e9fda
Revises: 6ea60816b767
Create Date: 2025-10-07 12:11:38.356524

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '384a305e9fda'
down_revision: Union[str, Sequence[str], None] = '6ea60816b767'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
