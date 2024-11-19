from dataclasses import dataclass

from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy import select, insert, update, delete, exists

from integration_bus.application import entities, dto
from integration_bus.application.interfaces import IEisRepository

from typing import Optional

from integration_bus.application.util.enum import EisKind, EIS_TYPES


@dataclass
class EisRepository(IEisRepository):
    async_session_maker: async_sessionmaker

    async def get_eis_list(self) -> list[entities.Eis]:
        query = select(entities.Eis)
        async with self.async_session_maker() as session:
            res = await session.execute(query)

        return res.scalars().all()

    async def get_eis_by_id(self, id_: int) -> Optional[entities.Eis]:
        query = select(entities.Eis) \
            .where(entities.Eis.id == id_)

        async with self.async_session_maker() as session:
            res = await session.execute(query)

        return res.scalar()

    async def check_if_exists_by_id(self, id_: int) -> bool:
        subquery = (
            select(entities.Eis).where(entities.Eis.id == id_)
        ).exists()
        async with self.async_session_maker() as session:
            res = await session.scalar(select(entities.Eis).where(subquery))
        return res

    async def add_eis(self, eis: dto.eis.ReqCreate) -> int:
        query = insert(entities.Eis).values(eis.model_dump()).returning(entities.Eis.id)

        async with self.async_session_maker() as session:
            res = await session.execute(query)
            await session.commit()

        return res.scalar()

    async def update_eis(self, eis: dto.eis.ReqUpdate):
        update_query = update(entities.Eis) \
            .values(eis.model_dump(exclude={'id'})) \
            .where(entities.Eis.id == eis.id)

        async with self.async_session_maker() as session:
            await session.execute(update_query)
            await session.commit()

    async def delete_eis(self, id_: int) -> Optional[int]:
        query = delete(entities.Eis) \
            .where(entities.Eis.id == id_) \
            .returning(entities.Eis.id)

        async with self.async_session_maker() as session:
            res = await session.execute(query)
            await session.commit()

        return res.scalar()

    async def get_eis_list_of_kind(self, kind: EisKind) -> list[str]:
        matching_types = EIS_TYPES[kind]
        query = select(entities.Eis.title).where(entities.Eis.eis_type.in_(matching_types))

        async with self.async_session_maker() as session:
            res = await session.execute(query)

        return res.scalars().all()
