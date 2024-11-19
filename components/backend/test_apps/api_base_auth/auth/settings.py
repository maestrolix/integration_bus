from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BASIC_AUTH_USERNAME: str = 'user'
    BASIC_AUTH_PASSWORD: str = 'password'

    class Config:
        env_file = '.env'
