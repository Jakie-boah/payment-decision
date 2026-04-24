from src.domain.values.id import Id
from src.domain.values.number import Amount
from src.domain.values.currency import Currency
from src.domain.values.strings import Webhook, Description


class Payment:
    def __init__(
            self,
            *,
            amount: Amount,
            currency: Currency,
            description: Description,
            webhook: Webhook,
            uid: Id = None,
            meta_data: dict | None = None,

    ):
        self._id = uid or Id.generate()

        self._amount = amount
        self._currency = currency
        self._description = description
        self._webhook = webhook
        self._meta_data = meta_data

    @property
    def id(self):
        return self._id

    def mark_failed(self):
        pass

    def mark_succeeded(self):
        pass

    def mark_pending(self):
        pass
