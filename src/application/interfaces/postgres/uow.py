from typing import Protocol

from src.application.interfaces.postgres.repository import Repository


class UnitOfWork(Protocol):
    outbox: Repository
    payment: Repository

    async def commit(self): ...

    async def rollback(self): ...
