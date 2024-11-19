import inspect
from dataclasses import dataclass
from datetime import datetime
from enum import IntEnum, auto

from integration_bus.adapters.log import logger
from integration_bus.application import dto, entities
from integration_bus.application.errors import DependencyNotFound, CyclicDependency
from integration_bus.application.interfaces import IRunnerRepository
from integration_bus.application.interfaces.connection import (
    IConnectionManager,
    IDatabaseConnection,
    IHttpConnection,
)
from integration_bus.application.util import collector
from integration_bus.application.util.collector import RunnerCollector, RunnerData
from integration_bus.application.util.enum import (
    EisKind,
    RunnerEventStatus,
    RunnerExecutionRequestStatus,
    RunnerLogStatus,
    RunnerLogType,
    RunnerStatus,
)


@dataclass
class RouterService:
    connection_manager: IConnectionManager
    runner_repo: IRunnerRepository

    __runner_collector = collector.RunnerCollector()

    async def route(self, runner_key: str):
        created_at = datetime.now()
        req = await logger.create_execution_request(
            created_at=created_at,
            status=RunnerExecutionRequestStatus.IN_PROGRESS
        )

        runner = await self.runner_repo.get_runner_by_key(runner_key)
        if runner is None:
            req_status = RunnerExecutionRequestStatus.KEY_NOT_FOUND
        else:
            req_status = await self.try_execute_runners(runner, req.id)

        await logger.update_execution_request(
            id=req.id,
            status=req_status,
            total_time_execution=(datetime.now() - created_at).total_seconds(),
        )

    async def try_execute_runners(
            self,
            main_runner: entities.Runner,
            req_id: int
    ) -> RunnerExecutionRequestStatus:
        """ Метод-прослойка перед исполнением, который проверяет, возможно ли
        на данный момент выполнить те или иные раннеры, посредством проверки их
        блокировок. 
        
        Если все раннеры на данный момент свободны (считая зависимые)
        производится их блокировка и последующее исполнение.
        """
        final_status = RunnerExecutionRequestStatus.SUCCESS
        runners = await self.get_unique_runner_deps(main_runner)
        runners, is_updated = await self.runner_repo.try_update_runner_status(
            runners=runners,
            status=RunnerStatus.RUNNING,
            status_clause=RunnerStatus.READY
        )

        if is_updated:
            events = await self._create_running_events(req_id, runners)
            final_status = await self._execute_runners(runners, events)
        else:
            final_status = RunnerExecutionRequestStatus.BLOCKED
            await self._create_blocked_or_free_events(req_id, runners)

        await self.runner_repo.try_update_runner_status(
            runners=runners,
            status=RunnerStatus.READY,
            status_clause=RunnerStatus.RUNNING
        )
        return final_status

    async def _execute_runners(
            self,
            runners: list[entities.Runner],
            events: list[entities.RunnerEvent]
    ) -> RunnerExecutionRequestStatus:
        """ Основной исполняющий раннеры метод, который так же привязывает 
        результаты исполнения раннера к ивентам.
        
        """
        runners_exec = True
        final_status = RunnerExecutionRequestStatus.SUCCESS

        for runner, event in zip(runners, events):
            if runners_exec:
                start_time_exec = datetime.now()
                runner_completed = await self._execute_runner(runner, event.id)
                time_execution_runner = (datetime.now() - start_time_exec).total_seconds()

                if runner_completed:
                    await logger.update_runner_event(
                        id=event.id,
                        status=RunnerEventStatus.SUCCESS,
                        time_execution_runner=time_execution_runner
                    )
                else:
                    await logger.update_runner_event(
                        id=event.id,
                        status=RunnerEventStatus.ERROR,
                        time_execution_runner=None
                    )
                    final_status = RunnerExecutionRequestStatus.ERROR
                    runners_exec = False
            else:
                await logger.update_runner_event(
                    id=event.id,
                    status=RunnerEventStatus.NOT_EXEC,
                    time_execution_runner=None
                )
        return final_status

    async def _execute_runner(self, runner_info: entities.Runner, event_id: int) -> bool:
        runner_info = await self.runner_repo.get_runner_by_id(runner_info.id)
        try:
            conn_from = await self.connection_manager.create(runner_info.eis_from)
            conn_to = await self.connection_manager.create(runner_info.eis_to)
        except Exception as e:
            await logger.create_runner_log(
                event_id=event_id, text=str(e),
                type=RunnerLogType.CONNETION, status=RunnerLogStatus.ERROR
            )
            return False

        runner_data = self.__runner_collector.get(runner_info.key)
        runner_obj = runner_data.cls(
            conn_from=conn_from,
            conn_to=conn_to
        )

        try:
            await logger.create_runner_log(
                event_id=event_id, text="Раннер в исполнении...",
                type=RunnerLogType.RUNNER, status=RunnerLogStatus.INFO
            )
            await runner_obj.run()
            await logger.create_runner_log(
                event_id=event_id, text="Раннер успешно выполнился",
                type=RunnerLogType.RUNNER, status=RunnerLogStatus.INFO
            )
            return True
        except Exception as e:
            await logger.create_runner_log(
                event_id=event_id, text=str(e),
                type=RunnerLogType.RUNNER, status=RunnerLogStatus.ERROR
            )
            return False

    async def get_unique_runner_deps(
            self,
            main_runner: entities.Runner
    ) -> list[entities.Runner]:
        """
        Возвращает список с уникальными раннерами.

        Элементы возвращаются в виде последовательности, от самых зависимых раннеров к корневому.

        Вызов этого метода должен осуществляться только после проверки
        на отсутствие циклических зависимостей!
        """
        runner_list: list[entities.Runner] = []

        async def init_list(runner: entities.Runner):
            """
            Обходит граф зависимостей раннера и записывает все раннеры в список.

            Порядок элементов в списке будет соответствовать верному порядку вызова раннеров.
            """
            if runner in runner_list:
                return
            for dep in runner.dependencies:
                db_dep = await self.runner_repo.get_runner_by_id(dep.id)
                await init_list(db_dep)
                runner_list.append(runner)

        await init_list(main_runner)

        return runner_list

    # Логирование...

    async def _create_running_events(
            self,
            req_id: int,
            runners: list[entities.Runner],
    ) -> list[entities.RunnerEvent]:
        events = []
        created_at = datetime.now()
        for runner in runners:
            events.append(
                entities.RunnerEvent(
                    runner_id=runner.id,
                    request_id=req_id,
                    status=RunnerExecutionRequestStatus.IN_PROGRESS,
                    created_at=created_at
                )
            )
        return await logger.create_runner_events(events)

    async def _create_blocked_or_free_events(
            self,
            req_id: int,
            runners: list[entities.Runner],
    ):
        events = []
        created_at = datetime.now()
        for runner in runners:
            status = RunnerEventStatus.FREE if runner.status == RunnerStatus.READY else RunnerEventStatus.BLOCKED
            events.append(
                entities.RunnerEvent(
                    runner_id=runner.id,
                    request_id=req_id,
                    status=status,
                    created_at=created_at
                )
            )
        await logger.create_runner_events(events)
