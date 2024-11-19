from pydantic_settings import BaseSettings
from pythonjsonlogger.jsonlogger import JsonFormatter

from ssd_libs.logging_formatter import ColorizedFormatter


class Settings(BaseSettings):
    LOGGING_LEVEL: str = 'INFO'
    LOGGING_JSON: bool = False

    @property
    def LOGGING_CONFIG(self):
        fmt = '%(asctime)s [%(levelname)s] | [%(name)s]: %(message)s'
        datefmt = '%Y-%m-%d %H:%M:%S'

        config = {
            'version': 1,
            'disable_existing_loggers': True,
            'formatters': {
                'json': {
                    '()': lambda: JsonFormatter(fmt, datefmt, json_ensure_ascii=False)
                },
                'colorized': {
                    '()': lambda: ColorizedFormatter(fmt)
                }
            },
            'handlers': {
                'default': {
                    'level': self.LOGGING_LEVEL,
                    'formatter': 'json' if self.LOGGING_JSON else 'colorized',
                    'class': 'logging.StreamHandler',
                    'stream': 'ext://sys.stdout',
                },
            },
            'loggers': {
                '': {
                    'handlers': ['default'],
                    'level': self.LOGGING_LEVEL,
                    'propagate': False
                },
            }
        }

        return config

    class Config:
        extra = 'ignore'
        env_file = '.env'
        env_file_encoding = 'utf-8'
