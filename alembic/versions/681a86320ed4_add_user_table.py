"""add user table

Revision ID: 681a86320ed4
Revises: b124bce6f423
Create Date: 2025-03-21 17:06:51.805367

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '681a86320ed4'
down_revision: Union[str, None] = 'b124bce6f423'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users', 
                    sa.Column("user_id", sa.Integer(), nullable=False, primary_key=True),
                    sa.Column("email", sa.String(), nullable=False, unique=True),
                    sa.Column("password", sa.String(), nullable=False),
                    sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()'))
                    )


def downgrade() -> None:
    op.drop_table('users')