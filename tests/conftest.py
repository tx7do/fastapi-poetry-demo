import pytest
from httpx import AsyncClient
from tortoise import Tortoise
from tortoise.contrib.test import finalizer, initializer

from app.main import app


async def init_db() -> None:
    """Initial database connection"""
    await Tortoise.init(
        db_url="sqlite://:memory:",
        modules={"models": ["app.models"]},
        _create_db=True,
        timezone="Asia/Shanghai",
        use_tz=True,
    )
    # print(f"Database created!")
    await Tortoise.generate_schemas()
    # print("Success to generate schemas")


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session")
async def client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        print("Client is ready")
        yield client


@pytest.fixture(scope="function", autouse=True)
async def initialize_tests(request):
    # print("initialize_tests----------------->")

    # initializer(modules={"models": ["app.models"]}, db_url="sqlite://:memory:")
    # request.addfinalizer(finalizer)

    await init_db()
    yield
    await Tortoise._drop_databases()
