import asyncio
import os
from typing import Generator

import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from core.config import DATABASE_URL
from db.tables import Base, Dish, Menu, Submenu
from main import app

test_engine = create_async_engine(
    DATABASE_URL,
)

session = sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


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


@pytest_asyncio.fixture(scope="session")
async def async_session(a_session=session) -> AsyncSession:
    async with a_session() as s:
        async with test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        async with s.begin():
            test_menu = Menu(
                id=os.getenv("MENU_ID"),
                title="TEST menu 1",
                description="TEST menu description 1",
            )
            test_submenu = Submenu(
                id=os.getenv("SUBMENU_ID"),
                title="TEST submenu 1",
                description="TEST submenu description 1",
                menu_id=os.getenv("MENU_ID"),
            )
            test_dish = Dish(
                id=os.getenv("DISH_ID"),
                title="TEST dish 1",
                description="TEST dish description 1",
                price="13.3535",
                submenu_id=os.getenv("SUBMENU_ID"),
            )
            s.add(test_menu)
            await s.flush()
            s.add(test_submenu)
            await s.flush()
            s.add(test_dish)
            await s.flush()
        yield s

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await test_engine.dispose()
