from collections.abc import AsyncGenerator
from typing import Any

import structlog
from aiohttp import ClientSession
from dishka import Provider, Scope, from_context, provide

from src.application.interfaces.webhook.call import WebhookService
from src.infrastructure.config.config_storage import Config
from src.infrastructure.webhook.call import ImplWebhookService


class AioHttpProvider(Provider):
    context = from_context(provides=Config, scope=Scope.APP)

    @provide(scope=Scope.REQUEST)
    async def get_aiohttp_session(self) -> AsyncGenerator[ClientSession, Any]:
        async with ClientSession() as session:
            yield session

    @provide(scope=Scope.REQUEST)
    async def get_feed_external_api_service(
        self, http_session: ClientSession,  logger: structlog.BoundLogger
    ) -> WebhookService:
        return ImplWebhookService(http_session=http_session, logger=logger)
