"""add content

Revision ID: a04f31af2cbd
Revises: ded08a38434e
Create Date: 2024-03-20 23:35:24.530933

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a04f31af2cbd'
down_revision: Union[str, None] = 'ded08a38434e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
