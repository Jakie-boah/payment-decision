import uuid
from decimal import Decimal

import pytest
import pytest_asyncio
from src.application.dto.payment import NewPayment
from src.application.use_cases.create_payment import CreatePaymentUseCase
from src.application.use_cases.publish_payments import PublishPaymentsUseCase
from src.domain.values.currency import Currency


@pytest_asyncio.fixture
async def publish_payments_use_case(container):
    return await container.get(PublishPaymentsUseCase)


@pytest_asyncio.fixture
async def create_payment_use_case(container):
    return await container.get(CreatePaymentUseCase)


@pytest.mark.asyncio
async def test_publish_payments(create_payment_use_case, publish_payments_use_case, uow):
    new_payment_dto = NewPayment(
        amount=Decimal(100),
        currency=Currency.EUR,
        webhook_url="https://example.com",
        meta_data=None,
        idempotency_key=uuid.uuid4()
    )
    await create_payment_use_case(new_payment_dto)

    await publish_payments_use_case()

    outbox = await uow.outbox.filter()
    assert len(outbox) == 0



