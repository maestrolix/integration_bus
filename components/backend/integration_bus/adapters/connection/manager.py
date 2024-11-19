from typing import Optional, Union
from enum import StrEnum, auto

from integration_bus.application import entities
from integration_bus.adapters.connection.types import (
    HttpNoAuthConnection,
    HttpBasicAuthConnection,
    DatabaseAuthConnection,
    HttpJwtAuthConnection
)
from integration_bus.application.interfaces.connection import IConnectionManager


class ConnectionType(StrEnum):
    HTTP_NO_AUTH = auto()
    HTTP_BASIC_AUTH = auto()
    HTTP_JWT_AUTH = auto()
    DATABASE_AUTH = auto()


AnyConnection = Union[HttpNoAuthConnection, HttpBasicAuthConnection, DatabaseAuthConnection]


class ConnectionManager(IConnectionManager):
    __cached_connections: dict[int, AnyConnection] = {}

    async def create(self, eis: entities.Eis) -> Optional[AnyConnection]:
        if self.__cached_connections.get(eis.id) is None:
            conn = None
            if eis.eis_type == ConnectionType.HTTP_NO_AUTH:
                conn = HttpNoAuthConnection(eis=eis)
            elif eis.eis_type == ConnectionType.HTTP_BASIC_AUTH:
                conn = HttpBasicAuthConnection(eis=eis)
            elif eis.eis_type == ConnectionType.DATABASE_AUTH:
                conn = DatabaseAuthConnection(eis=eis)
            elif eis.eis_type == ConnectionType.HTTP_JWT_AUTH:
                conn = HttpJwtAuthConnection(eis=eis)
            self.__cached_connections[eis.id] = conn
        return self.__cached_connections[eis.id]
