import structlog

from src.application.interfaces.postgres.uow import UnitOfWork
from src.application.interfaces.publisher import Publisher
from src.domain.entities.outbox import Outbox


class PublishPaymentsUseCase:
    def __init__(
            self,
            logger: structlog.BoundLogger,
            publisher: Publisher,
            uow: UnitOfWork

    ):
        self.logger = logger
        self.publisher = publisher
        self.uow = uow

    async def __call__(self):
        outboxes: list[Outbox] = await self.uow.outbox.filter()

        if not outboxes:
            self.logger.info("No outbox")
            return

        for outbox in outboxes:
            self.logger.info(outbox)
            await self.publisher.publish(outbox)

            outbox.mark_as_processed()
            await self.uow.outbox.update(outbox)
            self.logger.info(f"Апдейтнул для {outbox.pk}")

        await self.uow.commit()
        self.logger.info("вышел")
