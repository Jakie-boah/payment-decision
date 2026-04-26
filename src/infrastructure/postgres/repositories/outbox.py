from src.application.interfaces.postgres.repository import Repository
from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.entities.payment import Payment
from src.infrastructure.postgres.tables import outbox_table
from sqlalchemy.dialects.postgresql import insert as pg_insert


class OutboxPostgresRepository(Repository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, payment: Payment):
        await self.session.execute(
            pg_insert(outbox_table).values(
                aggregate_id=payment.id.value,
                event_type=payment.status,
                payload=payment.get_payment_screen(),
                idempotency_key=payment.idempotency_key.value,
                created_at=payment.created_at,
            )
        )
