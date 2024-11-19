from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class RunnerArgs:
    key: str
    dependencies: list[str]


@dataclass
class RunnerData:
    cls: type[Any]
    args: RunnerArgs


class RunnerCollector:
    __runners: dict[str, RunnerData] = {}

    @classmethod
    def collect(cls, key: str, dependencies: Optional[list[str]] = None):
        """
        Сообщает роутеру о раннере, связывая его ключ с Python классом
        и некоторой дополнительной информацией (аргументами).
        Декоратор создан как альтернатива динамической загрузке класса во время исполнения.
        """
        if key in cls.__runners:
            raise ValueError('раннер с таким ключом уже был добавлен')

        def __mark(original_cls):
            cls.__runners[key] = RunnerData(
                cls=original_cls,
                args=RunnerArgs(
                    key,
                    dependencies if dependencies is not None else []
                )
            )
            return original_cls

        return __mark

    def get(self, key: str) -> Optional[RunnerData]:
        return self.__runners.get(key)

    def get_all(self) -> dict[str, RunnerData]:
        return self.__runners
