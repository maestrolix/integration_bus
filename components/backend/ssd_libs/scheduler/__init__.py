"""

    Библиотека планировщик, для запуска асинхронных и синхронных задач
    с помощью синтаксиса cron.

"""
from .scheduler import Scheduler
from .settings import Settings
from .tasks.async_task import AsyncTask
from .tasks.sync_task import SyncTask

__all__ = ['Scheduler', 'AsyncTask', 'SyncTask', 'Settings', 'global_scheduler']
__version__ = '1.0.0'


global_scheduler = Scheduler()