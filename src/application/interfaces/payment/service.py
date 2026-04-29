from typing import Protocol

from src.domain.entities.payment import Payment


class PaymentService(Protocol):
    async def process(self, payment: Payment): ...
