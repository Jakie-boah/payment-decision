from typing import Protocol

from src.domain.entities.outbox import Outbox


class Publisher(Protocol):
    async def publish(self, outbox: Outbox) -> None: ...
