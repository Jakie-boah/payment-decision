from dishka import AsyncContainer, make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import Depends, FastAPI, Header, HTTPException, status

from src.infrastructure.config.config_loader import load_config_from_env
from src.infrastructure.config.config_storage import Config
from src.infrastructure.ioc_container import (
    AioHttpProvider,
    LoggerProvider,
    PaymentProvider,
    RabbitProvider,
    SessionProvider,
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


def create_app(config: Config) -> FastAPI:

    async def verify_api_key(x_api_key: str = Header(..., alias="X-API-Key")):
        if x_api_key != config.super_secret_api_key:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid API key",
            )

    app = FastAPI(
        title="PAYMENT-DECISION",
        root_path="/",
        dependencies=[Depends(verify_api_key)],
    )

    @app.get("/health")
    async def healthcheck():
        return {"status": "ok"}

    app.include_router(router)

    register_exception_handlers(app)

    return app


def app_factory() -> FastAPI:
    config: Config = load_config_from_env()
    app = create_app(config)
    container = create_container(config)

    setup_dishka(container=container, app=app)
    return app
