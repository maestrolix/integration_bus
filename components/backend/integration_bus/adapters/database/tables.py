from sqlalchemy import (
    TIMESTAMP,
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
    Text,
    Sequence,
)

naming_convention = {
    'ix': 'ix_%(column_0_label)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(table_name)s_%(constraint_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'pk': 'pk_%(table_name)s'
}

metadata = MetaData(
    naming_convention=naming_convention
)

eis = Table(
    'eis',
    metadata,
    Column(
        'id',
        Integer,
        primary_key=True,
        comment='Уникальный идентификатор'
    ),
    Column(
        'title',
        String(256),
        nullable=False,
        comment='Название ВИС'
    ),
    Column(
        'description',
        Text,
        comment='Описание ВИС'
    ),
    Column(
        'host',
        String(256),
        comment='Адрес ВИС'
    ),
    Column(
        'port',
        Integer,
        comment='Порт ВИС'
    ),
    Column(
        'https',
        Boolean,
        comment='Использование https или http. True, если https.'
    ),
    Column(
        'username',
        String(256),
        comment='Имя пользователя'
    ),
    Column(
        'password',
        String(256),
        comment='Пароль пользователя'
    ),
    Column(
        'auth_endpoint',
        String(256),
        comment='Конечная точка для авторизации'
    ),
    Column(
        'db_name',
        String(128),
        comment='Название базы данных'
    ),
    Column(
        'db_type',
        String(128),
        comment='Поставщик базы данных'
    ),
    Column(
        'eis_type',
        String(128),
        nullable=False,
        comment='Тип ВИС'
    ),
    comment='Информация о внешних информационных системах'
)

runners = Table(
    'runners',
    metadata,
    Column(
        'id',
        Integer,
        primary_key=True,
        comment='Уникальный идентификатор'
    ),
    Column(
        'title',
        String(256),
        nullable=True,
        comment='Название раннера'
    ),
    Column(
        'eis_from_id',
        ForeignKey('eis.id', ondelete='CASCADE'),
        nullable=True,
        comment='Идентификатор ВИС, откуда брать данные'
    ),
    Column(
        'eis_to_id',
        ForeignKey('eis.id', ondelete='CASCADE'),
        nullable=True,
        comment='Идентификатор ВИС, куда сохранять данные'
    ),
    Column(
        'key',
        String(256),
        nullable=False,
        unique=True,
        comment='Ключ раннера'
    ),
    Column(
        'description',
        Text,
        comment='Описание раннера'
    ),
    Column(
        'launch_time',
        String(64),
        nullable=True,
        comment='Время запуска задачи в формате cron'
    ),
    Column(
        'blocked',
        Boolean,
        nullable=False,
        default=False,
        comment='Пользовательская блокировка'
    ),
    Column(
        'test_mode',
        Boolean,
        nullable=False,
        default=False,
        comment='Тестовый режим'
    ),
    Column(
        'push_notification',
        Boolean,
        nullable=False,
        default=False,
        comment='Пуш-уведомление'
    ),
    Column(
        'status',
        String(128),
        nullable=False,
        comment='Статус раннера'
    ),
    Column(
        'eis_from_kind',
        String(128),
        nullable=False,
        comment='Вид ВИС, откуда брать данные',
    ),
    Column(
        'eis_to_kind',
        String(128),
        nullable=False,
        comment='Вид ВИС, куда сохранять данные'
    ),
    comment='Информация о раннерах'
)

mock_data = Table(
    'mock_data',
    metadata,
    Column(
        'id',
        Integer,
        primary_key=True,
        comment='Уникальный идентификатор'
    ),
    Column(
        'runner_id',
        ForeignKey('runners.id', ondelete='CASCADE'),
        nullable=False,
        comment='Идентификатор раннера, с которым связаны тестовые данные'
    ),
    Column(
        'title',
        String(256),
        nullable=False,
        comment='Название тестовых данных'
    ),
    Column(
        'file_uri',
        String(256),
        nullable=False,
        comment='Путь к файлу с данными'
    ),
    Column(
        'is_main',
        Boolean,
        nullable=False,
        default=False,
        comment='Является ли тестовый файл главным'
    ),
    comment='Информация о файлах с тестовыми данными'
)

runners_dependencies = Table(
    'runners_dependencies',
    metadata,
    Column(
        'runner_id',
        ForeignKey('runners.id', ondelete='CASCADE'),
        primary_key=True,
        nullable=False,
        comment='Идентификатор основного раннера'
    ),
    Column(
        'dependency_runner_id',
        ForeignKey('runners.id', ondelete='CASCADE'),
        primary_key=True,
        nullable=False,
        comment='Идентификатор раннера-зависимости'
    ),
    comment='Зависимости раннеров (ассоциативная таблица)'
)


# Логирование ранеров

runner_execution_requests = Table(
    'runner_execution_requests', 
    metadata, 
    Column(
        'id',
        Integer,
        primary_key=True,
        comment='Уникальный идентификатор'
    ),
    Column(
        'status', 
        String(32), 
        nullable=False,
        comment='Статус запроса на выгрузку'
    ),
    Column(
        'total_time_execution', 
        Float, 
        nullable=True,
        comment='Общее время запроса на выгрузку'
        
    ),
    Column(
        'created_at', 
        TIMESTAMP(), 
        nullable=False, 
        comment='Время создания события'
    ),
    comment='Здесь хранится конкретный запрос по ключу. '
)

runner_events = Table(
    'runner_events',
    metadata, 
    Column(
        'id',
        Integer,
        primary_key=True,
        comment='Уникальный идентификатор'
    ),
    Column(
        'runner_id',
        ForeignKey('runners.id', ondelete='SET NULL'),
        nullable=True,
        comment='Ссылка на ранер'
    ),
    Column(
        'request_id',
        ForeignKey('runner_execution_requests.id', ondelete='CASCADE'),
        nullable=True,
        comment='Ссылка на запрос'
    ),
    Column(
        'status', 
        String(32), 
        nullable=False,
        comment='Статус ранера'
    ),
    Column(
        'time_execution_runner', 
        Float, 
        nullable=True, 
        comment='Время исполнения ранера'
    ), 
    Column(
        'created_at', 
        TIMESTAMP(), 
        nullable=False, 
        comment='Время создания события'
    ),
    comment='Хранятся события ранеров, которые были вызваны по запросу по ключу.'
)

runner_logs = Table(
    'runner_logs',
    metadata,
    Column(
        'id',
        Integer,
        primary_key=True,
        comment='Уникальный идентификатор'
    ),
    Column(
        'event_id',
        ForeignKey('runner_events.id', ondelete='CASCADE'),
        nullable=True,
        comment='Ссылка на событие ранера'
    ),
    Column(
        'status', 
        String(32), 
        nullable=False,
        comment='Статус лога'
    ),
    Column(
        'type', 
        String(32), 
        nullable=False,
        comment='Тип лога'
    ),
    Column(
        'text', 
        String(1024), 
        nullable=False, 
        comment='Текст лога'
    ),
    Column(
        'created_at', 
        TIMESTAMP(), 
        nullable=False, 
        comment='Время создания события'
    )
)