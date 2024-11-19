"""Eis kind field

Revision ID: eddfe7efaae6
Revises: 1f1f3e7341c7
Create Date: 2023-09-18 13:11:51.042809+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eddfe7efaae6'
down_revision = '1f1f3e7341c7'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'runners',
        sa.Column('eis_from_kind', sa.String(length=128), nullable=False, comment='Вид ВИС, откуда брать данные')
    )
    op.add_column(
        'runners',
        sa.Column('eis_to_kind', sa.String(length=128), nullable=False, comment='Вид ВИС, куда сохранять данные')
    )


def downgrade():
    op.drop_column('runners', 'eis_to_kind')
    op.drop_column('runners', 'eis_from_kind')
