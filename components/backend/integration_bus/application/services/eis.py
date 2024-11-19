from dataclasses import dataclass

from integration_bus.application import entities, interfaces, dto

from typing import Optional


@dataclass
class EisService:
    eis_repo: interfaces.IEisRepository

    async def get_eis_list(self) -> list[entities.Eis]:
        return await self.eis_repo.get_eis_list()

    async def get_eis_by_id(self, id_: int) -> Optional[entities.Eis]:
        return await self.eis_repo.get_eis_by_id(id_)

    async def add_eis(self, eis: dto.eis.ReqCreate) -> dto.eis.RespDetail:
        id_ = await self.eis_repo.add_eis(eis)
        return dto.eis.RespDetail(**eis.model_dump(), id=id_)

    async def update_eis(self, eis: dto.eis.ReqUpdate) -> Optional[entities.Eis]:
        if not await self.eis_repo.check_if_exists_by_id(eis.id):
            return None
        await self.eis_repo.update_eis(eis)
        db_eis = await self.eis_repo.get_eis_by_id(eis.id)
        return db_eis

    async def delete_eis(self, id_: int) -> Optional[int]:
        return await self.eis_repo.delete_eis(id_)
