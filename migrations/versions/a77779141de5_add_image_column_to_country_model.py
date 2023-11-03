"""Add image column to Country model

Revision ID: a77779141de5
Revises: 74b7f5bc4646
Create Date: 2023-10-24 00:03:49.335811

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a77779141de5'
down_revision: Union[str, None] = '74b7f5bc4646'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('countries', sa.Column('country_image', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('countries', 'country_image')
    # ### end Alembic commands ###
