from uuid import UUID, uuid4

from src.domain.values.base import BaseValueObject
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Id(BaseValueObject):
    value: UUID

    def validate(self):
        if self.value is None:
            raise ValueError("Id cannot be None")

        try:
            UUID(str(self.value))
        except ValueError:
            raise ValueError("Id must be correct")

    @classmethod
    def generate(cls):
        return Id(uuid4())


@dataclass(frozen=True, slots=True)
class IdempotencyKey(BaseValueObject):
    value: UUID

    def validate(self):
        if self.value is None:
            raise ValueError("IdempotencyKey cannot be None")

        try:
            UUID(str(self.value))
        except ValueError:
            raise ValueError("IdempotencyKey must be correct")
