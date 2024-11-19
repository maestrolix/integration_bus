from abc import ABC, abstractmethod
from datetime import datetime

from croniter import croniter


class IBaseTask(ABC):

    @abstractmethod
    def get_name(self) -> str:
        """ """
        raise NotImplementedError

    @abstractmethod
    def get_job(self) -> callable:
        """ """
        raise NotImplementedError

    @abstractmethod
    def get_uniq_name(self) -> str:
        """ """
        raise NotImplementedError

    @abstractmethod
    def get_next_run_datepoint(self) -> datetime:
        """ """
        raise NotImplementedError

    @abstractmethod
    def _on_finish(self):
        """ """
        raise NotImplementedError

    @abstractmethod
    def _create_calendar(self) -> croniter:
        """ """
        raise NotImplementedError
