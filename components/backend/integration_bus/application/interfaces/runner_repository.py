from abc import ABC, abstractmethod
from typing import Optional

from integration_bus.application import dto, entities
from integration_bus.application.util import enum
from integration_bus.application.util.enum import RunnerStatus, EisKind


class IRunnerRepository(ABC):

    @abstractmethod
    async def get_runners_list(self) -> list[entities.Runner]:
        """ Возвращает множество записей о раннерах из БД. """
        raise NotImplementedError

    @abstractmethod
    async def get_runners_key_list(self) -> list[str]:
        """ Возвращает список всех ключей раннеров, которые есть в БД. """
        raise NotImplementedError

    @abstractmethod
    async def get_runner_by_id(self, id_: int) -> Optional[entities.Runner]:
        """
        Возвращает одну запись о раннере из БД по идентификатору.
        
        Если раннер не был найден, возвращает `None`.
        """
        raise NotImplementedError

    @abstractmethod
    async def check_if_exists_by_id(self, id_: int) -> bool:
        """ Проверяет, существует ли запись о раннере в БД, по идентификатору. """
        raise NotImplementedError

    @abstractmethod
    async def get_runner_by_key(self, key: str) -> Optional[entities.Runner]:
        """
        Выполняет поиск записи о раннере по ключу.
        
        Если раннер найден, возвращает информацию о раннере. Иначе возвращает `None`.
        """
        raise NotImplementedError

    @abstractmethod
    async def add_runner(self, runner: entities.Runner):
        """ Сохраняет информацию о новом раннере в БД. """
        raise NotImplementedError

    @abstractmethod
    async def update_runner(self, runner: dto.runner.ReqUpdate):
        """ Обновляет информацию о раннере в БД. """
        raise NotImplementedError

    @abstractmethod
    async def update_runner_eis_from_kind(self, id_: int, kind: EisKind):
        """ Обновляет вид ВИС, откуда брать данные. """
        raise NotImplementedError

    @abstractmethod
    async def update_runner_eis_to_kind(self, id_: int, kind: EisKind):
        """ Обновляет вид ВИС, куда отправлять данные. """
        raise NotImplementedError

    @abstractmethod
    async def delete_runner(self, id: int) -> Optional[int]:
        """
        Удаляет раннер по его идентификатору.
        
        Возвращает идентификатор в случае успешного удаления. Иначе `None`.
        """
        raise NotImplementedError

    @abstractmethod
    async def update_runner_status(self, id_: int, status: RunnerStatus):
        """ Обновляет статус раннера по его идентификатору. """
        raise NotImplementedError

    @abstractmethod
    async def update_runner_dependencies(self, id_: int, dependency_ids: list[int]):
        """ Обновляет список зависимостей раннера. """
        raise NotImplementedError

    @abstractmethod
    async def try_update_runner_status(
        self, 
        runners: list[entities.Runner], 
        status: enum.RunnerStatus, 
        status_clause: enum.RunnerStatus
    ) -> tuple[list[entities.Runner], bool]:
        """ """
        raise NotImplementedError