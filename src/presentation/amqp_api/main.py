import asyncio

import structlog
from dishka import make_async_container
from dishka.integrations.faststream import setup_dishka as setup_faststream_ioc
from faststream.asgi import AsgiFastStream, make_ping_asgi
from faststream.rabbit import RabbitBroker

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
from src.presentation.amqp_api.endpoints import router


async def application_factory():
    config = load_config_from_env()

    container = make_async_container(
        LoggerProvider(),
        SessionProvider(),
        AioHttpProvider(),
        RabbitProvider(),
        PaymentProvider(),
        UseCaseProvider(),
        context={Config: config}
    )

    broker = await container.get(RabbitBroker)
    logger = await container.get(structlog.BoundLogger)

    broker.include_routers(router)

    app = AsgiFastStream(
        broker,
        asyncapi_path="/docs",
        asgi_routes=[
            ("/health", make_ping_asgi(broker, timeout=3.0)),
        ],
    )
    logger.info("Точка входа для стрима")

    setup_faststream_ioc(
        container=container,
        app=app,
        finalize_container=True,
    )

    run_options = {"host": "0.0.0.0", "port": "8000"}

    await app.run(run_extra_options=run_options)


if __name__ == "__main__":
    asyncio.run(application_factory())
