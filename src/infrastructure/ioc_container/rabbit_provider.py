from dishka import Provider, Scope, provide, from_context

from src.infrastructure.config.config_storage import Config
from faststream.rabbit import RabbitBroker
from src.infrastructure.broker.publisher import ImplPublisher
from src.application.interfaces.publisher import Publisher


class RabbitProvider(Provider):
    context = from_context(provides=Config, scope=Scope.APP)

    @provide(scope=Scope.APP)
    async def get_rabbit_broker(self, config: Config) -> RabbitBroker:
        broker = RabbitBroker(config.rabbitmq)
        await broker.connect()
        return broker

    @provide(scope=Scope.REQUEST)
    async def get_publisher(self) -> Publisher:
        return ImplPublisher()
