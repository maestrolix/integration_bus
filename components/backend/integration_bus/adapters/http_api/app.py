from fastapi import FastAPI

from integration_bus.adapters.http_api import controllers


def create_app(
        version: str,
        is_debug: bool = False,
        swagger_on: bool = False,
        title: str = 'noname'
) -> FastAPI:
    """ Собирает основное приложение """
    app = FastAPI(
        title=title,
        debug=is_debug,
        version=version,
        docs_url='/docs' if swagger_on else None,
        redoc_url='/redoc' if swagger_on else None,
    )

    app.include_router(controllers.eis_router)
    app.include_router(controllers.runner_router)
    app.include_router(controllers.event_router)
    return app
