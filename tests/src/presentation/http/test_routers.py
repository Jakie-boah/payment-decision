import uuid

import aiohttp

import pytest_asyncio
import pytest


@pytest_asyncio.fixture
async def http_session():
    async with aiohttp.ClientSession() as session:
        yield session


@pytest.mark.asyncio
async def test_request(http_session, logger):
    url = "http://api:8001/api/v1/payments"

    header = {
        "Idempotency-Key": str(uuid.uuid4()),
    }

    data = {
        "amount": 100,
        "currency": "EUR",
        "webhook_url": "https://example.com",
        "meta_data": None,
        "description": "some"
    }

    async with http_session.post(url, headers=header, json=data) as response:
        data1 = await response.json()
        logger.info(data1)
        assert response.status == 200

    async with http_session.post(url, headers=header, json=data) as response:
        data2 = await response.json()
        logger.info(data2)
        assert response.status == 200

    assert data1 == data2