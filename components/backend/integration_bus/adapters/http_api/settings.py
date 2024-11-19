from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_IS_DEBUG: bool = False
    APP_VERSION: str = '0.0.1'
    APP_SWAGGER_ON: bool = True
    APP_TITLE: str = 'noname'
    APP_LOGGING_LEVEL: str = 'INFO'

    
    @property
    def LOGGING_CONFIG(self):
        return {
            'loggers': {
                'gunicorn': {
                    'handlers': ['default'],
                    'level': self.APP_LOGGING_LEVEL,
                    'propagate': False
                },
                'uvicorn': {
                    'handlers': ['default'],
                    'level': self.APP_LOGGING_LEVEL,
                    'propagate': False
                },
            }
        }

    class Config:
        extra = 'ignore'
        env_file = '.env'
        env_file_encoding = 'utf-8'
    
    