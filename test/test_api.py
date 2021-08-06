import pytest
from asgi_lifespan import LifespanManager
from httpx import AsyncClient
from src.server import app


@pytest.fixture()
async def client():
    async with AsyncClient(app=app, base_url="http://test") as client, LifespanManager(app):
        yield client


@pytest.mark.asyncio
async def test_read_main(client):
    response = await client.get("/")
    assert response.status_code == 200
    # assert response.json() == {"msg": "Hello World"}
