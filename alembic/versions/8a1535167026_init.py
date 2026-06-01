# template of alembic
"""init

Revision ID: 8a1535167026
Revises: a8706465a812
Create Date: 2026-05-28 17:13:43.074072

"""

from typing import Sequence, Union


# revision identifiers, used by Alembic.
revision: str = "8a1535167026"
down_revision: Union[str, Sequence[str], None] = "a8706465a812"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
