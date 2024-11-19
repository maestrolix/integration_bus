from abc import ABC, abstractmethod
from dataclasses import dataclass

from sqlalchemy.ext.asyncio import async_sessionmaker


@dataclass
class IDatabaseConnection(ABC):
    """ Интерфейс соединения с базой данных. """
    @property
    @abstractmethod
    def session_maker(self) -> async_sessionmaker:
        raise NotImplementedError
