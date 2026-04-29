import pytest_asyncio
from src.presentation.http_api.main import create_container


@pytest_asyncio.fixture
async def container(config):
    container_ = create_container(config)
    async with container_() as c:
        yield c
    await container_.close()
