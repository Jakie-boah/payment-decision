from typing import Protocol

from src.domain.values.strings import Webhook


class WebhookService(Protocol):
    async def process(self, *, payload: dict[str, str], webhook: Webhook): ...
