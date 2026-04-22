from src.domain.values.base import BaseValueObject
from dataclasses import dataclass

from enum import StrEnum


class StatusChoices(StrEnum):
    PENDING = "pending"
    SUCCEEDED = "succeeded"
    FAILED = "failed"


@dataclass(frozen=True, slots=True)
class Status(BaseValueObject):
    value: str

    def validate(self):
        if self.value not in StatusChoices:
            raise ValueError(
                f"Status {self.value} is not valid.\nChoose from {StatusChoices._value2member_map_.values()}"
            )
