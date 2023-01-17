from typing import Optional
from db.tables import dish
from models.dish import Dish, DishIn
from .base import BaseRepository


class DishRepository(BaseRepository):
    async def get_all(self, m_id: str, sm_id: str) -> list:
        query = dish.select().where(dish.c.submenu_id == sm_id)
        return await self.database.fetch_all(query)

    async def create(self, m_id: str, sm_id: str, d: DishIn) -> Dish:
        new_record = Dish(
            title=d.title,
            description=d.description,
            price=d.price
        )

        values = {**new_record.dict()}
        query = dish.insert().values(**values)
        await self.database.execute(query, {"submenu_id": sm_id})
        return values

    async def patch(self, d_id: int, d: DishIn) -> Optional[Dish]:
        answer = Dish(
            id=d_id,
            title=d.title,
            description=d.description,
            price=d.price
        )

        values = {**answer.dict()}
        values.pop("id")

        query = dish.update().where(dish.c.id == d_id).values(**values)
        await self.database.execute(query)
        return await self.get_by_id(d_id)

    async def delete(self, d_id: int) -> None:
        query = dish.delete().where(dish.c.id == d_id)
        return await self.database.execute(query=query)

    async def get_by_id(self, d_id: int) -> Optional[Dish]:
        query = dish.select().where(dish.c.id == d_id)

        d = await self.database.fetch_one(query=query)

        if d is None:
            return None
        return Dish.parse_obj(d)
