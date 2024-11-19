from dataclasses import dataclass

from sqlalchemy import select, Column, Integer, Boolean, String, table, ForeignKey

from integration_bus.application.interfaces.connection import IDatabaseConnection, IHttpConnection
from integration_bus.application.util.collector import RunnerCollector


# TODO: убрать этот класс, когда будет первый реальный раннер

@RunnerCollector.collect(key='test_runner')
@dataclass
class DatabaseAuthToHttpNoAuthExample:
    conn_from: IDatabaseConnection
    conn_to: IHttpConnection

    __pet_table = table(
        'pet',
        Column('id', Integer(), nullable=False, primary_key=True, autoincrement=True),
        Column('name', String(length=128), nullable=False),
        Column('age', Integer(), nullable=False),
        Column('gender', Boolean(), nullable=False),
        Column('animal', String(length=128), nullable=False),
        Column('owner_id', ForeignKey('person.id'), nullable=False),
    )

    async def run(self):
        print('Вызов раннера Database -> HTTP No Auth')
        print('  => Производится запрос.')
        async with self.conn_from.session_maker() as session:
            res = await session.execute(select(self.__pet_table))
            res = res.all()
        print('  => Получен ответ:', res)
        print('  => Данные отправляются.')
        status, body = await self.conn_to.post('/person', body={
            'name': 'TEST',
            'gender': False,
            'age': 30
        })
        print('  => Получен ответ:', status, body)
