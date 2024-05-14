"""create_users_table

Revision ID: 3a89ee52c184
Revises: 268eaddbb734
Create Date: 2024-05-02 11:32:32.480336

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3a89ee52c184'
down_revision: Union[str, None] = 'a5a50c8e5c18'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id",sa.Integer, nullable=False),
        sa.Column("email",sa.String, nullable=False),
        sa.Column("password",sa.String, nullable=False),
        sa.Column("created_at",sa.TIMESTAMP(timezone=False), nullable=False, server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email")
    )
    pass


def downgrade() -> None:
    op.drop_table("users")
    pass
