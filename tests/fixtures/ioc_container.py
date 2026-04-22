from src.presentation.main import create_container
import pytest
import pytest_asyncio


@pytest_asyncio.fixture
async def container(config):
    container_ = create_container(config)
    async with container_() as c:
        yield c
    await container_.close()
