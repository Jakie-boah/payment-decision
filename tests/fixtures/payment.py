import uuid
from decimal import Decimal

import pytest
import pytest_asyncio
from src.application.dto.payment import NewPayment
from src.application.use_cases.create_payment import CreatePaymentUseCase
from src.domain.values.currency import Currency


@pytest.fixture
def new_payment_dto() -> NewPayment:
    return NewPayment(
        amount=Decimal(100),
        currency=Currency.EUR,
        webhook_url="https://example.com",
        meta_data=None,
        idempotency_key=uuid.uuid4()
    )


@pytest_asyncio.fixture(name="create_payment")
async def create_payment_use_case(container):
    new_payment_dto = NewPayment(
        amount=Decimal(100),
        currency=Currency.EUR,
        webhook_url="https://example.com",
        meta_data=None,
        idempotency_key=uuid.uuid4()
    )

    use_case = await container.get(CreatePaymentUseCase)

    await use_case(new_payment_dto)

