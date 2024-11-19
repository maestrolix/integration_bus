import logging
from datetime import datetime, timezone
from typing import Callable
from uuid import uuid4

from croniter import croniter

from ..interfaces import IBaseTask


class BaseTask(IBaseTask):

    def __init__(
            self,
            name: str,
            cron: str,
            job: Callable,
            job_args: tuple | None = None,
            job_kwargs: dict | None = None,
            *,
            is_overdue_gap_needed: bool = True

    ) -> None:
        self._name = name
        self._instance_key = uuid4()
        self._job = job

        self._job_args = job_args or ()
        self._job_kwargs = job_kwargs or {}
        self._cron = cron

        self._croniter = self._create_calendar()
        self._is_overdue_gap_needed = is_overdue_gap_needed

        self._next_run = self._croniter.get_next(datetime)
        self._last_started_at = None

        self._logger = logging.getLogger('scheduler')

    def get_name(self) -> str:
        return self._name

    def get_job(self) -> Callable:
        return self._job

    def get_uniq_name(self) -> str:
        return f'{self._name}_{self._instance_key}'
    

    def get_next_run_datepoint(self) -> datetime:
        return self._next_run

    def _on_finish(self):
        finished_at = datetime.now(timezone.utc)

        optimistic_next_run = self._croniter.get_next(
            datetime,
            self._croniter.get_current(),
        )

        is_overdue = finished_at >= optimistic_next_run
        if not is_overdue:
            self._next_run = optimistic_next_run

        if is_overdue and self._is_overdue_gap_needed:
            self._croniter.set_current(finished_at)
            self._next_run = self._croniter.get_next(datetime)

        if is_overdue and not self._is_overdue_gap_needed:
            self._croniter.set_current(finished_at)
            self._next_run = finished_at

    def _create_calendar(self) -> croniter:
        assert croniter.is_valid(self._cron), 'Некорректный синтаксис cron'
        return croniter(self._cron, datetime.now(timezone.utc))
