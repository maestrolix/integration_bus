from dataclasses import dataclass
from sqlalchemy import insert, Column, Integer, Boolean, String, table, ForeignKey

from integration_bus.application.interfaces.connection import IHttpConnection, IDatabaseConnection
from integration_bus.application.util.collector import RunnerCollector


# TODO: убрать этот класс, когда будет первый реальный раннер

@RunnerCollector.collect(key='second_test_runner', dependencies=['test_runner'])
@dataclass
class HttpBasicAuthToDatabaseAuthExample:
    conn_from: IHttpConnection
    conn_to: IDatabaseConnection

    __person_table = table(
        'person',
        Column('id', Integer(), nullable=False, primary_key=True, autoincrement=True),
        Column('name', String(length=256), nullable=False),
        Column('gender', Boolean(), nullable=False),
        Column('age', Integer(), nullable=False),
    )

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
        print('Вызов раннера HTTP Basic Auth -> Database')
        print('  => Производится запрос.')
        status, body = await self.conn_from.get('/album')
        print('  => Получен ответ:', status, body)
        print('  => Данные отправляются.')
        async with self.conn_to.session_maker() as session:
            new_person = {
                'name': 'TEST',
                'gender': True,
                'age': 24
            }
            query = insert(self.__person_table).values(new_person).returning(self.__person_table.c.id)
            new_id = await session.scalar(query)
            new_pet = {
                'name': 'TEST',
                'age': 2,
                'gender': True,
                'animal': 'cat',
                'owner_id': new_id
            }
            query = insert(self.__pet_table).values(new_pet).returning(self.__pet_table.c.id)
            new_pet_id = await session.scalar(query)
            await session.commit()
        print('  => Получен ответ:', new_pet_id)
