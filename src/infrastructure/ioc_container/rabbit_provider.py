import structlog
from dishka import Provider, Scope, from_context, provide
from faststream.rabbit import RabbitBroker

from src.application.interfaces.publisher import Publisher
from src.infrastructure.broker.publisher import ImplPublisher
from src.infrastructure.config.config_storage import Config
from src.presentation.amqp_api.middleware import ErrorHandlingMiddleware


class RabbitProvider(Provider):
    context = from_context(provides=Config, scope=Scope.APP)

    @provide(scope=Scope.APP)
    async def get_rabbit_broker(self, config: Config, logger: structlog.BoundLogger) -> RabbitBroker:
        broker = RabbitBroker(config.rabbitmq, logger=logger, middlewares=[ErrorHandlingMiddleware])
        await broker.connect()
        return broker

    @provide(scope=Scope.REQUEST)
    async def get_publisher(self, broker: RabbitBroker, logger: structlog.BoundLogger) -> Publisher:
        return ImplPublisher(broker, logger=logger)
