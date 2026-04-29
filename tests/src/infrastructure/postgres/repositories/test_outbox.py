import pytest
from sqlalchemy import select
from src.infrastructure.postgres.repositories.outbox import OutboxPostgresRepository
from src.infrastructure.postgres.tables import outbox_table


@pytest.fixture
def repo(session):
    return OutboxPostgresRepository(session)


@pytest.mark.asyncio
async def test_outbox_repo(repo, session, payment, logger):
    payment.mark_pending()
    await repo.save(payment.get_outbox())
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
    outbox = payment.get_outbox()
    assert outbox.processed_at is None
    await repo.save(outbox)
    await session.commit()

    result = await repo.filter()
    logger.info(result)
    [outbox] = result
    assert outbox.processed_at is None
