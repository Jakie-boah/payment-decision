import asyncio
from collections.abc import Awaitable, Callable
from typing import Any

from faststream import BaseMiddleware, StreamMessage
from faststream.rabbit.message import RabbitMessage

from src.infrastructure.payment.exceptions import PaymentError


class ErrorHandlingMiddleware(BaseMiddleware):
    MAX_RETRIES = 3

    async def consume_scope(
            self,
            call_next: Callable[[StreamMessage[Any]], Awaitable[Any]],
            msg: RabbitMessage,
    ) -> Any:

        for attempt in range(self.MAX_RETRIES + 1):
            try:
                result = await call_next(msg)
                await msg.ack()
                return result

            except PaymentError:
                if attempt == self.MAX_RETRIES:
                    await msg.nack(requeue=False)
                    raise

                await asyncio.sleep(2 ** attempt)
        return None
