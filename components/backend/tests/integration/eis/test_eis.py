import pytest
import pytest_asyncio

from fastapi.testclient import TestClient
from fastapi import status

from typing import Any

from tests.conftest import AppServices
from tests.integration.eis import INIT_DATA, ADD_DATA, UPDATE_DATA, BAD_DATA, DELETE_IDS

from integration_bus.application import dto


@pytest_asyncio.fixture(scope='session', autouse=True)
async def init_db_tables(app_services: AppServices):
    for data in INIT_DATA:
        await app_services.eis_service.add_eis(dto.EisCreateRequest(**data))


@pytest.mark.parametrize('params', ADD_DATA)
def test_add_eis(client: TestClient, params: dict[str, Any]):
    resp = client.post('/eis', json=params)

    assert resp.status_code == status.HTTP_201_CREATED
    assert resp.json().get('title') == params.get('title')
    assert resp.json().get('eis_type') == params.get('eis_type')


@pytest.mark.parametrize('params', BAD_DATA)
def test_add_eis_failed(client: TestClient, params: dict[str, Any]):
    resp = client.post('/eis', json=params)
    assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_get_all_eis(client: TestClient):
    resp = client.get('/eis')
    assert resp.status_code == status.HTTP_200_OK
    assert len(resp.json()) == len(INIT_DATA) + len(ADD_DATA)


@pytest.mark.parametrize('eis_id', range(1, len(INIT_DATA) + len(ADD_DATA) + 1))
def test_get_eis_by_id(client: TestClient, eis_id: int):
    resp = client.get(f'/eis/{eis_id}')
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json() is not None


def test_get_eis_by_id_failed(client: TestClient):
    resp = client.get(f'/eis/{len(INIT_DATA) + len(ADD_DATA) + 1}')
    assert resp.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.parametrize('params', UPDATE_DATA)
def test_update_eis(client: TestClient, params: dict[str, Any]):
    resp = client.put('/eis', json=params)

    assert resp.status_code == status.HTTP_200_OK
    assert resp.json().get('title') == params.get('title')
    assert resp.json().get('username') == params.get('username')
    assert resp.json().get('password') == params.get('password')


def test_update_eis_failed(client: TestClient):
    resp = client.put('/eis', json={
        # нет поля id
        'title': 'Несуществующая тестовая ВИС',
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
    })

    assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.parametrize('id', DELETE_IDS)
def test_delete_eis(client: TestClient, id: int):
    resp = client.delete('/eis', params={'id': id})

    assert resp.status_code == status.HTTP_200_OK


def test_delete_eis_failed(client: TestClient):
    resp = client.delete('/eis', params={'id': 3})

    assert resp.status_code == status.HTTP_404_NOT_FOUND
