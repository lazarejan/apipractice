"""empty message

Revision ID: b124bce6f423
Revises: be8b79390e49
Create Date: 2025-03-21 17:00:37.561430

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b124bce6f423'
down_revision: Union[str, None] = 'be8b79390e49'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    

def downgrade() -> None:
    op.drop_column("posts", "content")