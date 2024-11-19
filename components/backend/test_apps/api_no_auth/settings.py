from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    TEST_API_HOST: str = 'localhost'
    TEST_API_PORT: int = 3000

    class Config:
        env_file = '.env'
