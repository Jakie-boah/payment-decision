from dishka import make_async_container, AsyncContainer
from fastapi import FastAPI
from dishka.integrations.fastapi import setup_dishka
from src.presentation.http.handlers import register_exception_handlers
from src.infrastructure.config.config_loader import load_config_from_env
from src.infrastructure.ioc_container import UseCaseProvider, LoggerProvider, SessionProvider

from src.infrastructure.config.config_storage import Config
from src.presentation.http.routers import router


def create_container(config: Config) -> AsyncContainer:
    return make_async_container(
        LoggerProvider(),
        SessionProvider(),
        UseCaseProvider(),
        context={Config: config}
    )


def create_app() -> FastAPI:
    app = FastAPI(
        title="PAYMENT-DECISION",
        root_path="/",
    )

    @app.get("/health")
    async def healthcheck():
        return {"status": "ok"}

    app.include_router(router)

    register_exception_handlers(app)

    return app


def app_factory() -> FastAPI:
    config: Config = load_config_from_env()
    app = create_app()
    container = create_container(config)

    setup_dishka(container=container, app=app)
    return app
