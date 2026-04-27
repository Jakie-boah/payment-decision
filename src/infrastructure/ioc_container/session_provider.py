from collections.abc import AsyncIterable

from dishka import Provider, Scope, from_context, provide
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.application.interfaces.postgres.reader import PaymentReader
from src.infrastructure.config.config_storage import Config
from src.infrastructure.postgres.reader.payment import ImplPaymentReader
from src.infrastructure.postgres.uow import ImplUnitOfWork
from src.application.interfaces.postgres.uow import UnitOfWork


class SessionProvider(Provider):
    context = from_context(provides=Config, scope=Scope.APP)

    @provide(scope=Scope.APP)
    async def engine(self, config: Config) -> AsyncIterable[AsyncEngine]:
        engine = create_async_engine(
            config.db_dsn,
            echo=False,
            pool_size=50,
            max_overflow=50,
            pool_timeout=30,
            pool_pre_ping=True,
        )
        yield engine
        await engine.dispose()

    @provide(scope=Scope.APP)
    async def session_poll(self, engine: AsyncEngine) -> async_sessionmaker:
        return async_sessionmaker(bind=engine, expire_on_commit=False)

    @provide(scope=Scope.REQUEST)
    async def get_session(
            self,
            session_poll: async_sessionmaker,
    ) -> AsyncIterable[AsyncSession]:
        session = session_poll()
        yield session
        await session.close()

    @provide(scope=Scope.REQUEST)
    async def get_uow_instance(self, session: AsyncSession) -> UnitOfWork:
        return ImplUnitOfWork(session=session)

    @provide(scope=Scope.REQUEST)
    async def get_reader(self, session: AsyncSession) -> PaymentReader:
        return ImplPaymentReader(session=session)
