from src.application.interfaces.postgres.repository import Repository, T
from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.entities.payment import Payment
from src.domain.values.currency import Currency
from src.domain.values.number import Amount
from src.domain.values.status import Status
from src.domain.values.strings import Webhook, Description
from src.infrastructure.postgres.tables import payments_table
from sqlalchemy.dialects.postgresql import insert as pg_insert
from src.domain.values.id import Id, IdempotencyKey


class PaymentPostgresRepository(Repository[Payment]):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, payment: Payment) -> Payment:
        stmt = (
            pg_insert(payments_table)
            .values(
                id=payment.id.value,
                idempotency_key=payment.idempotency_key.value,
                amount=payment.amount.value,
                currency=payment.currency,
                webhook=payment.webhook.value,
                description=payment.description.value,
                meta_data=payment.meta_data,
                status=payment.status,
                created_at=payment.created_at,
            )
            .on_conflict_do_update(
                index_elements=["idempotency_key"],
                set_={
                    "id": payments_table.c.id,
                },
            )
            .returning(payments_table)
        )

        result = await self.session.execute(stmt)
        row = result.mappings().first()

        return Payment(
            uid=Id(row.id),
            idempotency_key=IdempotencyKey(row.idempotency_key),
            amount=Amount(row.amount),
            currency=Currency(row.currency),
            webhook=Webhook(row.webhook),
            description=Description(row.description),
            meta_data=row.meta_data,
            status=Status(row.status),
            created_at=row.created_at,
        )

    async def filter(self) -> list[Payment]:
        raise NotImplementedError

    async def update(self, domain: Payment):
        raise NotImplementedError