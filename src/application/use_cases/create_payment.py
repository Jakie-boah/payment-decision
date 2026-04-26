import structlog
from src.application.dto.payment import NewPayment
from src.domain.entities.payment import Payment
from src.domain.mapper import map_payment_from_dto
from src.application.interfaces.postgres.uow import UnitOfWork
from src.application.dto.payment import Result


class CreatePaymentUseCase:
    def __init__(
            self,
            logger: structlog.BoundLogger,
            uow: UnitOfWork,
    ):
        self.logger = logger
        self.uow = uow

    async def __call__(self, payload: NewPayment) -> Result:
        payment: Payment = map_payment_from_dto(payload)
        payment.mark_pending()

        await self.uow.outbox.save(payment)
        await self.uow.payment.save(payment)

        await self.uow.commit()

        return Result(
            payment_id=payment.id,
            status=payment.status,
            created_at=payment.created_at
        )
