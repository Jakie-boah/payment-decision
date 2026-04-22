from dataclasses import dataclass

from src.domain.values.base import BaseValueObject

MAX_DESCRIPTION_LENGTH = 500


@dataclass(frozen=True, slots=True)
class Description(BaseValueObject):
    value: str

    def validate(self):
        if len(self.value) > MAX_DESCRIPTION_LENGTH:
            raise ValueError("Description too long")
