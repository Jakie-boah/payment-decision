from unittest.mock import patch

import pytest
import pytest_asyncio
from src.application.interfaces.payment.service import PaymentService
from src.infrastructure.payment.exceptions import PaymentError


@pytest_asyncio.fixture
async def service(container):
    return await container.get(PaymentService)


@pytest.mark.asyncio
async def test_payment_success(service, payment):
    with patch("src.infrastructure.payment.payment.random.randint", return_value=2):
        result = await service.process(payment)
        assert result is None


@pytest.mark.asyncio
async def test_payment_error(service, payment):
    with patch("src.infrastructure.payment.payment.random.randint", return_value=1), pytest.raises(PaymentError):
        await service.process(payment)
