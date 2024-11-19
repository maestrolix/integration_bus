from datetime import datetime
from typing import Optional

from attr import dataclass
from sqlalchemy import insert, update
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from integration_bus.application import entities, interfaces
from integration_bus.application.util import enum


@dataclass
class Logger(interfaces.ILogger): 
    async_session_maker: async_sessionmaker[AsyncSession]
    
    def set_sessionmaker(self, async_session_maker: async_sessionmaker[AsyncSession]) -> None: 
        """ Устанавливает генератор сессий для логированя. """
        self.async_session_maker = async_session_maker
            
    async def create_execution_request(
        self,
        created_at: datetime, 
        status: enum.RunnerExecutionRequestStatus
    ) -> entities.RunnerExecutionRequest:
        """ """
        query = insert(
            entities.RunnerExecutionRequest
        ).values(
            status=status, 
            created_at=created_at
        ).returning(
            entities.RunnerExecutionRequest
        )
        
        async with self.async_session_maker() as session: 
            _res = await session.execute(query)
            await session.commit()
            
        return _res.scalar()
        
    async def update_execution_request(
        self, 
        id: int,
        total_time_execution: float, 
        status: enum.RunnerExecutionRequestStatus
    ) -> entities.RunnerExecutionRequest: 
        """ """
        query = update(
            entities.RunnerExecutionRequest
        ).where(
            entities.RunnerExecutionRequest.id == id
        ).values(
            status=status,
            total_time_execution=round(total_time_execution, 5)
        ).returning(
            entities.RunnerExecutionRequest
        )
        
        async with self.async_session_maker() as session: 
            _res = await session.execute(query)
            await session.commit()
        
        return _res.scalar()
    
    async def create_runner_events(
        self,
        events: list[entities.RunnerEvent]
    ) -> list[entities.RunnerEvent]: 
        """ """
        events_db = []
        async with self.async_session_maker() as session: 
            for event in events: 
                query = insert(
                    entities.RunnerEvent
                ).values(
                    runner_id=event.runner_id, 
                    request_id=event.request_id, 
                    status=event.status,
                    created_at=event.created_at
                ).returning(
                    entities.RunnerEvent
                )
                _res = await session.execute(query)
                events_db.append(_res.scalar())
            await session.commit()
                
        return events_db
    
    async def update_runner_event(
        self, 
        id: int,
        status: enum.RunnerEventStatus, 
        time_execution_runner: Optional[float] = None,
    ) -> None: 
        query = update(
            entities.RunnerEvent
        ).where(
            entities.RunnerEvent.id == id
        ).values(
            status=status, 
            time_execution_runner=time_execution_runner
        )
        
        async with self.async_session_maker() as session: 
            await session.execute(query)
            await session.commit()
            
    async def create_runner_log(
        self,
        event_id: int,
        text: str, 
        type: enum.RunnerLogType,
        status: enum.RunnerLogStatus,
    ) -> None: 
        """ """
        created_at = datetime.now()
        
        query = insert(
            entities.RunnerLog
        ).values(
            event_id=event_id, text=text,
            type=type, status=status,
            created_at=created_at
        )
        
        async with self.async_session_maker() as session: 
            await session.execute(query)
            await session.commit()
         