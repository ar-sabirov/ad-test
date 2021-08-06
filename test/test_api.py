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
    response200 = await client.get("/")
    response400 = await client.get("/?col=wtf")
    assert response200.status_code == 200
    assert response400.status_code == 400
