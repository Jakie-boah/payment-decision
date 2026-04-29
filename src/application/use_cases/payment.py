import structlog

from src.application.dto.amqp import OutboxPayload
from src.application.interfaces.payment.service import PaymentService
from src.application.interfaces.postgres.uow import UnitOfWork
from src.domain.entities.outbox import Outbox
from src.domain.entities.payment import Payment
from src.domain.mapper import map_outbox_from_payload


class PaymentUseCase:
    def __init__(
            self,
            logger: structlog.BoundLogger,
            payment_service: PaymentService,
            uow: UnitOfWork,
    ):
        self.logger = logger
        self.payment_service = payment_service
        self.uow = uow

    async def __call__(self, payload: OutboxPayload):

        outbox: Outbox = map_outbox_from_payload(payload)

        payment: Payment = await self.uow.payment.get(uid=outbox.aggregate_id)

        await self.payment_service.process(payment)

        payment.mark_succeeded()

        outbox = payment.get_outbox()
        outbox.mark_as_processed()

        await self.uow.payment.update(payment)
        await self.uow.outbox.save(outbox)

        await self.uow.commit()
