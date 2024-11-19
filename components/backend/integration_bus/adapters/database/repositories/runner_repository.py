from dataclasses import dataclass

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy import select, insert, update, delete, exists, func
from sqlalchemy.orm import joinedload

from integration_bus.application import entities, dto
from integration_bus.application.interfaces import IRunnerRepository

from typing import Optional

from integration_bus.application.util import enum
from integration_bus.application.util.enum import RunnerStatus, EisKind


@dataclass
class RunnerRepository(IRunnerRepository):
    async_session_maker: async_sessionmaker[AsyncSession]

    async def get_runners_list(self) -> list[entities.Runner]:
        query = select(entities.Runner)
        async with self.async_session_maker() as session:
            res = await session.execute(query)
        return res.scalars().all()

    async def get_runners_key_list(self) -> list[str]:
        query = select(entities.Runner.key)
        async with self.async_session_maker() as session:
            res = await session.execute(query)
        return res.scalars().all()

    async def get_runner_by_id(self, id_: int) -> Optional[entities.Runner]:
        query = select(entities.Runner) \
                .where(entities.Runner.id == id_)\
                .options(joinedload(entities.Runner.eis_from))\
                .options(joinedload(entities.Runner.eis_to))\
                .options(joinedload(entities.Runner.dependencies))

        async with self.async_session_maker() as session:
            res = await session.execute(query)
        return res.scalar()

    async def check_if_exists_by_id(self, id_: int) -> bool:
        subquery = (
            select(entities.Runner).where(entities.Runner.id == id_)
        ).exists()
        async with self.async_session_maker() as session:
            res = await session.scalar(select(entities.Runner).where(subquery))
        return res

    async def get_runner_by_key(self, key: str) -> Optional[entities.Runner]:
        query = select(entities.Runner)\
                .where(entities.Runner.key == key) \
                .options(joinedload(entities.Runner.eis_from)) \
                .options(joinedload(entities.Runner.eis_to)) \
                .options(joinedload(entities.Runner.dependencies))

        async with self.async_session_maker() as session:
            res = await session.execute(query)
        return res.scalar()

    async def add_runner(self, runner: entities.Runner):
        async with self.async_session_maker() as session:
            session.add(runner)
            await session.commit()

    async def update_runner(self, runner: dto.runner.ReqUpdate):
        update_query = update(entities.Runner) \
            .values(runner.model_dump(exclude={'id'})) \
            .where(entities.Runner.id == runner.id)

        async with self.async_session_maker() as session:
            await session.execute(update_query)
            await session.commit()

    async def update_runner_status(self, id_: int, status: RunnerStatus):
        update_query = update(entities.Runner) \
            .values({'status': status}) \
            .where(entities.Runner.id == id_)

        async with self.async_session_maker() as session:
            await session.execute(update_query)
            await session.commit()

    async def update_runner_eis_from_kind(self, id_: int, kind: EisKind):
        update_query = update(entities.Runner) \
            .values({'eis_from_kind': kind}) \
            .where(entities.Runner.id == id_)

        async with self.async_session_maker() as session:
            await session.execute(update_query)
            await session.commit()

    async def update_runner_eis_to_kind(self, id_: int, kind: EisKind):
        update_query = update(entities.Runner) \
            .values({'eis_to_kind': kind}) \
            .where(entities.Runner.id == id_)

        async with self.async_session_maker() as session:
            await session.execute(update_query)
            await session.commit()

    async def delete_runner(self, id_: int) -> Optional[int]:
        query = delete(entities.Runner)\
                .where(entities.Runner.id == id_)\
                .returning(entities.Runner.id)

        async with self.async_session_maker() as session:
            res = await session.execute(query)
            await session.commit()

        return res.scalar()

    async def update_runner_dependencies(self, id_: int, dependency_ids: list[int]):
        delete_query = delete(entities.RunnerDependency)\
            .where(entities.RunnerDependency.runner_id == id_)
        async with self.async_session_maker() as session:
            await session.execute(delete_query)
            if len(dependency_ids) != 0:
                insert_query = insert(entities.RunnerDependency)\
                    .values([
                        {'runner_id': id_, 'dependency_runner_id': dep_id} for dep_id in dependency_ids
                    ])
                await session.execute(insert_query)
            await session.commit()
            
            
    async def try_update_runner_status(
        self, 
        runners: list[entities.Runner], 
        status: enum.RunnerStatus, 
        status_clause: enum.RunnerStatus
    ) -> tuple[list[entities.Runner], bool]: 
        """ """
        runners_ids = [obj.id for obj in runners]
        
        runners_subquery = select(
            func.count(entities.Runner.id)
        ).where(
            entities.Runner.id.in_(runners_ids), 
            entities.Runner.status == status_clause
        ).scalar_subquery()
        
        update_query = update(
            entities.Runner
        ).where(
            len(runners) == runners_subquery, 
            entities.Runner.id.in_(runners_ids)
        ).values(
            {'status': status}
        ).returning(entities.Runner)
        
        query = select(entities.Runner).where(entities.Runner.id.in_(runners_ids))
        async with self.async_session_maker() as session: 
            async with session.begin(): 
                update_query = await session.execute(update_query)
                runners_db = await session.execute(query)
                await session.commit()

        runners_db = runners_db.scalars().all()
        len_updated = len(update_query.scalars().all())
        return runners_db, True if len_updated != 0 else False
