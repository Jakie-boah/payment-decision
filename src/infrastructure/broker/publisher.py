from src.application.interfaces.publisher import Publisher
from src.domain.entities.outbox import Outbox


class ImplPublisher(Publisher):
    async def publish(self, outbox: Outbox) -> None:
        pass
