import pytest
from sqlalchemy import select
from src.domain.values.status import Status
from src.infrastructure.postgres.repositories.payment import PaymentPostgresRepository
from src.infrastructure.postgres.tables import payments_table


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


@pytest.mark.asyncio
async def test_payment_conflict(repo, session, payment, logger):
    p1 = await repo.save(payment)
    await session.commit()

    p2 = await repo.save(payment)
    await session.commit()

    assert p1.id == p2.id


@pytest.mark.asyncio
async def test_update(repo, session, payment, logger):
    await repo.save(payment)
    await session.commit()

    payment.mark_succeeded()

    await repo.update(payment)
    await session.commit()


    payment = await repo.get(uid=payment.id)
    assert payment.status == Status.SUCCEEDED
