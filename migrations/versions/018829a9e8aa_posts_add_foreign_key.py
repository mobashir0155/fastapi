"""posts_add_foreign_key

Revision ID: 018829a9e8aa
Revises: 3a89ee52c184
Create Date: 2024-05-02 11:41:19.281156

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '018829a9e8aa'
down_revision: Union[str, None] = '3a89ee52c184'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("owner_id", sa.Integer, nullable=False))
    op.create_foreign_key("fk_posts_users",source_table="posts", referent_table="users",local_cols=["owner_id"],remote_cols=["id"], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint("fk_posts_users",table_name="posts",type_="foreignkey")
    op.drop_column("posts","owner_id")
    pass
