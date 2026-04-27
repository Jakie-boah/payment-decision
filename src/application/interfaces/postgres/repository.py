from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class Repository(ABC, Generic[T]):
    @abstractmethod
    async def save(self, domain: T): ...

    @abstractmethod
    async def filter(self) -> list[T]: ...

    @abstractmethod
    async def update(self, domain: T): ...
