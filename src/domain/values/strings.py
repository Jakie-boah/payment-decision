from dataclasses import dataclass
from urllib.parse import urlparse

from src.domain.values.base import BaseValueObject


MAX_DESCRIPTION_LENGTH = 500


@dataclass(frozen=True, slots=True)
class Description(BaseValueObject):
    value: str

    def validate(self):
        if len(self.value) > MAX_DESCRIPTION_LENGTH:
            raise ValueError("Description too long")


    @classmethod
    def default(cls):
        return Description("N/A")


@dataclass(frozen=True, slots=True)
class Webhook(BaseValueObject):
    value: str

    def validate(self):
        parsed = urlparse(self.value)
        if not parsed.scheme or not parsed.netloc:
            raise ValueError("Webhook URL must have scheme and netloc")
