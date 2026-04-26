from src.application.interfaces.postgres.repository import Repository
from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.entities.payment import Payment
from src.infrastructure.postgres.tables import payments_table
from sqlalchemy.dialects.postgresql import insert as pg_insert


class PaymentPostgresRepository(Repository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, payment: Payment):
        await self.session.execute(
            pg_insert(payments_table).values(
                id=payment.id.value,
                idempotency_key=payment.idempotency_key.value,
                amount=payment.amount.value,
                currency=payment.currency,
                webhook=payment.webhook.value,
                description=payment.description.value,
                meta_data=payment.meta_data,
                status=payment.status,
                created_at=payment.created_at
            )
        )
