from typing import Optional
from db.tables import submenu
from models.submenu import Submenu, SubmenuIn
from .base import BaseRepository
from sqlalchemy import text


class SubmenuRepository(BaseRepository):
    async def get_all(self, m_id: str) -> list:
        query = text(
            f"""SELECT s.*, COUNT(DISTINCT d.id) AS dishes_count
            FROM submenu AS s
            LEFT JOIN dish AS d ON d.submenu_id = s.id
            WHERE s.menu_id = '{m_id}'
            GROUP BY s.id
            """
        )
        return await self.database.fetch_all(query)

    async def get_by_id(self, m_id: str, sm_id: str) -> Optional[Submenu]:
        query = text(
            f"""SELECT s.*, COUNT(DISTINCT d.id) AS dishes_count
            FROM submenu AS s
            LEFT JOIN dish AS d ON d.submenu_id = s.id
            WHERE s.menu_id = '{m_id}'
            AND s.id = '{sm_id}'
            GROUP BY s.id
            """
        )

        sm = await self.database.fetch_one(query)

        if sm is None:
            return None
        return Submenu.parse_obj(sm)

    async def create(self, m_id: str, sm: SubmenuIn) -> Submenu:
        new_record = Submenu(
            title=sm.title,
            description=sm.description
        )

        values = {**new_record.dict()}
        values.pop("dishes_count")

        query = submenu.insert().values(**values)

        await self.database.execute(query, {"menu_id": f"{m_id}"})
        return values

    async def patch(self, m_id: str, sm_id: str, sm: SubmenuIn) -> Optional[Submenu]:
        answer = Submenu(
            id=sm_id,
            title=sm.title,
            description=sm.description
        )

        values = {**answer.dict()}
        values.pop("id")
        values.pop("dishes_count")

        query = submenu.update().where(submenu.c.id == sm_id).values(**values)
        await self.database.execute(query)
        return await self.get_by_id(m_id, sm_id)

    async def delete(self, sm_id: str) -> None:
        query = submenu.delete().where(submenu.c.id == sm_id)
        return await self.database.execute(query=query)


