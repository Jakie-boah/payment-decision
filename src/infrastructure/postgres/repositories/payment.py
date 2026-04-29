from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.interfaces.postgres.repository import Repository
from src.domain.entities.payment import Payment
from src.domain.mapper import map_payment_from_db
from src.domain.values.id import Id
from src.infrastructure.postgres.exceptions import PaymentNotFoundError
from src.infrastructure.postgres.tables import payments_table


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

        return map_payment_from_db(row)

    async def get(self, uid: Id) -> Payment:
        rows = await self.session.execute(
            select(payments_table).where(payments_table.c.id == uid.value)
        )
        payment = rows.mappings().first()

        if not payment:
            raise PaymentNotFoundError

        return map_payment_from_db(payment)

    async def filter(self) -> list[Payment]:
        raise NotImplementedError

    async def update(self, domain: Payment):
        await self.session.execute(
            update(payments_table).where(payments_table.c.id == domain.id.value)
            .values(
                webhook=domain.webhook.value,
                description=domain.description.value,
                meta_data=domain.meta_data,
                status=domain.status,
            )
        )
