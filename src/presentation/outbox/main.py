import asyncio

import structlog
from dishka import AsyncContainer, make_async_container

from src.application.use_cases.publish_payments import PublishPaymentsUseCase
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


async def monitor():
    config = load_config_from_env()

    while True:
        try:

            container = create_container(config)

            async with container() as req:
                use_case = await req.get(PublishPaymentsUseCase)
                await use_case()

            await container.close()

        except Exception as e:
            logger = await container.get(structlog.BoundLogger)
            logger.error(e)

        finally:
            await asyncio.sleep(5)


if __name__ == "__main__":
    asyncio.run(monitor())
