import asyncio
import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from httpx import AsyncClient
from typing import Generator
from main import app
from db.base import database
from sqlalchemy import text
from core.config import DATABASE_URL
from sqlalchemy import create_engine

engine = create_engine(DATABASE_URL)


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def async_client() -> AsyncClient:
    async with LifespanManager(app):
        async with AsyncClient(app=app, base_url="http://test") as client:
            yield client


@pytest_asyncio.fixture
async def create_menu():
    query = text(
        """
        INSERT INTO menu (id, title, description)
        VALUES ('62b74c7e-5913-4fe8-a524-9e0280828c97',
        'TEST menu 1', 'TEST menu description 1')
        """
    )
    await database.execute(query)


@pytest_asyncio.fixture()
async def create_submenu():
    query = text(
        """
        INSERT INTO submenu (id, title, description, menu_id)
        VALUES ('cbcc0a55-8225-4053-9f71-acd65371ee9c',
        'TEST submenu 1', 'TEST submenu description 1',
        '62b74c7e-5913-4fe8-a524-9e0280828c97')
        """
    )
    await database.execute(query)


@pytest_asyncio.fixture
async def create_dish():
    query = text(
        """
        INSERT INTO dish (id, title, description, price, submenu_id)
        VALUES ('f7811d6d-bcc3-45f3-93ce-1343a7f6b34d',
        'TEST dish 1', 'TEST dish description 1', '13.3535',
        'cbcc0a55-8225-4053-9f71-acd65371ee9c')
        """
    )
    await database.execute(query)
