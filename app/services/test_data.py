from typing import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.base import async_session
from repositories.test_data import TestDataRepository


async def get_session() -> AsyncGenerator:
    async with async_session() as session:
        async with session.begin():
            yield session


class TestDataService:
    def __init__(
        self,
        test_data_rep: TestDataRepository = Depends(),
        session: AsyncSession = Depends(get_session),
    ):
        self.test_data_rep = test_data_rep
        self.session = session

    async def create(self):
        menus = await self.test_data_rep.create(self.session)
        return menus
