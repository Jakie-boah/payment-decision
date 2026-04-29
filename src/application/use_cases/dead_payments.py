import structlog

from src.application.dto.amqp import OutboxPayload
from src.application.interfaces.postgres.uow import UnitOfWork
from src.domain.entities.outbox import Outbox
from src.domain.entities.payment import Payment
from src.domain.mapper import map_outbox_from_payload


class DeadPaymentUseCase:

    def __init__(self, uow: UnitOfWork, logger: structlog.BoundLogger):
        self.uow = uow
        self.logger = logger

    async def __call__(self, payload: OutboxPayload):
        self.logger.error("Payment failed")
        outbox: Outbox = map_outbox_from_payload(payload)

        payment: Payment = await self.uow.payment.get(uid=outbox.aggregate_id)

        payment.mark_failed()

        outbox = payment.get_outbox()
        outbox.mark_as_processed()

        await self.uow.payment.update(payment)
        await self.uow.outbox.save(outbox)
        await self.uow.commit()
