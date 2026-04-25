from src.application.dto.payment import NewPayment
from src.domain.entities.payment import Payment
from src.domain.values.number import Amount
from src.domain.values.currency import Currency
from src.domain.values.strings import Webhook, Description
from src.domain.values.id import IdempotencyKey


def map_payment_from_dto(dto: NewPayment) -> Payment:
    idempotency_key = IdempotencyKey(dto.idempotency_key)
    amount = Amount(dto.amount)
    currency = Currency(dto.currency)
    webhook = Webhook(dto.webhook_url)
    description = Description(dto.description) if dto.description else None

    return Payment(
        idempotency_key=idempotency_key,
        amount=amount,
        currency=currency,
        webhook=webhook,
        description=description,
        meta_data=dto.meta_data,
    )
