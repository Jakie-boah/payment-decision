from dataclasses import dataclass
from decimal import Decimal

from src.domain.values.currency import Currency


@dataclass(slots=True, frozen=True)
class NewPayment:
    amount: Decimal
    currency: Currency
    webhook_url: str
    meta_data: dict[str, str] | None
    description: str = "N/A"
