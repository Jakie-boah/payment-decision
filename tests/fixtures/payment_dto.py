import uuid
from src.application.dto.payment import NewPayment
from decimal import Decimal
import pytest
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
