from fastapi import HTTPException
from starlette import status

from cache_redis.events import create_new_cache, delete_cache, get_cache_response
from db.tables import dish
from models.dish import Dish, DishIn

from .base import BaseRepository


class DishRepository(BaseRepository):
    async def get_all(self, sm_id: str) -> list:
        query = dish.select().where(dish.c.submenu_id == sm_id)
        return await self.database.fetch_all(query)

    async def create(self, m_id: str, sm_id: str, d: DishIn) -> Dish:
        new_record = Dish(
            title=d.title,
            description=d.description,
            price='%.2f' % float(d.price),
        )

        values = {**new_record.dict()}

        await create_new_cache(values)
        await delete_cache(m_id)
        await delete_cache(sm_id)

        query = dish.insert().values(**values)
        await self.database.execute(query, {'submenu_id': sm_id})
        return values

    async def patch(self, m_id: str, sm_id: str, d_id: str, d: DishIn) -> \
            Dish | None:
        answer = Dish(
            id=d_id,
            title=d.title,
            description=d.description,
            price='%.2f' % float(d.price),
        )

        values = {**answer.dict()}

        await create_new_cache(values)
        await delete_cache(m_id)
        await delete_cache(sm_id)

        values.pop('id')

        query = dish.update().where(dish.c.id == d_id).values(**values)
        await self.database.execute(query)
        return await self.get_by_id(d_id)

    async def delete(self, m_id: str, sm_id: str, d_id: str) -> dict:
        query = dish.delete().where(dish.c.id == d_id)
        await self.database.execute(query=query)
        await delete_cache(m_id)
        await delete_cache(sm_id)
        await delete_cache(d_id)
        return {'status': True, 'message': 'The dish has been deleted'}

    async def get_by_id(self, d_id: str) -> Dish | None:
        data = await get_cache_response(d_id)

        if data:
            return data

        query = dish.select().where(dish.c.id == d_id)
        record = await self.database.fetch_one(query=query)

        if record is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='dish not found',
            )

        data = Dish.parse_obj(record)
        await create_new_cache(data.dict(), d_id)
        return data
