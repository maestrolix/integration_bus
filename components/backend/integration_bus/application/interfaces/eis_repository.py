from abc import ABC, abstractmethod
from typing import Optional

from integration_bus.application import dto, entities
from integration_bus.application.util.enum import EisKind


class IEisRepository(ABC):

    @abstractmethod
    async def get_eis_list(self) -> list[entities.Eis]:
        """ Возвращает множество записей о ВИС из БД. """
        raise NotImplementedError

    @abstractmethod
    async def get_eis_by_id(self, id_: int) -> Optional[entities.Eis]:
        """
        Возвращает одну запись о ВИС из БД по идентификатору.
        
        Если ВИС не была найдена, возвращает `None`.
        """
        raise NotImplementedError

    @abstractmethod
    async def check_if_exists_by_id(self, id_: int) -> bool:
        """ Проверяет, существует ли запись о ВИС в БД, по идентификатору. """
        raise NotImplementedError

    @abstractmethod
    async def add_eis(self, eis: dto.eis.ReqCreate) -> int:
        """ Сохраняет информацию о новой ВИС в БД. """
        raise NotImplementedError

    @abstractmethod
    async def update_eis(self, eis: dto.eis.ReqUpdate):
        """ Обновляет информацию о ВИС в БД. """
        raise NotImplementedError

    @abstractmethod
    async def delete_eis(self, id_: int) -> Optional[int]:
        """
        Удаляет ВИС по его идентификатору.
        
        Возвращает идентификатор в случае успешного удаления. Иначе `None`.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_eis_list_of_kind(self, kind: EisKind) -> list[str]:
        """ Возвращает список названий ВИС, которые относятся к виду `kind`. """
        raise NotImplementedError
