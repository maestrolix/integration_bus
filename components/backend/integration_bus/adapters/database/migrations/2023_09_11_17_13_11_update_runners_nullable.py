"""Update runners nullable

Revision ID: 1f1f3e7341c7
Revises: 081491b902be
Create Date: 2023-09-11 17:13:11.057938+00:00

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '1f1f3e7341c7'
down_revision = '081491b902be'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        'runners', 'launch_time',
        existing_type=sa.VARCHAR(length=64),
        nullable=True,
        existing_comment='Время запуска задачи в формате cron'
    )
    op.alter_column(
        'runners', 'title',
        existing_type=sa.VARCHAR(length=256),
        nullable=True,
        existing_comment='Название раннера'
    )
    op.alter_column(
        'runners', 'eis_from_id',
        existing_type=sa.INTEGER(),
        nullable=True,
        existing_comment='Идентификатор ВИС, откуда брать данные'
    )
    op.alter_column(
        'runners', 'eis_to_id',
        existing_type=sa.INTEGER(),
        nullable=True,
        existing_comment='Идентификатор ВИС, куда сохранять данные'
    )


def downgrade():
    op.alter_column(
        'runners', 'eis_to_id',
        existing_type=sa.INTEGER(),
        nullable=False,
        existing_comment='Идентификатор ВИС, куда сохранять данные'
    )
    op.alter_column(
        'runners', 'eis_from_id',
        existing_type=sa.INTEGER(),
        nullable=False,
        existing_comment='Идентификатор ВИС, откуда брать данные'
    )
    op.alter_column(
        'runners', 'title',
        existing_type=sa.VARCHAR(length=256),
        nullable=False,
        existing_comment='Название раннера'
    )
    op.alter_column(
        'runners', 'launch_time',
        existing_type=sa.VARCHAR(length=64),
        nullable=False,
        existing_comment='Время запуска задачи в формате cron'
    )
