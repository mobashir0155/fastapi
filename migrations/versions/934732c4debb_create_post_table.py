"""create_post_table

Revision ID: 934732c4debb
Revises: 
Create Date: 2024-05-02 10:50:16.598060

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '934732c4debb'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("posts", sa.Column("id", sa.Integer, primary_key=True, nullable=False), sa.Column("title", sa.String,nullable=False))
    pass


def downgrade() -> None:
    op.drop_table("posts")
    pass
