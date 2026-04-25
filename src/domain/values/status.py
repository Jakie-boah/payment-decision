from src.domain.values.base import BaseValueObject
from dataclasses import dataclass

from enum import StrEnum


class Status(StrEnum):
    PENDING = "pending"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    NOT_SET = "not_set"
