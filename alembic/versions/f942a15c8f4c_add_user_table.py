"""add user table

Revision ID: f942a15c8f4c
Revises: a04f31af2cbd
Create Date: 2024-03-20 23:38:51.369372

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f942a15c8f4c'
down_revision: Union[str, None] = 'a04f31af2cbd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    sa.Column('id',sa.Integer(), nullable=False),
    sa.Column('email',sa.String(), nullable=False),
    sa.Column('password',sa.String(), nullable=False),
    sa.Column('created_at',sa.TIMESTAMP(timezone=True),
              server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    pass


def downgrade():
    op.drop_table('users')
    pass
