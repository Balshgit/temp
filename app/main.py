from fastapi import FastAPI

from app.di.app_dependency_injector import DIContainer
from app.infra.logging import configure_logging
from app.routes import api_router
from settings.config import AppSettings, load_app_settings


class Application:
    def __init__(self, settings: AppSettings):
        self.app = FastAPI(
            title="Training title",
            description="Python API",
            debug=settings.DEBUG,
        )
        self.app.state.settings = settings
        self.settings = settings
        self.app.include_router(api_router)
        self.create_di_container()

        configure_logging(
            level=settings.LOG_LEVEL,
            enable_json_logs=settings.ENABLE_JSON_LOGS,
        )

    def create_di_container(self) -> None:
        container = DIContainer()
        self.app.state.container = container

    @property
    def fastapi_app(self) -> FastAPI:
        return self.app


def create_app(settings: AppSettings | None = None) -> FastAPI:
    settings = settings or load_app_settings()
    return Application(settings=settings).fastapi_app


if __name__ == "__main__":
    import uvicorn

    app = create_app()
    host = app.state.settings.APP_HOST
    port = app.state.settings.APP_PORT

    uvicorn.run(app, host=host, port=port)
