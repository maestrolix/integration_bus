from datetime import datetime, timezone

from ._base_task import BaseTask
from ..interfaces import ISyncTask


class SyncTask(BaseTask, ISyncTask):

    def _run(self) -> None:
        self._logger.info(f'Задача - [{self._name}]. UUID - [{self._instance_key}]. CRON -> [{self._cron}]')

        self._last_started_at = datetime.now(timezone.utc)
        try:
            self._job(*self._job_args, **self._job_kwargs)
        except Exception as e:
            self._logger.error(f'Задача завершилась с ошибкой. UUID - [{self._instance_key}]. \n{e}')
        else:
            self._logger.info(f'Задача завершилась. UUID - [{self._instance_key}]')

        self._on_finish()
