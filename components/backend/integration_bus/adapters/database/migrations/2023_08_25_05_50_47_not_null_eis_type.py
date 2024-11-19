"""Not null eis_type

Revision ID: 081491b902be
Revises: c2fc16d7a642
Create Date: 2023-08-25 05:50:47.749402+00:00

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '081491b902be'
down_revision = 'c2fc16d7a642'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        'eis', 'eis_type',
        existing_type=sa.VARCHAR(length=128),
        nullable=False,
        existing_comment='Тип ВИС'
    )


def downgrade():
    op.alter_column(
        'eis', 'eis_type',
        existing_type=sa.VARCHAR(length=128),
        nullable=True,
        existing_comment='Тип ВИС'
    )
