import pytest
import pytest_asyncio
from src.application.use_cases.create_payment import CreatePaymentUseCase


@pytest_asyncio.fixture
async def use_case(container):
    return await container.get(CreatePaymentUseCase)


@pytest.mark.asyncio
async def test_create_payment_use_case(use_case, logger):
    assert use_case
    assert use_case.logger
    logger.info(use_case)
