
from src.domain.mapper import map_payment_from_dto
from src.domain.entities.payment import Payment

from src.domain.values.id import Id, IdempotencyKey
from src.domain.values.number import Amount
from src.domain.values.currency import Currency
from src.domain.values.strings import Webhook, Description



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
    assert isinstance(payment._idempotency_key, IdempotencyKey)
