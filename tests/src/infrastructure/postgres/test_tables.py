import pytest_asyncio
import pytest

from src.infrastructure.postgres.tables import outbox_table
from sqlalchemy import insert


@pytest.mark.asyncio
async def test_outbox_table(session, logger):
    await session.execute(
        insert(outbox_table).values(
            name="test",
        )
    )
    await session.commit()
    logger.info(" все ок")
