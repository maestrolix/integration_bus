from abc import ABC, abstractmethod

from integration_bus.application import entities
from integration_bus.application.util import enum
from datetime import datetime
from typing import Optional

class ILogger(ABC): 
    
    @abstractmethod
    async def create_execution_request(
        self,
        created_at: datetime, 
        status: enum.RunnerExecutionRequestStatus
    ) -> entities.RunnerExecutionRequest:
        """ """
        raise NotImplementedError
    
    @abstractmethod
    async def update_execution_request(
        self, 
        id: int,
        total_time_execution: float, 
        status: enum.RunnerExecutionRequestStatus
    ) -> entities.RunnerExecutionRequest: 
        """ """
        raise NotImplementedError
    
    @abstractmethod
    async def update_runner_event(
        self, 
        id: int,
        status: enum.RunnerEventStatus, 
        time_execution_runner: float,
    ) -> None: 
        """ """
        raise NotImplementedError