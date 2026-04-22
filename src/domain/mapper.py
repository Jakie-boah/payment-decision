from src.application.dto.payment import NewPayment
from src.domain.entities.payment import Payment
from src.domain.values.number import Amount


def map_payment_from_dto(dto: NewPayment) -> Payment:

    amount = Amount(dto.amount)


    return Payment(
        amount=amount,
    )
