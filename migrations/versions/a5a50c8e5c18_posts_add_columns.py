"""posts_add_columns

Revision ID: a5a50c8e5c18
Revises: 1b6dc28d95ef
Create Date: 2024-05-02 11:13:57.682895

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a5a50c8e5c18'
down_revision: Union[str, None] = '1b6dc28d95ef'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("created_at", sa.TIMESTAMP(timezone=False), nullable=False, server_default=sa.text('now()')))
    pass


def downgrade() -> None:
    op.drop_column("posts","created_at")
    pass
