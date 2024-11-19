from typing import Optional
from pydantic import RootModel, BaseModel, Field
from datetime import datetime as dt

from integration_bus.application.dto import dataclasses


class RespList(RootModel[list[dataclasses.Event]]):
    root: list[dataclasses.Event]


class ReqCreate(BaseModel):
    runner_id: int = Field(
        gt=0,
        description='Идентификатор раннера, с которым связано данное событие'
    )
    status: str = Field(
        description='Текущий статус'
    )
    log_file_uri: Optional[str] = Field(
        default=None,
        description='Путь к файлу лога'
    )
    datetime: dt = Field(
        comment='Время последнего обновления'
    )
    # TODO: временное решение, пока не будет известно, как сделать autoincrement на не PK колонке
    number: int = Field(
        default=1,
        gt=0
    )


class ReqUpdate(BaseModel):
    id: int = Field(
        description='Уникальный идентификатор',
        gt=0
    )
    runner_id: int = Field(
        gt=0,
        description='Идентификатор раннера, с которым связано данное событие'
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
