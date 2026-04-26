from dishka import make_async_container, AsyncContainer
from src.infrastructure.ioc_container import UseCaseProvider, LoggerProvider, SessionProvider

from src.infrastructure.config.config_storage import Config


def create_container(config: Config) -> AsyncContainer:
    return make_async_container(
        LoggerProvider(),
        SessionProvider(),
        UseCaseProvider(),
        context={Config: config}
    )
