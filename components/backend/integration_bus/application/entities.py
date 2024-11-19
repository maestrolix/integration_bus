from datetime import datetime
from typing import Optional

from attr import dataclass

from integration_bus.application.util.enum import RunnerStatus, EisKind, EisType


@dataclass
class Eis:
    id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    host: Optional[str] = None
    port: Optional[int] = None
    https: Optional[bool] = None
    username: Optional[str] = None
    password: Optional[str] = None
    auth_endpoint: Optional[str] = None
    db_name: Optional[str] = None
    db_type: Optional[str] = None
    eis_type: Optional[EisType] = None


@dataclass
class Runner:
    id: Optional[int] = None
    key: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    eis_from: Optional[Eis] = None
    eis_to: Optional[Eis] = None
    launch_time: Optional[str] = None
    blocked: bool = False
    test_mode: bool = False
    push_notification: bool = False
    status: str = RunnerStatus.READY
    mock_dataset: list['MockData'] = list()
    dependencies: list['Runner'] = list()  # раннеры, от которых зависит данный
    dependants: list['Runner'] = list()  # раннеры, которые зависят от данного
    eis_from_kind: Optional[EisKind] = None
    eis_to_kind: Optional[EisKind] = None


@dataclass
class RunnerDependency:
    runner_id: Optional[int] = None
    dependency_runner_id: Optional[int] = None


@dataclass
class MockData:
    id: Optional[int] = None
    runner: Optional[Runner] = None
    title: Optional[str] = None
    file_uri: Optional[str] = None
    is_main: bool = False


@dataclass
class RunnerExecutionRequest: 
    id: Optional[int] = None
    status: Optional[str] = None
    total_time_execution: Optional[float] = None
    created_at: Optional[datetime] = None


@dataclass
class RunnerEvent:
    id: Optional[int] = None
    runner_id: Optional[int] = None
    runner: Optional[Runner] = None
    request_id: Optional[int] = None
    status: Optional[str] = None
    created_at: Optional[datetime] = None
    
@dataclass
class RunnerLog: 
    id: Optional[int] = None
    event_id: Optional[int] = None
    status: Optional[str] = None
    type: Optional[str] = None
    text: Optional[str] = None
    created_at: Optional[datetime] = None