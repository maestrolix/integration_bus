import inspect
from dataclasses import dataclass

from integration_bus.application import entities
from integration_bus.application.errors import CyclicDependency, DependencyNotFound
from integration_bus.application.interfaces import IRunnerRepository
from integration_bus.application.interfaces.connection import IDatabaseConnection, IHttpConnection
from integration_bus.application.util.collector import RunnerCollector, RunnerData
from integration_bus.application.util.enum import EisKind, VisitedState


@dataclass
class DependencyValidationService(): 
    runner_repo: IRunnerRepository

    __runner_collector = RunnerCollector()
    
    
    async def validate_runner_connection_types(self, db_runner: entities.Runner, runner_data: RunnerData):
        """
        Проверяет типы соединений раннеров на соответствие данным из БД.

        1) Если поля аннотированы неверно или не аннотированы вообще, поднимается исключение.
        2) Если аннотация, которой помечено соединение, не сответствует полю `eis_[from,to]_kind` в БД,
        то запись в БД обновляется.
        """
        # получить словарь вида { 'название_поля': тип }
        annotated_cls_fields = dict(inspect.getmembers(runner_data.cls))['__annotations__']
        conn_from_cls = annotated_cls_fields.get('conn_from')
        conn_to_cls = annotated_cls_fields.get('conn_to')

        # проверить conn_from
        if conn_from_cls == IHttpConnection:
            if db_runner.eis_from_kind != EisKind.HTTP:
                await self.runner_repo.update_runner_eis_from_kind(db_runner.id, EisKind.HTTP)
        elif conn_from_cls == IDatabaseConnection:
            if db_runner.eis_from_kind != EisKind.DATABASE:
                await self.runner_repo.update_runner_eis_from_kind(db_runner.id, EisKind.DATABASE)
        else:
            raise Exception(
                'The `conn_from` must be declared and have a type of one of the abstract connection classes')

        # проверить conn_to
        if conn_to_cls == IHttpConnection:
            if db_runner.eis_to_kind != EisKind.HTTP:
                await self.runner_repo.update_runner_eis_to_kind(db_runner.id, EisKind.HTTP)
        elif conn_to_cls == IDatabaseConnection:
            if db_runner.eis_to_kind != EisKind.DATABASE:
                await self.runner_repo.update_runner_eis_to_kind(db_runner.id, EisKind.DATABASE)
        else:
            raise Exception('The `conn_to` must be declared and have a type of one of the abstract connection classes')

    async def check_for_cyclic_dependencies(self, main_runner: entities.Runner):
        """
        Проверяет, что у раннера в графе зависимостей нет циклов (нет циклических зависимостей).
        """
        tmp_runner_set: list[entities.Runner] = []

        async def init_set(runner: entities.Runner):
            """ Обходит граф зависимостей раннера и записывает раннеры в множество. """
            if any(runner.id == e.id for e in tmp_runner_set):
                return
            tmp_runner_set.append(runner)
            for dep in runner.dependencies:
                db_dep = await self.runner_repo.get_runner_by_id(dep.id)
                await init_set(db_dep)

        await init_set(main_runner)

        dependency_graph: dict[int, list[int]] = {}

        for runner in tmp_runner_set:
            dependency_graph[runner.id] = []
            for dep in runner.dependencies:
                dependency_graph[runner.id].append(dep.id)

        # Алгоритм DFS O(V + E)
        # Обход графа зависимостей в глубину и выявление циклов.

        visited = {k: VisitedState.NOT_VISITED for k in dependency_graph.keys()}
        detected_cycles: list[list[int]] = []

        def register_cycle(stack: list[int], v: int):
            cycle: list[int] = [stack.pop()]
            while cycle[-1] != v:
                cycle.append(stack.pop())
            cycle.reverse()
            if cycle not in detected_cycles:
                cycle.append(cycle[0])
                detected_cycles.append(cycle)

        def dfs(stack: list[int]):
            for v in dependency_graph[stack[-1]]:
                if visited[v] == VisitedState.IN_STACK:
                    register_cycle(stack.copy(), v)
                elif visited[v] == VisitedState.NOT_VISITED:
                    stack.append(v)
                    visited[v] = VisitedState.IN_STACK
                    dfs(stack)
            visited[stack.pop()] = VisitedState.NOT_VISITED

        for v in dependency_graph.keys():
            if visited[v] == VisitedState.NOT_VISITED:
                stack: list[int] = [v]
                visited[v] = VisitedState.VISITED
                dfs(stack)

        if len(detected_cycles) != 0:
            raise CyclicDependency(detected_cycles)

    async def validate_runner_info(self):
        # TODO: подумать, как оптимизировать логику
        all_runners = self.__runner_collector.get_all()

        registered_runner_keys = await self.runner_repo.get_runners_key_list()
        for runner_key, runner_data in all_runners.items():
            if runner_key not in registered_runner_keys:
                runner = entities.Runner(key=runner_key)
                await self.runner_repo.add_runner(runner)
                await self.validate_runner_connection_types(runner, runner_data)

        for runner_key, runner_data in all_runners.items():
            db_runner = await self.runner_repo.get_runner_by_key(runner_key)
            db_deps = [runner.key for runner in db_runner.dependencies]
            declared_deps = runner_data.args.dependencies

            if db_deps != declared_deps:
                new_dependency_ids = []
                for declared_key in declared_deps:
                    db_dependency = await self.runner_repo.get_runner_by_key(declared_key)
                    if db_dependency is None:
                        raise DependencyNotFound(db_runner.key, declared_key)
                    new_dependency_ids.append(db_dependency.id)
                await self.runner_repo.update_runner_dependencies(db_runner.id, new_dependency_ids)

        for runner_key, runner_data in all_runners.items():
            db_runner = await self.runner_repo.get_runner_by_key(runner_key)
            await self.check_for_cyclic_dependencies(db_runner)
