from .config import configure
from .logger import Logger
from .settings import Settings


__all__ = ['configure', 'Settings', 'logger']

logger = Logger(None)

