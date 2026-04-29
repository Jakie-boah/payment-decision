from typing import cast

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.interfaces.postgres.reader import Payment, PaymentReader
from src.domain.values.id import Id
from src.infrastructure.postgres.exceptions import PaymentNotFoundError
from src.infrastructure.postgres.tables import payments_table


class ImplPaymentReader(PaymentReader):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_payment_by_id(self, *, uid: Id) -> Payment:
        rows = await self.session.execute(
            select(
                payments_table.c.id,
                payments_table.c.amount,
                payments_table.c.currency,
                payments_table.c.webhook,
                payments_table.c.description,
                payments_table.c.status,
                payments_table.c.meta_data,
                payments_table.c.created_at,
            ).where(payments_table.c.id == uid.value)
        )
        result = rows.mappings().first()

        if not result:
            raise PaymentNotFoundError

        return cast("Payment", dict(result))
