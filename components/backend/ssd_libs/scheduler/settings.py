from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SCHEDULER_LOG_LEVEL: str = 'DEBUG'

    @property
    def LOGGING_CONFIG(self):
        return {
            'loggers': {
                'scheduler': {
                    'handlers': ['default'],
                    'level': self.SCHEDULER_LOG_LEVEL,
                    'propagate': False,
                }
            }
        }

    class Config:
        extra = 'ignore'
        env_file = '.env'
        env_file_encoding = 'utf-8'
