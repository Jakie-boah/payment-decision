import structlog
from aiohttp import ClientSession

from src.application.interfaces.webhook.call import WebhookService
from src.domain.values.strings import Webhook


class ImplWebhookService(WebhookService):
    def __init__(
            self,
            *,
            http_session: ClientSession,
            logger: structlog.BoundLogger,
    ):
        self.http_session = http_session
        self.logger = logger

    async def get_feed(self, *, payload: dict[str, str], webhook: Webhook):
        async with self.http_session.request(
                "POST", webhook.value, json=payload, timeout=10
        ) as resp:
            resp.raise_for_status()
            return await resp.json()
