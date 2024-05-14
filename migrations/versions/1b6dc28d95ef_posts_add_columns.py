"""posts_add_columns

Revision ID: 1b6dc28d95ef
Revises: 934732c4debb
Create Date: 2024-05-02 11:07:01.440952

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1b6dc28d95ef'
down_revision: Union[str, None] = '934732c4debb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String, nullable=False))
    op.add_column("posts", sa.Column("published", sa.Boolean, nullable=True, server_default="False"))
    pass


def downgrade() -> None:
    op.drop_column("posts","content")
    op.drop_column("posts","published")
    pass
