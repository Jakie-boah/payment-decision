import structlog
from src.application.dto.payment import NewPayment
from src.domain.entities.payment import Payment

class CreatePaymentUseCase:
    def __init__(self, logger: structlog.BoundLogger):
        self.logger = logger

    async def __call__(self, payload: NewPayment):
        ...
