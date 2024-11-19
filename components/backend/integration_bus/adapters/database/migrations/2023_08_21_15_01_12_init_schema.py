"""Init schema

Revision ID: 173c8d25c95e
Revises:
Create Date: 2023-08-21 15:01:12.157450+00:00

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '173c8d25c95e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'eis',
        sa.Column('id', sa.Integer(), nullable=False, comment='Уникальный идентификатор'),
        sa.Column('title', sa.String(length=256), nullable=False, comment='Название ВИС'),
        sa.Column('description', sa.Text(), nullable=True, comment='Описание ВИС'),
        sa.Column('host', sa.String(length=256), nullable=True, comment='Адрес ВИС'),
        sa.Column('port', sa.Integer(), nullable=True, comment='Порт ВИС'),
        sa.Column('https', sa.Boolean(), nullable=True,
                  comment='Использование https или http. True, если https.'),
        sa.Column('username', sa.String(length=256), nullable=True, comment='Имя пользователя'),
        sa.Column('password', sa.String(length=256), nullable=True, comment='Пароль пользователя'),
        sa.Column('auth_endpoint', sa.String(length=256), nullable=True,
                  comment='Конечная точка для авторизации'),
        sa.Column('db_name', sa.String(length=128), nullable=True, comment='Название базы данных'),
        sa.Column('db_type', sa.String(length=128), nullable=True, comment='Поставщик базы данных'),
        sa.Column('eis_type', sa.String(length=128), nullable=True, comment='Тип ВИС'),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_eis')),
        comment='Информация о внешних информационных системах'
    )
    op.create_table(
        'runners',
        sa.Column('id', sa.Integer(), nullable=False, comment='Уникальный идентификатор'),
        sa.Column('eis_from_id', sa.Integer(), nullable=False,
                  comment='Идентификатор ВИС, откуда брать данные'),
        sa.Column('eis_to_id', sa.Integer(), nullable=False,
                  comment='Идентификатор ВИС, куда сохранять данные'),
        sa.Column('key', sa.String(length=256), nullable=False, comment='Ключ раннера'),
        sa.Column('description', sa.Text(), nullable=True, comment='Описание раннера'),
        sa.Column('launch_time', sa.String(length=64), nullable=False,
                  comment='Время запуска задачи в формате cron'),
        sa.Column('blocked', sa.Boolean(), nullable=False, comment='Пользовательская блокировка'),
        sa.Column('test_mode', sa.Boolean(), nullable=False, comment='Тестовый режим'),
        sa.Column('push_notification', sa.Boolean(), nullable=False, comment='Пуш-уведомление'),
        sa.Column('status', sa.String(length=128), nullable=False, comment='Статус раннера'),
        sa.ForeignKeyConstraint(['eis_from_id'], ['eis.id'], name=op.f('fk_runners_eis_from_id_eis'),
                                ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['eis_to_id'], ['eis.id'], name=op.f('fk_runners_eis_to_id_eis'),
                                ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_runners')),
        sa.UniqueConstraint('key', name=op.f('uq_runners_key')),
        comment='Информация о раннерах'
    )
    op.create_table(
        'events',
        sa.Column('id', sa.Integer(), nullable=False, comment='Уникальный идентификатор'),
        sa.Column('runner_id', sa.Integer(), nullable=False,
                  comment='Идентификатор раннера, с которым связано данное событие'),
        sa.Column('status', sa.String(length=128), nullable=False, comment='Текущий статус'),
        sa.Column('log_file_uri', sa.String(length=256), nullable=True, comment='Путь к файлу лога'),
        sa.Column('number', sa.Integer(), nullable=False, comment='Номер события'),
        sa.Column('datetime', sa.TIMESTAMP(), nullable=False, comment='Время последнего обновления'),
        sa.ForeignKeyConstraint(['runner_id'], ['runners.id'], name=op.f('fk_events_runner_id_runners'),
                                ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_events')),
        comment='Информация о событиях системы'
    )
    op.create_table(
        'mock_data',
        sa.Column('id', sa.Integer(), nullable=False, comment='Уникальный идентификатор'),
        sa.Column('runner_id', sa.Integer(), nullable=False,
                  comment='Идентификатор раннера, с которым связаны тестовые данные'),
        sa.Column('title', sa.String(length=256), nullable=False, comment='Название тестовых данных'),
        sa.Column('file_uri', sa.String(length=256), nullable=False, comment='Путь к файлу с данными'),
        sa.Column('is_main', sa.Boolean(), nullable=False, comment='Является ли тестовый файл главным'),
        sa.ForeignKeyConstraint(['runner_id'], ['runners.id'], name=op.f('fk_mock_data_runner_id_runners'),
                                ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_mock_data')),
        comment='Информация о файлах с тестовыми данными'
    )
    op.create_table(
        'runners_dependencies',
        sa.Column('runner_id', sa.Integer(), nullable=False, comment='Идентификатор основного раннера'),
        sa.Column('dependency_runner_id', sa.Integer(), nullable=False,
                  comment='Идентификатор раннера-зависимости'),
        sa.ForeignKeyConstraint(['dependency_runner_id'], ['runners.id'],
                                name=op.f('fk_runners_dependencies_dependency_runner_id_runners'),
                                ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['runner_id'], ['runners.id'],
                                name=op.f('fk_runners_dependencies_runner_id_runners'), ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('runner_id', 'dependency_runner_id', name=op.f('pk_runners_dependencies')),
        comment='Зависимости раннеров (ассоциативная таблица)'
    )


def downgrade():
    op.drop_table('runners_dependencies')
    op.drop_table('mock_data')
    op.drop_table('events')
    op.drop_table('runners')
    op.drop_table('eis')
