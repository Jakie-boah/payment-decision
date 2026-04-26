from src.infrastructure.postgres.repositories.payment import PaymentPostgresRepository

import pytest
from src.infrastructure.postgres.tables import payments_table
from sqlalchemy import select


@pytest.fixture
def repo(session):
    return PaymentPostgresRepository(session)


@pytest.mark.asyncio
async def test_payment_save(repo, session, payment, logger):
    payment.mark_pending()
    await repo.save(payment)
    await session.commit()

    row = await session.execute(
        select(payments_table).where(payments_table.c.id == payment.id.value)
    )

    result = row.mappings().one()
    assert result
    logger.info(result)
