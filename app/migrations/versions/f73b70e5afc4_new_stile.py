"""New stile

Revision ID: f73b70e5afc4
Revises: e6bcff3734cf
Create Date: 2024-02-05 21:13:36.693432

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'f73b70e5afc4'
down_revision: Union[str, None] = 'e6bcff3734cf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('rooms', 'image_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('rooms', 'image_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###
