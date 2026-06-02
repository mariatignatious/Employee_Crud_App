# template of alembic
"""add-employee-departmet

Revision ID: 3f206cf9c84e
Revises: 40d7b9e29aef
Create Date: 2026-06-01 21:18:25.820761

"""

from typing import Sequence, Union


# revision identifiers, used by Alembic.
revision: str = "3f206cf9c84e"
down_revision: Union[str, Sequence[str], None] = "40d7b9e29aef"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
