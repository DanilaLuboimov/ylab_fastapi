from typing import Optional
from db.tables import menu
from models.menu import Menu, MenuIn
from .base import BaseRepository
from sqlalchemy import text


class MenuRepository(BaseRepository):
    async def get_all(self) -> list:
        query = text(
            """SELECT m.*, COUNT(DISTINCT s.id) AS submenus_count, COUNT(DISTINCT d.id) AS dishes_count
            FROM menu AS m
            LEFT JOIN submenu AS s ON s.menu_id = m.id
            LEFT JOIN dish AS d ON d.submenu_id = s.id
            GROUP BY m.id"""
        )
        return await self.database.fetch_all(query)

    async def create(self, m: MenuIn) -> Menu:
        new_record = Menu(
            title=m.title,
            description=m.description
        )

        values = {**new_record.dict()}
        values.pop("submenus_count")
        values.pop("dishes_count")
        query = menu.insert().values(**values)
        await self.database.execute(query)
        return values

    async def patch(self, m_id: int, m: MenuIn) -> Optional[Menu]:
        answer = Menu(
            id=m_id,
            title=m.title,
            description=m.description
        )

        values = {**answer.dict()}
        values.pop("id")
        values.pop("submenus_count")
        values.pop("dishes_count")

        query = menu.update().where(menu.c.id == m_id).values(**values)
        await self.database.execute(query)
        return await self.get_by_id(m_id)

    async def delete(self, m_id: int) -> None:
        query = menu.delete().where(menu.c.id == m_id)
        return await self.database.execute(query=query)

    async def get_by_id(self, m_id: int) -> Optional[Menu]:
        query = text(
            f"""SELECT m.*, COUNT(DISTINCT s.id) AS submenus_count, COUNT(DISTINCT d.id) AS dishes_count
            FROM menu AS m
            LEFT JOIN submenu AS s ON s.menu_id = m.id
            LEFT JOIN dish AS d ON d.submenu_id = s.id
            WHERE m.id = '{m_id}'
            GROUP BY m.id"""
        )

        m = await self.database.fetch_one(query=query)

        if m is None:
            return None
        return Menu.parse_obj(m)
