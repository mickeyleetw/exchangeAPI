from main import app
import pytest
from httpx import AsyncClient
from files.exchange_rate import get_exchange_map

mock_exchange_rate ={
    "currencies": {
        "TWD": {
            "TWD": 1,
            "JPY": 4
        },
        "JPY": {
            "TWD": 0.25,
            "JPY": 1
        }
    }
}


@pytest.fixture
def anyio_backend():
    return 'asyncio'


@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url='http://test') as ac:
        yield ac

@pytest.fixture
def exchange_map():
    return mock_exchange_rate

@pytest.fixture(autouse=True)
def override_exchange_map(exchange_map): 

    def get_test_exchange_map():
        return exchange_map

    app.dependency_overrides[get_exchange_map] = get_test_exchange_map