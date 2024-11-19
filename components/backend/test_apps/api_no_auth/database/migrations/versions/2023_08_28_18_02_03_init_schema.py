"""Init schema

Revision ID: d85460e17e6d
Revises: 
Create Date: 2023-08-28 18:02:03.343382

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'd85460e17e6d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'person',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(length=256), nullable=False),
        sa.Column('gender', sa.Boolean(), nullable=False),
        sa.Column('age', sa.Integer(), nullable=False),
    )
    op.create_table(
        'pet',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(length=128), nullable=False),
        sa.Column('age', sa.Integer(), nullable=False),
        sa.Column('gender', sa.Boolean(), nullable=False),
        sa.Column('animal', sa.String(length=128), nullable=False),
        sa.Column('owner_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['owner_id'], ['person.id'], ),
    )


def downgrade() -> None:
    op.drop_table('pet')
    op.drop_table('person')
