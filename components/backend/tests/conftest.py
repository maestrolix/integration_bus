from asyncio import AbstractEventLoop

import pytest
import pytest_asyncio
import asyncio

from fastapi.testclient import TestClient

from dataclasses import dataclass

from integration_bus.adapters import database, http_api, log, connection
from integration_bus.adapters.database import repositories
from integration_bus.application import services
from integration_bus.adapters.http_api.dependencies import Services
from integration_bus.adapters.http_api.app import create_app
from integration_bus.adapters.database.tables import metadata

from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, async_sessionmaker


@pytest.fixture(scope='session')
def event_loop():
    """ Переопределение фикстуры по умолчанию для поддержки async-фикстур. """
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@dataclass
class AppSettings:
    http_api: http_api.Settings
    db: database.Settings


@pytest.fixture(scope='session')
def app_settings() -> AppSettings:
    app_settings = AppSettings(
        http_api=http_api.Settings(),
        db=database.Settings()
    )
    log.configure(app_settings.http_api.LOGGING_CONFIG, app_settings.db.LOGGING_CONFIG)
    return app_settings


@dataclass
class DbConfig:
    engine: AsyncEngine
    async_session_maker: async_sessionmaker

    eis_repo: repositories.EisRepository
    runner_repo: repositories.RunnerRepository
    event_repo: repositories.EventRepository


@pytest_asyncio.fixture(scope='session')
async def db_config(app_settings: AppSettings) -> DbConfig:
    engine = create_async_engine('sqlite+aiosqlite:///', echo=app_settings.db.DATABASE_DEBUG)
    async with engine.connect() as conn:
        await conn.run_sync(metadata.create_all)
    async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
    return DbConfig(
        engine=engine,
        async_session_maker=async_session_maker,
        eis_repo=repositories.EisRepository(async_session_maker=async_session_maker),
        runner_repo=repositories.RunnerRepository(async_session_maker=async_session_maker),
        event_repo=repositories.EventRepository(async_session_maker=async_session_maker)
    )


@dataclass
class AppServices:
    eis_service: services.EisService
    runner_service: services.RunnerService
    event_service: services.EventService
    router_service: services.RouterService


@pytest.fixture(scope='session')
def app_services(db_config: DbConfig, app_settings: AppSettings) -> AppServices:
    return AppServices(
        eis_service=services.EisService(eis_repo=db_config.eis_repo),
        runner_service=services.RunnerService(
            runner_repo=db_config.runner_repo,
            eis_repo=db_config.eis_repo,
        ),
        event_service=services.EventService(event_repo=db_config.event_repo),
        router_service=services.RouterService(
            connection_manager=connection.ConnectionManager(),
            runner_repo=db_config.runner_repo,
            event_repo=db_config.event_repo
        )
    )


@pytest.fixture(scope='session')
def client(
        app_services: AppServices,
        app_settings: AppSettings,
        event_loop: AbstractEventLoop
) -> TestClient:
    Services.eis = app_services.eis_service
    Services.runner = app_services.runner_service
    Services.event = app_services.event_service
    Services.router = app_services.router_service

    if not event_loop:
        event_loop.create_task(Services.dependency_validation_service.validate_runner_info())

    app = create_app(
        is_debug=app_settings.http_api.APP_IS_DEBUG,
        version=app_settings.http_api.APP_VERSION,
        swagger_on=app_settings.http_api.APP_SWAGGER_ON,
        title=app_settings.http_api.APP_TITLE
    )

    return TestClient(app)
