from dataclasses import asdict

import structlog
from faststream.rabbit import RabbitBroker

from src.application.interfaces.publisher import Publisher
from src.domain.entities.outbox import Outbox


class ImplPublisher(Publisher):

    def __init__(self, broker: RabbitBroker, logger: structlog.BoundLogger):
        self.broker = broker
        self.logger = logger

    async def publish(self, outbox: Outbox) -> None:
        payload = outbox.convert_to_payload()
        await self.broker.publish(
            payload,
            queue="payment-queue",
        )
        self.logger.info(f"ОТпавил все гонво {asdict(payload)}")
