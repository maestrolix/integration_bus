"""Add cascade

Revision ID: 6831e69e0b48
Revises: 503af0d29c7b
Create Date: 2023-08-28 19:11:31.742693

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6831e69e0b48'
down_revision: Union[str, None] = '503af0d29c7b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint('pet_owner_id_fkey', 'pet', type_='foreignkey')
    op.create_foreign_key(None, 'pet', 'person', ['owner_id'], ['id'], ondelete='CASCADE')


def downgrade() -> None:
    op.drop_constraint(None, 'pet', type_='foreignkey')
    op.create_foreign_key('pet_owner_id_fkey', 'pet', 'person', ['owner_id'], ['id'])
