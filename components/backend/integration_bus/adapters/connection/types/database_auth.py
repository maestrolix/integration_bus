from enum import StrEnum, auto

from integration_bus.application.interfaces.connection import IDatabaseConnection
from integration_bus.application import entities
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine


class DatabaseVendor(StrEnum):
    POSTGRESQL = auto()
    ORACLE = auto()


class DatabaseAuthConnection(IDatabaseConnection):
    """ Соединение с базой данных. """
    __async_session_maker: async_sessionmaker

    def __init__(self, eis: entities.Eis):
        self.eis = eis
        engine = create_async_engine(self.base_url)
        self.__async_session_maker = async_sessionmaker(bind=engine)

    @property
    def session_maker(self) -> async_sessionmaker:
        return self.__async_session_maker

    @property
    def base_url(self) -> str:
        if self.eis.db_type == DatabaseVendor.POSTGRESQL:
            db_driver = '+' + 'asyncpg'
        elif self.eis.db_type == DatabaseVendor.ORACLE:
            db_driver = '+' + 'cx_oracle'
        else:
            db_driver = ''

        return '{db_type}{db_driver}://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'.format(
            db_type=self.eis.db_type,
            db_driver=db_driver,
            db_user=self.eis.username,
            db_pass=self.eis.password,
            db_host=self.eis.host.rstrip('/'),
            db_port=self.eis.port,
            db_name=self.eis.db_name,
        )
