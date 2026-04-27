from src.infrastructure.postgres.repositories.payment import PaymentPostgresRepository

import pytest
from src.infrastructure.postgres.tables import payments_table
from sqlalchemy import select


@pytest.fixture
def mapper(session):
    return PaymentPostgresRepository(session)


@pytest.mark.asyncio
async def test_payment_save(mapper, session, payment, logger):
    payment.mark_pending()
    await mapper.save(payment)
    await session.commit()

    row = await session.execute(
        select(payments_table).where(payments_table.c.id == payment.id.value)
    )

    result = row.mappings().one()
    assert result
    logger.info(result)


@pytest.mark.asyncio
async def test_payment_conflict(mapper, session, payment, logger):
    p1 = await mapper.save(payment)
    await session.commit()

    p2 = await mapper.save(payment)
    await session.commit()

    assert p1.id == p2.id
