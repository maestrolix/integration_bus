import asyncio
import heapq
import logging
import signal
import threading
import time
import traceback
from concurrent.futures import Future, ThreadPoolExecutor
from datetime import datetime, timezone
from multiprocessing import cpu_count
from queue import Queue
from typing import Callable
from uuid import UUID

from .tasks.async_task import AsyncTask
from .tasks.sync_task import SyncTask


class Scheduler:
    """ Динамический планировщик для исполнения синхронных и асинхронных задач.
    
    NOTE: Помните, что даже если функция исполнения одна, объекты задач должны быть разными.
    """
    _loop_delay: float = 0.01

    def __init__(
            self,
            async_tasks: list[AsyncTask] | None = None,
            sync_tasks: list[SyncTask] | None = None,
    ):
        self._logger = logging.getLogger('scheduler')
        
        self._stopped = False
        self._lock = threading.Lock()
        self._tasks_q: list[tuple[datetime, str, AsyncTask | SyncTask]] = []    
        
        self._futures_mapper: dict[int, Future] = {}
        self._executor: ThreadPoolExecutor | None = ThreadPoolExecutor(max_workers=cpu_count() // 2)
        self._sync_tasks: list[SyncTask] = sync_tasks if sync_tasks else []
        
        self._async_tasks: list[AsyncTask] = async_tasks if async_tasks else []
        self._async_futures_q: Queue[asyncio.Future] = Queue()
        self._async_event_loop: asyncio.AbstractEventLoop = asyncio.new_event_loop()
        self._async_event_loop_t: threading.Thread | None = None
        self._async_task_checker_t: threading.Thread | None = None
        
        if sync_tasks:
            self._prepare_tasks(*self._sync_tasks)
        if async_tasks: 
            self._prepare_tasks(*self._async_tasks)
        
        self.__register_sigterm_handler()
        
    def run(self):
        self._logger.info('Планировщик запущен!')
        
        self._run_async_helpers()
        while not self._stopped:
            try:
                self._run()
            except (KeyboardInterrupt, SystemExit):
                self.stop()
                continue
            except Exception as e:
                self._logger.exception(
                    'Unexpected error occurred, trying again \n[%s]',
                    e,
                )
                time.sleep(self._loop_delay)
                continue
 
    def stop(self):
        self._logger.info('Остановка планировщика ...')
        self._stopped = True
        self._executor.shutdown(wait=True)
        self._async_event_loop.stop()
        self._logger.info('Остановка планировщика завершилась!')
        
    def add_tasks(self, tasks: list[SyncTask] | list[AsyncTask]) -> None:
        """ Добавляет новые задачи в планировщик. """
        if tasks:
            self._prepare_tasks(*tasks)
            self._logger.info(f'Задачи добавлены в планировщик в количестке [{len(tasks)}]!')
        else: 
            self._logger.info('Добавляемый список с задачами пуст ...')
 
    def delete_tasks_by_unique_name(self, names: list[str]) -> None: 
        """ Удаляет задачи из планировщика по их именам """
        with self._lock:
            for task, id in zip(self._tasks_q, range(len(self._tasks_q))): 
                for name in names:
                    if task[2].get_uniq_name() == name: 
                        self._tasks_q.pop(id)
        self._logger.info(f'Задачи были удалены в количестве [{len(names)}]')


    def _run_async_helpers(self): 
        """ Запускает вспомогательные потоки для выполнения асинхронных задач. """
        self._logger.debug('Запуск вспомогательных потоков для асинхронных задач ...')
        self._async_event_loop_t = threading.Thread(
            name='async_event_loop_t',
            target=self._start_event_loop,
            kwargs={'event_loop': self._async_event_loop},
            daemon=True,
        )
        self._async_task_checker_t = threading.Thread(
            name='async_task_checker_t',
            target=self._start_task_checker,
            kwargs={'async_futures_q': self._async_futures_q},
            daemon=True
        )
        self._async_event_loop_t.start()
        self._async_task_checker_t.start()
        
        self._logger.debug('Запуск успешен!')

    def _start_event_loop(self, event_loop: asyncio.AbstractEventLoop):
        """ Запуск цикла для выполнения асинхронных задач. """
        asyncio.set_event_loop(event_loop)
        event_loop.run_forever()

    def _start_task_checker(self, async_futures_q: Queue):
        """ Вспомогательный метод, для проверки статуса выполнения асинхронных задач """
        while True:
            message = async_futures_q.get()
            task: AsyncTask = message.get('task')
            future: asyncio.Future = message.get('future')
            exception = future.exception()

            if exception is not None:
                exception_formated = ''.join(traceback.TracebackException.from_exception(exception).format())
                self._logger.error(
                    f'Задача завершилась с ошибкой. UUID - [{task._instance_key}].\n {exception_formated}')
            else:
                self._logger.info(f'Задача завершилась. UUID - [{task._instance_key}]')


    def _run(self):
        while not self._stopped:
            if len(self._tasks_q) == 0:
                time.sleep(self._loop_delay)
                continue

            with self._lock:
                next_task = self._peak_nearest_task()
                next_run = next_task.get_next_run_datepoint()

                utcnow = datetime.now(timezone.utc)
                next_run_delay = (next_run - utcnow).total_seconds()
                if next_run_delay > 0:
                    time.sleep(self._loop_delay)
                    continue

                self._pop_nearest_task()
            self._run_task(next_task)

    def _peak_nearest_task(self) -> AsyncTask | SyncTask:
        return self._tasks_q[0][2]

    def _pop_nearest_task(self):
        heapq.heappop(self._tasks_q)

    def _push_task(self, task: AsyncTask | SyncTask):
        with self._lock:
            heapq.heappush(
                self._tasks_q, (
                    task.get_next_run_datepoint(),
                    task.get_uniq_name(),
                    task,
                )
            )

    def _prepare_tasks(self, *tasks: AsyncTask | SyncTask):
        for task in tasks:
            self._update_task_schedule(task)

    def _update_task_schedule(self, task: AsyncTask | SyncTask):
        self._push_task(task)

    def _on_task_done(self, future: Future):
        task = self._futures_mapper.pop(id(future))
        self._update_task_schedule(task)

    def _run_task(self, task: AsyncTask | SyncTask) -> None:
        if self._stopped:
            self._logger.info('Scheduler is stopped, cancel task')
            return

        if isinstance(task, AsyncTask):
            _future = task._run(self._async_event_loop)
            if _future:
                self._async_futures_q.put({'future': _future, 'task': task})
            self._update_task_schedule(task)

        if isinstance(task, SyncTask):
            _future = self._executor.submit(task._run)
            self._futures_mapper[id(_future)] = task
            _future.add_done_callback(self._on_task_done)


    def __register_sigterm_handler(self):
        def new_handler(*args, **kwargs):
            self.stop()
            if isinstance(old_handler, Callable):
                old_handler(*args, **kwargs)
        
        old_handler = signal.getsignal(signal.SIGTERM)
        signal.signal(signal.SIGTERM, new_handler)
