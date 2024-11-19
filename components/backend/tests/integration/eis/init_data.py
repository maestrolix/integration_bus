from typing import Any, Final


INIT_DATA: Final[list[dict[str, Any]]] = [
    {
        'title': 'Первая тестовая ВИС',
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
        'title': 'Вторая тестовая ВИС',
        'description': None,
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
        'title': 'Третья тестовая ВИС',
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
        'title': 'Четвертая тестовая ВИС',
        'description': None,
        'host': None,
        'port': None,
        'https': None,
        'username': 'postgres',
        'password': 'postgres',
        'auth_endpoint': None,
        'db_name': 'remote_database',
        'db_type': 'POSTGRES',
        'eis_type': 'DB'
    }
]
