from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.interfaces.postgres.uow import UnitOfWork


class ImplUnitOfWork(UnitOfWork):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def commit(self) -> None:
        try:
            await self.session.commit()

        except SQLAlchemyError:
            await self.rollback()
            raise

    async def rollback(self) -> None:
        await self.session.rollback()
