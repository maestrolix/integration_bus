from abc import ABC, abstractmethod
from typing import Optional, Any

from integration_bus.application import entities


class IConnectionManager(ABC):
    """ Менеджер соединений отвечает за создание новых соединений с ВИС
    на основе информации о ней. """
    @abstractmethod
    async def create(self, eis: entities.Eis) -> Optional[Any]:
        """ Создает новое соединение с ВИС по информации о ней. """
        raise NotImplementedError
