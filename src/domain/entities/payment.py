from datetime import UTC, datetime

from src.domain.entities.outbox import Outbox
from src.domain.values.currency import Currency
from src.domain.values.id import Id, IdempotencyKey
from src.domain.values.number import Amount
from src.domain.values.status import Status
from src.domain.values.strings import Description, Webhook


class Payment:
    def __init__(
            self,
            *,
            idempotency_key: IdempotencyKey,
            amount: Amount,
            currency: Currency,
            webhook: Webhook,

            uid: Id = None,
            description: Description = None,
            meta_data: dict | None = None,
            created_at: datetime | None = None,
            status: Status = Status.NOT_SET,
    ):
        self._id = uid or Id.generate()
        self._idempotency_key = idempotency_key

        self._amount = amount
        self._currency = currency
        self._description = description or Description.default()
        self._webhook = webhook
        self._meta_data = meta_data

        self._status: Status = status

        self._created_at: datetime = created_at or datetime.now(UTC)
        self.__outbox = None

    @property
    def id(self):
        return self._id

    @property
    def status(self):
        return self._status

    @property
    def idempotency_key(self):
        return self._idempotency_key

    @property
    def amount(self):
        return self._amount

    @property
    def currency(self):
        return self._currency

    @property
    def webhook(self):
        return self._webhook

    @property
    def description(self):
        return self._description

    @property
    def meta_data(self):
        return self._meta_data

    @property
    def created_at(self):
        return self._created_at

    def mark_failed(self):
        self._status = Status.FAILED

    def mark_succeeded(self):
        self._status = Status.SUCCEEDED

    def mark_pending(self):
        self._status = Status.PENDING

    def get_outbox(self) -> Outbox:

        self.__outbox = Outbox(
            aggregate_id=self.id,
            idempotency_key=self.idempotency_key,
            event_type=self.status,
            payload=self._get_payment_screen(),
            created_at=self.created_at,
        )
        return self.__outbox

    def _get_payment_screen(self):
        return {
            "payment_id": self.id.as_generic(),
            "amount": self._amount.as_generic(),
            "currency": self._currency,
            "status": self.status,
            "created_at": str(self.created_at),
        }
