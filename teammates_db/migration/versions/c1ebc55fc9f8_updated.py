"""updated

Revision ID: c1ebc55fc9f8
Revises: 7243dc97be43
Create Date: 2025-02-14 20:43:44.393065

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c1ebc55fc9f8'
down_revision: Union[str, None] = '7243dc97be43'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('password', table_name='users')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('password', 'users', ['password'], unique=True)
    # ### end Alembic commands ###
