"""auto_vote

Revision ID: 877e3319042a
Revises: ae2bfd9b3e55
Create Date: 2025-03-21 18:59:48.924582

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '877e3319042a'
down_revision: Union[str, None] = 'ae2bfd9b3e55'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('votes',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['posts.post_id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'post_id')
    )
    op.create_index(op.f('ix_posts_post_id'), 'posts', ['post_id'], unique=False)
    op.create_index(op.f('ix_users_user_id'), 'users', ['user_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_user_id'), table_name='users')
    op.drop_index(op.f('ix_posts_post_id'), table_name='posts')
    op.drop_table('votes')
    # ### end Alembic commands ###
