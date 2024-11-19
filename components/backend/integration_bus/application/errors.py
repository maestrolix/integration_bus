class DependencyNotFound(Exception):
    """
    Исключение, выбрасывающееся, если раннер, который был указан в качестве
    зависимости другого раннера, не был найден.
    """
    def __init__(self, runner: str, dependency: str):
        super().__init__(f'The runner {runner} has unknown dependency {dependency}.')


class CyclicDependency(Exception):
    """
    Исключение, выбрасывающееся, если в графе зависимостей раннера
    обнаруживается хотя бы один цикл.
    """
    def __init__(self, cycles: list[list[int]]):
        cycle_strs = [' -> '.join(str(id_) for id_ in cycle) for cycle in cycles]
        super().__init__(f'Found cycle(s) in the runners\' dependency graphs: {", ".join(cycle_strs)}.')
