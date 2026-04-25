from src.domain.entities.payment import Payment
from src.domain.values.id import IdempotencyKey
from src.domain.values.status import Status
import pytest
from faker import Faker
from src.domain.values.number import Amount
from src.domain.values.currency import Currency
from src.domain.values.strings import Webhook
from datetime import datetime, date

fake = Faker()


@pytest.fixture(name="payment")
def payment_raw():
    return Payment(
        idempotency_key=IdempotencyKey(fake.uuid4()),
        amount=Amount(fake.pydecimal(positive=True, right_digits=2)),
        currency=Currency(Currency.RUB),
        webhook=Webhook(fake.url())
    )


def test_payment_date_field(payment):
    assert payment.created_at.date() == datetime.now().date()


@pytest.mark.parametrize(
    "case",
    (
            Status.FAILED,
            Status.PENDING,
            Status.SUCCEEDED,
    )
)
def test_set_status(case, payment):
    match case:
        case case.FAILED:
            payment.mark_failed()
            assert payment.status == Status.FAILED

        case case.PENDING:
            payment.mark_pending()
            assert payment.status == Status.PENDING

        case case.SUCCEEDED:
            payment.mark_succeeded()
            assert payment.status == Status.SUCCEEDED
