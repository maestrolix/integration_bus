from asyncio import AbstractEventLoop, Future
from abc import abstractmethod

from .base_task import IBaseTask


class IAsyncTask(IBaseTask):

    @abstractmethod
    def _run(self, event_loop: AbstractEventLoop) -> Future:
        """ """
        raise NotImplementedError
