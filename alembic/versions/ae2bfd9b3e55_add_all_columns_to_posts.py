"""add all columns to posts

Revision ID: ae2bfd9b3e55
Revises: 5e23808626a3
Create Date: 2025-03-21 18:43:03.308540

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ae2bfd9b3e55'
down_revision: Union[str, None] = '5e23808626a3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("published", sa.Boolean(), nullable=False, server_default=sa.text("false")))
    op.add_column("posts", sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')))

def downgrade() -> None:
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")