from typing import Final, Any


ADD_DATA: Final[list[dict[str, Any]]] = [
    {
        'title': 'Пятая тестовая ВИС',
        'description': None,
        'host': 'reg.ru',
        'port': 27017,
        'https': False,
        'username': 'admin',
        'password': '1234',
        'auth_endpoint': None,
        'db_name': 'example_database',
        'db_type': 'POSTGRES',
        'eis_type': 'DB'
    },
    {
        'title': 'Шестая тестовая ВИС',
        'description': 'Какое-то описание',
        'host': 'localhost',
        'port': 3000,
        'https': False,
        'username': 'mongo',
        'password': 'mongo',
        'auth_endpoint': None,
        'db_name': 'apartmentOwners',
        'db_type': 'MONGODB',
        'eis_type': 'DB'
    }
]

BAD_DATA: Final[list[dict[str, Any]]] = [
    {
        'title': None,
        'description': 'Какое-то описание',
        'host': None,
        'port': None,
        'https': None,
        'username': None,
        'password': None,
        'auth_endpoint': None,
        'db_name': None,
        'db_type': None,
        'eis_type': 'HTTP_NO_AUTH'
    },
    {
        'title': 'Несуществующая тестовая ВИС',
        'description': None,
        'host': None,
        'port': 'dududu',
        'https': None,
        'username': None,
        'password': None,
        'auth_endpoint': None,
        'db_name': None,
        'db_type': None,
        'eis_type': 'DB'
    }
]

UPDATE_DATA: Final[list[dict[str, Any]]] = [
    {
        'id': 1,
        'title': '#1 тестовая ВИС',
        'description': None,
        'host': 'google.com',
        'port': 8765,
        'https': False,
        'username': 'user',
        'password': 'pass',
        'auth_endpoint': None,
        'db_name': 'example_database',
        'db_type': 'ORACLE',
        'eis_type': 'DB'
    },
    {
        'id': 2,
        'title': '#2 тестовая ВИС',
        'description': None,
        'host': None,
        'port': None,
        'https': None,
        'username': 'admin',
        'password': 'password',
        'auth_endpoint': None,
        'db_name': None,
        'db_type': None,
        'eis_type': 'HTTP_NO_AUTH'
    }
]

DELETE_IDS: Final[list[int]] = [3, 4]
