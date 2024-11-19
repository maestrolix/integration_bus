# Импортируем модуль с раннерами, чтобы на них сработал декоратор,
# и у RunnerCollector были данные о всех классах раннеров.
# TODO: так делать на самом деле некорректно. Это решение остается
#   до момента, пока не будет предложено что-то лучше.
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from integration_bus.adapters import database, http_api, log, connection
from integration_bus.adapters.database import repositories
from integration_bus.adapters.http_api import create_app
from integration_bus.adapters.http_api.dependencies import Services
from integration_bus.application import services


class Settings:
    http_api = http_api.Settings()
    db = database.Settings()


class Logger:
    log.configure(Settings.http_api.LOGGING_CONFIG, Settings.db.LOGGING_CONFIG)


class DB:
    engine = create_async_engine(Settings.db.DATABASE_URL, echo=Settings.db.DATABASE_DEBUG)
    async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

    eis_repo = repositories.EisRepository(async_session_maker=async_session_maker)
    runner_repo = repositories.RunnerRepository(async_session_maker=async_session_maker)
    
    log.logger.set_sessionmaker(async_session_maker)


class Application:
    eis_service = services.EisService(eis_repo=DB.eis_repo)
    runner_service = services.RunnerService(
        runner_repo=DB.runner_repo,
        eis_repo=DB.eis_repo,
    )
    router_service = services.RouterService(
        connection_manager=connection.ConnectionManager(),
        runner_repo=DB.runner_repo,
    )
    dependency_validation_service = services.DependencyValidationService(
        runner_repo=DB.runner_repo
    )


def init_services():
    Services.eis = Application.eis_service
    Services.runner = Application.runner_service
    Services.router = Application.router_service
    Services.dependency_validation_service = Application.dependency_validation_service


def init_app():
    init_services()


init_app()
app = create_app(
    is_debug=Settings.http_api.APP_IS_DEBUG,
    version=Settings.http_api.APP_VERSION,
    swagger_on=Settings.http_api.APP_SWAGGER_ON,
    title=Settings.http_api.APP_TITLE
)


@app.on_event('startup')
async def startup_event():
    """ Хук, исполняющийся один раз перед запуском FastAPI приложения. """
    await Services.dependency_validation_service.validate_runner_info()
