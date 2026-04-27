from src.infrastructure.postgres.repositories.outbox import OutboxPostgresRepository

import pytest
from src.infrastructure.postgres.tables import outbox_table
from sqlalchemy import select


@pytest.fixture
def repo(session):
    return OutboxPostgresRepository(session)


@pytest.mark.asyncio
async def test_outbox_repo(repo, session, payment, logger):
    payment.mark_pending()
    await repo.save(payment.generate_outbox())
    await session.commit()

    row = await session.execute(
        select(outbox_table).where(outbox_table.c.idempotency_key == payment.idempotency_key.value)
    )

    result = row.mappings().one()
    assert result
    logger.info(result)


@pytest.mark.asyncio
async def test_filter_outbox(repo, payment, session, logger):
    payment.mark_pending()
    await repo.save(payment.generate_outbox())
    await session.commit()

    result = await repo.filter()
    logger.info(result)

