"""add foreign key to posts

Revision ID: 5e23808626a3
Revises: 681a86320ed4
Create Date: 2025-03-21 18:23:53.910566

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5e23808626a3'
down_revision: Union[str, None] = '681a86320ed4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False))


def downgrade() -> None:
    op.drop_column("posts", "user_id")
