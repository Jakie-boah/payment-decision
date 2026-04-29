import pytest
from faker import Faker
from src.domain.entities.payment import Payment
from src.domain.values.currency import Currency
from src.domain.values.id import IdempotencyKey
from src.domain.values.number import Amount
from src.domain.values.strings import Webhook


fake = Faker()


@pytest.fixture(name="payment")
def payment_raw():
    return Payment(
        idempotency_key=IdempotencyKey(fake.uuid4()),
        amount=Amount(fake.pydecimal(positive=True, left_digits=13, right_digits=2)),
        currency=Currency(Currency.RUB),
        webhook=Webhook(fake.url())
    )
