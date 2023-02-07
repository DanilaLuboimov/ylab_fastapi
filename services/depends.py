from typing import AsyncGenerator

from db.base import async_session


async def get_session() -> AsyncGenerator:
    async with async_session() as session:
        async with session.begin():
            yield session
