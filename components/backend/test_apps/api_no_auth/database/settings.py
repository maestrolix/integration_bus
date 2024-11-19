from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_HOST: str = 'no-auth-api-postgres'
    DATABASE_PORT: int = 5432
    DATABASE_USER: str = 'postgres'
    DATABASE_PASS: str = 'postgres'
    DATABASE_NAME: str = 'example_database'

    @property
    def DATABASE_URL(self) -> str:
        return 'postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'.format(
            db_user=self.DATABASE_USER,
            db_pass=self.DATABASE_PASS,
            db_host=self.DATABASE_HOST,
            db_port=self.DATABASE_PORT,
            db_name=self.DATABASE_NAME
        )

    class Config:
        env_file = '.env'
        extra = 'allow'
