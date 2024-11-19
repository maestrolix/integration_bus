from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    TEST_API_PORT: int = 3000
    TEST_API_HOST: str = 'localhost'

    class Config:
        env_file = '.env'
