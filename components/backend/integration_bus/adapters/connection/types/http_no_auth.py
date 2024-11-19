from typing import Any, Optional
from dataclasses import dataclass

from integration_bus.application.interfaces.connection import IHttpConnection
from integration_bus.application import entities

import aiohttp
import urllib.parse


@dataclass
class HttpNoAuthConnection(IHttpConnection):
    """ Соединение с HTTP API без аутентификации. """
    eis: entities.Eis

    async def post(
            self,
            uri_to: str,
            body: Optional[dict[str, Any]] = None,
            query_params: Optional[dict[str, Any]] = None,
            path_params: Optional[dict[str, Any]] = None
    ) -> tuple[int, Any]:
        async with aiohttp.ClientSession() as session:
            if path_params is not None:
                endpoint = uri_to.format(**path_params)
            else:
                endpoint = uri_to

            url = urllib.parse.urljoin(self.base_url, endpoint)

            resp = await session.post(url, json=body, params=query_params)
            return resp.status, await resp.json()

    async def get(
            self,
            uri_to: str,
            body: Optional[dict[str, Any]] = None,
            query_params: Optional[dict[str, Any]] = None,
            path_params: Optional[dict[str, Any]] = None
    ) -> tuple[int, Any]:
        async with aiohttp.ClientSession() as session:
            if path_params is not None:
                endpoint = uri_to.format(**path_params)
            else:
                endpoint = uri_to

            url = urllib.parse.urljoin(self.base_url, endpoint)

            resp = await session.get(url, json=body, params=query_params)
            return resp.status, await resp.json()

    @property
    def base_url(self) -> str:
        domain = ('https://' if self.eis.https else 'http://') + self.eis.host
        if self.eis.port:
            domain += ':' + str(self.eis.port)
        return domain
