import asyncio
from datetime import datetime, timezone

from ..interfaces import IAsyncTask
from ._base_task import BaseTask


class AsyncTask(BaseTask, IAsyncTask):

    def _run(self, event_loop: asyncio.AbstractEventLoop) -> asyncio.Future:
        self._logger.info(f'Задача - [{self._name}]. UUID - [{self._instance_key}]. CRON -> [{self._cron}]')

        _future: asyncio.Future = None
        self._last_started_at = datetime.now(timezone.utc)

        try:
            _future = asyncio.run_coroutine_threadsafe(self._job(*self._job_args, **self._job_kwargs), event_loop)
        except Exception as e:
            self._logger.error(f'Задача не запустилась. UUID - [{self._instance_key}]. \n{e}')

        self._on_finish()
        return _future
