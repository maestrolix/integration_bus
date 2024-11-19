from attr import dataclass
from sqlalchemy import column, insert, select, table

from integration_bus.application.interfaces.connection import IDatabaseConnection
from integration_bus.application.util.collector import RunnerCollector

"""
CREATE TABLE public.cats (
	id serial4 NOT NULL,
	title varchar NOT NULL,
	CONSTRAINT cats_pk PRIMARY KEY (id)
);
"""


@RunnerCollector.collect('test_1')
@dataclass
class DBToDBExample:
    conn_from: IDatabaseConnection
    conn_to: IDatabaseConnection

    async def run(self):
        select_query = select(table('cats', column('title')))

        async with self.conn_from.session_maker() as session:
            _res = await session.execute(select_query)
        _res = _res.mappings().all()

        insert_query = insert(table('cats', column('title'))).values(*_res)
        async with self.conn_to.session_maker() as session:
            await session.execute(insert_query)
            await session.commit()
