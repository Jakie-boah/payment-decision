import pytest
import pytest_asyncio
from src.application.use_cases.create_payment import CreatePaymentUseCase
from sqlalchemy import func, select
from src.infrastructure.postgres.tables import payments_table, outbox_table


@pytest_asyncio.fixture
async def use_case(container):
    return await container.get(CreatePaymentUseCase)


@pytest.mark.asyncio
async def test_create_payment_use_case(
        use_case,
        new_payment_dto,
):
    result = await use_case(new_payment_dto)

    assert result.payment_id
    assert result.status
    assert result.created_at


@pytest.mark.asyncio
async def test_create_payment_and_check_idempotent(
        use_case,
        new_payment_dto,
        session
):
    first_call = await use_case(new_payment_dto)
    second_call = await use_case(new_payment_dto)

    assert first_call.payment_id == second_call.payment_id

    rows = await session.execute(
        select(func.count()).select_from(payments_table)
    )
    p_count = rows.scalar_one()
    assert p_count == 1
    rows = await session.execute(
        select(func.count()).select_from(outbox_table)
    )
    o_count = rows.scalar_one()
    assert o_count == 1

