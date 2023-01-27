from copy import copy

from fastapi import HTTPException
from sqlalchemy import text
from starlette import status

from cache_redis.events import create_new_cache, delete_cache, get_cache_response
from db.tables import submenu
from models.submenu import Submenu, SubmenuIn

from .base import BaseRepository


class SubmenuRepository(BaseRepository):
    async def get_all(self, m_id: str) -> list:
        query = text(
            f"""SELECT s.*, COUNT(DISTINCT d.id) AS dishes_count
            FROM submenu AS s
            LEFT JOIN dish AS d ON d.submenu_id = s.id
            WHERE s.menu_id = '{m_id}'
            GROUP BY s.id
            """,
        )
        return await self.database.fetch_all(query)

    async def get_by_id(self, m_id: str, sm_id: str) -> Submenu | None:
        data = await get_cache_response(sm_id)

        if data:
            return data

        query = text(
            f"""SELECT s.*, COUNT(DISTINCT d.id) AS dishes_count
            FROM submenu AS s
            LEFT JOIN dish AS d ON d.submenu_id = s.id
            WHERE s.menu_id = '{m_id}'
            AND s.id = '{sm_id}'
            GROUP BY s.id
            """,
        )

        record = await self.database.fetch_one(query=query)

        if record is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='submenu not found',
            )

        data = Submenu.parse_obj(record)
        await create_new_cache(data.dict(), sm_id)

        return data

    async def create(self, m_id: str, sm: SubmenuIn) -> Submenu:
        new_record = Submenu(
            title=sm.title,
            description=sm.description,
        )

        values = {**new_record.dict()}

        await create_new_cache(copy(values))
        await delete_cache(m_id)

        values.pop('dishes_count')

        query = submenu.insert().values(**values)

        await self.database.execute(query, {'menu_id': f'{m_id}'})
        return values

    async def patch(self, m_id: str, sm_id: str, sm: SubmenuIn) -> \
            Submenu | None:
        answer = Submenu(
            id=sm_id,
            title=sm.title,
            description=sm.description,
        )

        values = {**answer.dict()}

        await create_new_cache(copy(values))
        await delete_cache(m_id)

        values.pop('id')
        values.pop('dishes_count')

        query = submenu.update().where(submenu.c.id == sm_id).values(**values)
        await self.database.execute(query)
        return await self.get_by_id(m_id, sm_id)

    async def delete(self, m_id: str, sm_id: str) -> dict:
        query = submenu.delete().where(submenu.c.id == sm_id)
        await self.database.execute(query=query)
        await delete_cache(m_id)
        await delete_cache(sm_id)
        return {'status': True, 'message': 'The submenu has been deleted'}
