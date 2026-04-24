from src.application.dto.payment import NewPayment
from src.domain.entities.payment import Payment
from src.domain.values.number import Amount
from src.domain.values.currency import Currency
from src.domain.values.strings import Webhook, Description


def map_payment_from_dto(dto: NewPayment) -> Payment:
    amount = Amount(dto.amount)
    currency = Currency(dto.currency)
    webhook = Webhook(dto.webhook_url)
    description = Description(dto.description)

    return Payment(
        amount=amount,
        currency=currency,
        webhook=webhook,
        description=description,
        meta_data=dto.meta_data,
    )
