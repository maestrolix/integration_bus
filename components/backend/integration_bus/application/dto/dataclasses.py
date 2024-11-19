from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime as dt


class Eis(BaseModel):
    id: int = Field(
        description='Уникальный идентификатор',
        gt=0
    )
    title: str = Field(
        description='Название ВИС'
    )
    host: Optional[str] = Field(
        default=None,
        description='Адрес ВИС'
    )
    port: Optional[int] = Field(
        default=None,
        description='Порт ВИС'
    )
    eis_type: Optional[str] = Field(
        default=None,
        description='Тип ВИС'
    )


class EisDetail(Eis):
    description: Optional[str] = Field(
        default=None,
        description='Описание ВИС'
    )
    https: Optional[bool] = Field(
        default=None,
        description='Использование https или http. True, если https.'
    )
    username: Optional[str] = Field(
        default=None,
        description='Имя пользователя'
    )
    password: Optional[str] = Field(
        default=None,
        description='Пароль пользователя'
    )
    auth_endpoint: Optional[str] = Field(
        default=None,
        description='Конечная точка для авторизации'
    )
    db_name: Optional[str] = Field(
        default=None,
        description='Название базы данных'
    )
    db_type: Optional[str] = Field(
        default=None,
        description='Поставщик базы данных'
    )
    eis_type: Optional[str] = Field(
        default=None,
        description='Тип ВИС'
    )


class Runner(BaseModel):
    id: int = Field(
        gt=0,
        description='Уникальный идентификатор'
    )
    title: Optional[str] = Field(
        default=None,
        description='Название раннера'
    )
    key: str = Field(
        description='Уникальный ключ раннера'
    )
    status: str = Field(
        description='Статус раннера'
    )


class RunnerDetail(Runner):
    eis_from_id: Optional[int] = Field(
        gt=0,
        default=None,
        description='Информация о ВИС, откуда брать данные'
    )
    eis_to_id: Optional[int] = Field(
        gt=0,
        default=None,
        description='Информация о ВИС, куда сохранять данные'
    )
    description: Optional[str] = Field(
        default=None,
        description='Описание раннера'
    )
    launch_time: Optional[str] = Field(
        default=None,
        description='Время запуска задачи в формате cron'
    )
    blocked: bool = Field(
        default=False,
        description='Пользовательская блокировка'
    )
    test_mode: bool = Field(
        default=False,
        description='Тестовый режим'
    )
    push_notification: bool = Field(
        default=False,
        description='Пуш-уведомление'
    )
    eis_from_name: Optional[str] = Field(
        default=None,
        description='Название ВИС, откуда брать данные'
    )
    eis_to_name: Optional[str] = Field(
        default=None,
        description='Название ВИС, куда сохранять данные'
    )
    dependencies: list[Runner] = Field(
        description='Раннеры-зависимости'
    )
    available_eis_from: list[str] = Field(
        description='Список названий ВИС, доступных для этого раннера, откуда брать данные'
    )
    available_eis_to: list[str] = Field(
        description='Список названий ВИС, доступных для этого раннера, куда отправлять данные'
    )


class Event(BaseModel):
    id: int = Field(
        gt=0,
        description='Уникальный идентификатор'
    )
    runner_id: int = Field(
        gt=0,
        description='Идентификатор раннера, с которым связано данное событие'
    )
    runner: Runner = Field(
        description='Раннер, с которым связано данное событие'
    )
    status: str = Field(
        description='Текущий статус'
    )
    log_file_uri: Optional[str] = Field(
        default=None,
        description='Путь к файлу лога'
    )
    number: int = Field(
        description='Номер события'
    )
    datetime: dt = Field(
        comment='Время последнего обновления'
    )
