import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.infrastructure.postgres.tables import metadata
from src.infrastructure.postgres.uow import ImplUnitOfWork

import pytest


@pytest_asyncio.fixture(scope="session")
async def engine(config):
    engine = create_async_engine(config.db_dsn, echo=False, pool_pre_ping=True)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture(scope="session")
async def session_maker(engine):
    return async_sessionmaker(bind=engine, expire_on_commit=False)


@pytest_asyncio.fixture(scope="function", autouse=True)
async def setup_db(engine, logger):
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def session(engine):
    async_session = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    async with async_session() as session:
        yield session


@pytest.fixture(scope="function")
def uow(session):
    return ImplUnitOfWork(session)
