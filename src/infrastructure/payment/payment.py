import random

import structlog

from src.application.interfaces.payment.service import PaymentService
from src.domain.entities.payment import Payment
from src.infrastructure.payment.exceptions import PaymentError


class ImplPaymentService(PaymentService):
    def __init__(self, logger: structlog.BoundLogger):
        self.logger = logger

    async def process(self, payment: Payment):

        choice = random.randint(1, 10)

        if choice == 1:
            raise PaymentError()

