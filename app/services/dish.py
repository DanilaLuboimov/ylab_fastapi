from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from cache_redis.events import create_new_cache, delete_cache, get_cache_response
from models.dish import DishIn, DishUpdate, MainDish
from repositories.dish import DishRepository

from .depends import get_session


class DishService:
    def __init__(
        self,
        dish_rep: DishRepository = Depends(),
        session: AsyncSession = Depends(get_session),
    ):
        self.dish_rep = dish_rep
        self.session = session

    async def get_all(self, sm_id: str) -> list:
        dishes = await self.dish_rep.get_all(session=self.session, sm_id=sm_id)
        return dishes

    async def create(
        self,
        m_id: str,
        sm_id: str,
        d: DishIn,
    ) -> MainDish:
        dish = await self.dish_rep.create(
            session=self.session,
            sm_id=sm_id,
            d=d,
        )

        await create_new_cache(dictionary=dish.dict())
        await delete_cache(name=sm_id)
        await delete_cache(name=m_id)
        return dish

    async def patch(
        self,
        m_id: str,
        sm_id: str,
        d_id: str,
        d: DishUpdate,
    ) -> MainDish | dict:
        cache = await get_cache_response(name=d_id)

        if not cache:
            check = await self.dish_rep.check_by_id(
                session=self.session,
                d_id=d_id,
            )

            if not check:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="dish not found",
                )

        await self.dish_rep.patch(
            session=self.session,
            d_id=d_id,
            d=d,
        )

        await delete_cache(name=d_id)
        await delete_cache(name=sm_id)
        await delete_cache(name=m_id)

        dish, cache_dict = await self.dish_rep.get_by_id(
            session=self.session,
            d_id=d_id,
        )

        if not dish:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="dish not found",
            )

        await create_new_cache(dictionary=cache_dict, name=d_id)
        return dish

    async def get_by_id(self, d_id: str) -> MainDish | dict:
        cache = await get_cache_response(name=d_id)

        if cache:
            return cache

        dish, cache_dict = await self.dish_rep.get_by_id(
            session=self.session,
            d_id=d_id,
        )

        if not dish:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="dish not found",
            )

        await create_new_cache(dictionary=cache_dict, name=d_id)
        return dish

    async def delete(
        self,
        m_id: str,
        sm_id: str,
        d_id: str,
    ) -> dict:
        cache = await get_cache_response(name=d_id)

        if cache:
            await delete_cache(name=d_id)

        check = await self.dish_rep.check_by_id(
            session=self.session,
            d_id=d_id,
        )
        if not check:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="dish not found",
            )

        await self.dish_rep.delete(session=self.session, record=check)

        await delete_cache(name=m_id)
        await delete_cache(name=sm_id)
        return {"status": True, "message": "The dish has been deleted"}
