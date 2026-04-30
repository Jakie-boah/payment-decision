from dataclasses import dataclass
from decimal import Decimal

from src.domain.values.base import BaseValueObject


DECIMAL_PLACES = 2
INTEGER_PART = 13

@dataclass(frozen=True, slots=True)
class Amount(BaseValueObject):
    value: Decimal

    def validate(self):
        if self.value <= 0:
            raise ValueError("Amount must be positive")

        if self.value.is_nan() or self.value.is_infinite():
            raise ValueError("Invalid amount")

        if abs(self.value.as_tuple().exponent) > DECIMAL_PLACES:
            raise ValueError("Too many decimal places")

        integer_part = abs(int(self.value))
        if len(str(integer_part)) > INTEGER_PART:
            raise ValueError("Integer part must have at most 13 digits")

    def as_generic(self):
        return str(self.value)
