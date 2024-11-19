from typing import Optional

from pydantic import RootModel, BaseModel, Field

from integration_bus.application.dto import dataclasses


class RespDetail(dataclasses.RunnerDetail):
    pass


class RespList(RootModel[list[dataclasses.Runner]]):
    root: list[dataclasses.Runner]


class ReqUpdate(BaseModel):
    id: int = Field(
        description='Уникальный идентификатор',
        gt=0
    )
    title: Optional[str] = Field(
        default=None,
        description='Название раннера'
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
    status: str = Field(
        description='Статус раннера'
    )
