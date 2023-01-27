from copy import copy

from fastapi import HTTPException
from sqlalchemy import text
from starlette import status

from cache_redis.events import create_new_cache, delete_cache, get_cache_response
from db.tables import menu
from models.menu import Menu, MenuIn

from .base import BaseRepository


class MenuRepository(BaseRepository):
    async def get_all(self) -> list:
        query = text(
            """
                SELECT m.*, COUNT(DISTINCT s.id)
                AS submenus_count, COUNT(DISTINCT d.id) AS dishes_count
                FROM menu AS m
                LEFT JOIN submenu AS s ON s.menu_id = m.id
                LEFT JOIN dish AS d ON d.submenu_id = s.id
                GROUP BY m.id
            """,
        )
        return await self.database.fetch_all(query)

    async def create(self, m: MenuIn) -> Menu:
        new_record = Menu(
            title=m.title,
            description=m.description,
        )

        values = {**new_record.dict()}

        await create_new_cache(copy(values))

        values.pop('submenus_count')
        values.pop('dishes_count')
        query = menu.insert().values(**values)
        await self.database.execute(query)
        return values

    async def patch(self, m_id: int, m: MenuIn) -> Menu | None:
        await self.get_by_id(m_id)

        answer = Menu(
            id=m_id,
            title=m.title,
            description=m.description,
        )

        values = {**answer.dict()}

        await create_new_cache(values, m_id)

        values.pop('id')
        values.pop('submenus_count')
        values.pop('dishes_count')

        query = menu.update().where(menu.c.id == m_id).values(**values)
        await self.database.execute(query)
        return await self.get_by_id(m_id)

    async def delete(self, m_id: int) -> dict:
        query = menu.delete().where(menu.c.id == m_id)
        await self.database.execute(query=query)
        await delete_cache(m_id)
        return {'status': True, 'message': 'The menu has been deleted'}

    async def get_by_id(self, m_id: int) -> Menu | None:
        data = await get_cache_response(m_id)

        if data:
            return data

        query = text(
            f"""
                SELECT m.*, COUNT(DISTINCT s.id)
                AS submenus_count, COUNT(DISTINCT d.id) AS dishes_count
                FROM menu AS m
                LEFT JOIN submenu AS s ON s.menu_id = m.id
                LEFT JOIN dish AS d ON d.submenu_id = s.id
                WHERE m.id = '{m_id}'
                GROUP BY m.id
            """,
        )

        record = await self.database.fetch_one(query=query)

        if record is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='menu not found',
            )

        data = Menu.parse_obj(record)
        await create_new_cache(data.dict(), m_id)

        return data
