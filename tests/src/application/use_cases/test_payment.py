from unittest.mock import patch

import pytest
import pytest_asyncio
from sqlalchemy import func, select
from src.application.use_cases.create_payment import CreatePaymentUseCase
from src.application.use_cases.dead_payments import DeadPaymentUseCase
from src.application.use_cases.payment import PaymentUseCase
from src.domain.entities.payment import Payment
from src.domain.values.id import Id
from src.domain.values.status import Status
from src.infrastructure.payment.exceptions import PaymentError
from src.infrastructure.postgres.tables import outbox_table, payments_table


@pytest_asyncio.fixture
async def use_case(container):
    return await container.get(PaymentUseCase)


@pytest_asyncio.fixture
async def create_payment_use_case(container):
    return await container.get(CreatePaymentUseCase)


@pytest.mark.asyncio
async def test_payment_success(create_payment, use_case, session, uow, logger):
    rows = await session.execute(select(payments_table))
    payment = rows.mappings().first()

    payment: Payment = await uow.payment.get(uid=Id(payment.id))

    outbox = payment.get_outbox()

    with patch("src.infrastructure.payment.payment.random.randint", return_value=2):
        await use_case(outbox.convert_to_payload())

    await session.close()

    payment: Payment = await uow.payment.get(uid=payment.id)

    assert payment.status == Status.SUCCEEDED

    rows = await session.execute(
        select(func.count()).select_from(outbox_table)
    )
    o_count = rows.scalar_one()
    assert o_count == 2

    rows = await session.execute(
        select(outbox_table)
    )

    [first, second] = rows.mappings().all()
    logger.info(second)
    assert second.event_type == Status.SUCCEEDED


@pytest_asyncio.fixture
async def dead_use_case(container):
    return await container.get(DeadPaymentUseCase)


@pytest.mark.asyncio
async def test_payment_failure(create_payment, dead_use_case, session, uow, logger):
    rows = await session.execute(select(payments_table))
    payment = rows.mappings().first()

    payment: Payment = await uow.payment.get(uid=Id(payment.id))

    outbox = payment.get_outbox()

    await dead_use_case(outbox.convert_to_payload())

    await session.close()

    payment: Payment = await uow.payment.get(uid=payment.id)

    assert payment.status == Status.FAILED

    rows = await session.execute(
        select(func.count()).select_from(outbox_table)
    )
    o_count = rows.scalar_one()
    assert o_count == 2
    rows = await session.execute(
        select(outbox_table)
    )

    [first, second] = rows.mappings().all()
    logger.info(second)
    assert second.event_type == Status.FAILED
