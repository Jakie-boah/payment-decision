from abc import ABC, abstractmethod
from typing import TypeVar


T = TypeVar("T")


class Repository[T](ABC):
    @abstractmethod
    async def save(self, domain: T): ...

    @abstractmethod
    async def filter(self) -> list[T]: ...

    @abstractmethod
    async def update(self, domain: T): ...

    @abstractmethod
    async def get(self, uid) -> T: ...

