from typing import Optional

from pydantic import RootModel, BaseModel, Field
from integration_bus.application.dto import dataclasses


class RespDetail(dataclasses.EisDetail):
    pass


class RespList(RootModel[list[dataclasses.Eis]]):
    root: list[dataclasses.Eis]


class ReqCreate(BaseModel):
    title: str = Field(
        description='Название ВИС'
    )
    description: Optional[str] = Field(
        default=None,
        description='Описание ВИС'
    )
    host: Optional[str] = Field(
        default=None,
        description='Адрес ВИС'
    )
    port: Optional[int] = Field(
        default=None,
        description='Порт ВИС'
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


class ReqUpdate(BaseModel):
    id: int = Field(
        description='Уникальный идентификатор',
        gt=0
    )
    title: str = Field(
        description='Название ВИС'
    )
    description: Optional[str] = Field(
        default=None,
        description='Описание ВИС'
    )
    host: Optional[str] = Field(
        default=None,
        description='Адрес ВИС'
    )
    port: Optional[int] = Field(
        default=None,
        description='Порт ВИС'
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
