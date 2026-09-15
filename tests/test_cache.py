import pytest
from fastapi import FastAPI, Request
from httpx import AsyncClient, ASGITransport
from fastapi_cache_decorator import cache

call_counter = 0

@pytest.fixture
def app():
    global call_counter
    call_counter = 0
    fastapi_app = FastAPI()

    @fastapi_app.get("/data")
    @cache(ttl=10)
    async def get_data(request: Request):
        global call_counter
        call_counter += 1
        return {"counter": call_counter}

    return fastapi_app

@pytest.mark.asyncio
async def test_caching(app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Call 1: Miss (runs func)
        r1 = await client.get("/data")
        assert r1.status_code == 200
        assert r1.json()["counter"] == 1

        # Call 2: Hit (returns cached result)
        r2 = await client.get("/data")
        assert r2.status_code == 200
        assert r2.json()["counter"] == 1 # Still 1, didn't increment!
