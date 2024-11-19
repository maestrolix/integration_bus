from typing import Any, Optional
from dataclasses import dataclass

import aiohttp
import urllib.parse

from integration_bus.application.interfaces.connection import IHttpConnection
from integration_bus.application import entities


@dataclass
class HttpJwtAuthConnection(IHttpConnection):
    """ Соединение с HTTP API с JWT аутентификацией. """
    eis: entities.Eis
    __cached_jwt: Optional[str] = None

    async def post(
            self,
            uri_to: str,
            body: Optional[dict[str, Any]] = None,
            query_params: Optional[dict[str, Any]] = None,
            path_params: Optional[dict[str, Any]] = None
    ) -> tuple[int, Any]:
        async with aiohttp.ClientSession() as session:
            endpoint = self.__build_endpoint(path_params, uri_to)
            url = urllib.parse.urljoin(self.base_url, endpoint)

            if self.__cached_jwt is None:
                self.__cached_jwt = await self.__refresh_jwt(session)
            resp = await session.post(url, json=body, params=query_params, headers=self.auth_header)
            if resp.status == 401:
                self.__cached_jwt = await self.__refresh_jwt(session)
                resp = await session.post(url, json=body, params=query_params, headers=self.auth_header)
            return resp.status, await resp.json()

    async def get(
            self,
            uri_to: str,
            body: Optional[dict[str, Any]] = None,
            query_params: Optional[dict[str, Any]] = None,
            path_params: Optional[dict[str, Any]] = None
    ) -> tuple[int, Any]:
        async with aiohttp.ClientSession() as session:
            endpoint = self.__build_endpoint(path_params, uri_to)
            url = urllib.parse.urljoin(self.base_url, endpoint)

            if self.__cached_jwt is None:
                self.__cached_jwt = await self.__refresh_jwt(session)
            resp = await session.get(url, json=body, params=query_params, headers=self.auth_header)
            if resp.status == 401:
                self.__cached_jwt = await self.__refresh_jwt(session)
                resp = await session.get(url, json=body, params=query_params, headers=self.auth_header)
            return resp.status, await resp.json()

    def __build_endpoint(self, path_params: Optional[dict[str, Any]], uri_to: str) -> str:
        if path_params is not None:
            return uri_to.format(**path_params)
        else:
            return uri_to

    async def __refresh_jwt(self, session: aiohttp.ClientSession):
        auth_data = {'username': self.eis.username, 'password': self.eis.password}
        resp = await session.post(urllib.parse.urljoin(self.base_url, self.eis.auth_endpoint), data=auth_data)
        return (await resp.json()).get('token')

    @property
    def auth_header(self) -> dict[str, str]:
        return {'Authorization': 'Bearer ' + self.__cached_jwt}

    @property
    def base_url(self) -> str:
        domain = ('https://' if self.eis.https else 'http://') + self.eis.host
        if self.eis.port:
            domain += ':' + str(self.eis.port)
        return domain
