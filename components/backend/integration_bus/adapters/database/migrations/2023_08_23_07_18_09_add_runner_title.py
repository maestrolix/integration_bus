"""Add runner title

Revision ID: c2fc16d7a642
Revises: 173c8d25c95e
Create Date: 2023-08-23 07:18:09.816994+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c2fc16d7a642'
down_revision = '173c8d25c95e'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('runners', sa.Column('title', sa.String(length=256), nullable=False, comment='Название раннера'))


def downgrade():
    op.drop_column('runners', 'title')
