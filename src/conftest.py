from main import app
import pytest
from httpx import AsyncClient


@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url='http://test') as ac:
        yield ac
