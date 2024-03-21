"""adding remaining information

Revision ID: 2ea021b46a04
Revises: f942a15c8f4c
Create Date: 2024-03-20 23:45:09.333282

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2ea021b46a04'
down_revision: Union[str, None] = 'f942a15c8f4c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    sa.Column('id',sa.Integer(), nullable=False),
    sa.Column('email',sa.String(), nullable=False),
    sa.Column('password',sa.String(), nullable=False),
    sa.Column('created_at',sa.TIMESTAMP(timezone=True),
              server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
