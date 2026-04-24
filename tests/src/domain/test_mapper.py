from src.domain.mapper import map_payment_from_dto
from src.domain.entities.payment import Payment
from src.application.dto.payment import NewPayment
from decimal import Decimal
import pytest
from src.domain.values.id import Id
from src.domain.values.number import Amount
from src.domain.values.currency import Currency
from src.domain.values.strings import Webhook, Description


@pytest.fixture
def new_payment_dto() -> NewPayment:
    return NewPayment(
        amount=Decimal(100),
        currency=Currency.EUR,
        webhook_url="https://example.com",
        meta_data=None
    )


def test_map_payment_from_dto(new_payment_dto):
    payment = map_payment_from_dto(new_payment_dto)

    assert payment
    assert isinstance(payment, Payment)
    assert isinstance(payment.id, Id)
    assert isinstance(payment._currency, Currency)
    assert isinstance(payment._webhook, Webhook)
    assert isinstance(payment._description, Description)
    assert isinstance(payment._amount, Amount)
    assert isinstance(payment._meta_data, type(None))
