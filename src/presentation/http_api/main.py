from dishka import AsyncContainer, make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from src.infrastructure.config.config_loader import load_config_from_env
from src.infrastructure.config.config_storage import Config
from src.infrastructure.ioc_container import (
    LoggerProvider,
    PaymentProvider,
    RabbitProvider,
    SessionProvider,
    AioHttpProvider,
    UseCaseProvider,
)
from src.presentation.http_api.handlers import register_exception_handlers
from src.presentation.http_api.routers import router


def create_container(config: Config) -> AsyncContainer:
    return make_async_container(
        LoggerProvider(),
        SessionProvider(),
        RabbitProvider(),
        PaymentProvider(),
        AioHttpProvider(),
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
