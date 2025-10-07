"""adicionando a UQ_curso_cidade

Revision ID: 6ea60816b767
Revises: eee782bd5d79
Create Date: 2025-10-07 12:02:19.307053

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6ea60816b767'
down_revision: Union[str, Sequence[str], None] = 'eee782bd5d79'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
