from src.infrastructure.postgres.reader.payment import ImplPaymentReader
import pytest_asyncio

from src.application.use_cases.create_payment import CreatePaymentUseCase
import uuid
from src.application.dto.payment import NewPayment
from decimal import Decimal
import pytest
from src.domain.values.currency import Currency
from src.infrastructure.postgres.tables import payments_table
from sqlalchemy import select
from src.infrastructure.postgres.exceptions import PaymentNotFoundError

from src.domain.values.id import Id


@pytest_asyncio.fixture
async def use_case(container):
    return await container.get(CreatePaymentUseCase)


@pytest_asyncio.fixture
async def create_payment(use_case):
    new_payment_dto = NewPayment(
        amount=Decimal(100),
        currency=Currency.EUR,
        webhook_url="https://example.com",
        meta_data=None,
        idempotency_key=uuid.uuid4()
    )
    await use_case(new_payment_dto)


@pytest.mark.asyncio
async def test_get_payment(session, create_payment):
    rows = await session.execute(select(payments_table.c.id))
    first = rows.mappings().first()

    reader = ImplPaymentReader(session)
    payment = await reader.get_payment_by_id(uid=Id(first.id))
    assert "id" in payment
    assert "amount" in payment
    assert "currency" in payment
    assert "webhook" in payment
    assert "description" in payment
    assert "status" in payment
    assert "meta_data" in payment
    assert "created_at" in payment


@pytest.mark.asyncio
async def test_get_payment_raise(session, ):
    reader = ImplPaymentReader(session)

    with pytest.raises(PaymentNotFoundError):
        await reader.get_payment_by_id(uid=Id(uuid.uuid4()))