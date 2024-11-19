from abc import abstractmethod
from .base_task import IBaseTask


class ISyncTask(IBaseTask):

    @abstractmethod
    def _run(self) -> None:
        """ """
        raise NotImplementedError
