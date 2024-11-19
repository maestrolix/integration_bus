from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BASIC_AUTH_USERNAME: str = 'user'
    BASIC_AUTH_PASSWORD: str = 'password'

    class Config:
        env_file = '../.env'


basic_auth = HTTPBasic()
settings = Settings()


def check_credentials(creds: HTTPBasicCredentials) -> bool:
    return creds.username == settings.BASIC_AUTH_USERNAME \
        and creds.password == settings.BASIC_AUTH_PASSWORD
