from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID
from src.domain.values.currency import Currency
from src.domain.values.status import Status
from datetime import datetime


@dataclass(slots=True, frozen=True)
class NewPayment:
    amount: Decimal
    currency: Currency
    webhook_url: str
    meta_data: dict[str, str] | None
    idempotency_key: UUID
    description: str = None


@dataclass(slots=True, frozen=True)
class PaymentRequest:
    amount: Decimal
    currency: Currency
    webhook_url: str
    meta_data: dict[str, str] | None
    description: str = None


@dataclass(slots=True, frozen=True)
class Result:
    payment_id: UUID
    status: Status
    created_at: datetime
