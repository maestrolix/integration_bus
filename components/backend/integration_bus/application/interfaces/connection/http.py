from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, Any


@dataclass
class IHttpConnection(ABC):
    """ Интерфейс HTTP-соединения. """
    @abstractmethod
    async def post(
            self,
            uri_to: str,
            body: Optional[dict[str, Any]] = None,
            query_params: Optional[dict[str, Any]] = None,
            path_params: Optional[dict[str, Any]] = None
    ) -> tuple[int, Any]:
        raise NotImplementedError

    @abstractmethod
    async def get(
            self,
            uri_to: str,
            body: Optional[dict[str, Any]] = None,
            query_params: Optional[dict[str, Any]] = None,
            path_params: Optional[dict[str, Any]] = None
    ) -> tuple[int, Any]:
        raise NotImplementedError
