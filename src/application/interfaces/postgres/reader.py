from datetime import datetime
from decimal import Decimal
from typing import Protocol, TypedDict
from uuid import UUID

from src.domain.values.currency import Currency
from src.domain.values.id import Id
from src.domain.values.status import Status


class Payment(TypedDict):
    id: UUID
    amount: Decimal
    currency: Currency
    webhook: str
    description: str
    status: Status
    meta_data: dict[str, str] | None
    created_at: datetime


class PaymentReader(Protocol):

    async def get_payment_by_id(self, *, uid: Id) -> Payment:
        ...
