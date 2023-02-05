from fastapi import HTTPException
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from cache_redis.events import create_new_cache, delete_cache, get_cache_response
from db.tables import Dish
from models.dish import DishIn, DishUpdate, MainDish


class DishRepository:
    @staticmethod
    async def get_all(session: AsyncSession, sm_id: str) -> list:
        stmt = select(
            Dish.id,
            Dish.title,
            Dish.description,
            Dish.price,
        ).where(
            Dish.submenu_id == sm_id,
        )

        result = await session.execute(stmt)

        answer = result.all()
        return answer

    @staticmethod
    async def create(
        session: AsyncSession,
        m_id: str,
        sm_id: str,
        d: DishIn,
    ) -> MainDish:
        new_record = MainDish(
            title=d.title,
            description=d.description,
            price=d.price,
        )

        new_dish = Dish(
            id=new_record.id,
            title=new_record.title,
            description=new_record.description,
            price=new_record.price,
            submenu_id=sm_id,
        )

        session.add(new_dish)
        await session.flush()

        await create_new_cache(new_record.dict())
        await delete_cache(m_id)
        await delete_cache(sm_id)

        return new_record

    async def patch(
        self,
        session: AsyncSession,
        m_id: str,
        sm_id: str,
        d_id: str,
        d: DishUpdate,
    ) -> MainDish | dict:
        await self.__get_by_id(session=session, d_id=d_id)

        stmt = (
            update(
                Dish,
            )
            .where(
                Dish.id == d_id,
            )
            .values(
                **d.dict(),
            )
        )

        await session.execute(stmt)

        await delete_cache(d_id)

        patch_record = await self.get_by_id(session=session, d_id=d_id)

        cache_dict = MainDish.parse_obj(patch_record).dict()
        await create_new_cache(cache_dict, d_id)
        await delete_cache(m_id)
        await delete_cache(sm_id)

        return patch_record

    async def delete(
        self,
        session: AsyncSession,
        m_id: str,
        sm_id: str,
        d_id: str,
    ) -> dict:
        record = await self.__get_by_id(session=session, d_id=d_id)

        await session.delete(record)
        await delete_cache(m_id)
        await delete_cache(sm_id)
        await delete_cache(d_id)
        return {"status": True, "message": "The dish has been deleted"}

    @staticmethod
    async def get_by_id(session: AsyncSession, d_id: str) -> MainDish | dict:
        cache = await get_cache_response(d_id)

        if cache:
            return cache

        stmt = select(
            Dish.id,
            Dish.title,
            Dish.description,
            Dish.price,
        ).where(
            Dish.id == d_id,
        )

        result = await session.execute(stmt)

        record = result.one_or_none()

        if record is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="dish not found",
            )

        cache_dict = MainDish.parse_obj(record).dict()
        await create_new_cache(cache_dict, d_id)
        return record

    @staticmethod
    async def __get_by_id(
        session: AsyncSession,
        d_id: str,
    ) -> Dish:
        stmt = select(
            Dish,
        ).where(
            Dish.id == d_id,
        )

        result = await session.scalar(stmt)

        if result is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="dish not found",
            )

        return result
