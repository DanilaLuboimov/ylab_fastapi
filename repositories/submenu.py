from fastapi import HTTPException
from sqlalchemy import distinct, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from cache_redis.events import create_new_cache, delete_cache, get_cache_response
from db.tables import Dish, Submenu
from models.submenu import MainSubmenu, SubmenuIn, SubmenuUpdate


class SubmenuRepository:
    @staticmethod
    async def get_all(session: AsyncSession, m_id: str) -> list:
        stmt = (
            select(
                Submenu.id,
                Submenu.title,
                Submenu.description,
                func.count(distinct(Dish.id)).label("dishes_count"),
            )
            .outerjoin(
                Dish,
                Dish.submenu_id == Submenu.id,
            )
            .where(
                Submenu.menu_id == m_id,
            )
            .group_by(Submenu.id)
        )

        result = await session.execute(stmt)

        answer = result.all()
        return answer

    @staticmethod
    async def get_by_id(
        session: AsyncSession,
        m_id: str,
        sm_id: str,
    ) -> MainSubmenu | dict:
        cache = await get_cache_response(sm_id)

        if cache:
            return cache

        stmt = (
            select(
                Submenu.id,
                Submenu.title,
                Submenu.description,
                func.count(distinct(Dish.id)).label("dishes_count"),
            )
            .outerjoin(
                Dish,
                Dish.submenu_id == Submenu.id,
            )
            .where(
                Submenu.menu_id == m_id,
            )
            .where(
                Submenu.id == sm_id,
            )
            .group_by(Submenu.id)
        )

        result = await session.execute(stmt)

        record = result.one_or_none()

        if record is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="submenu not found",
            )

        cache_dict = MainSubmenu.parse_obj(record).dict()
        await create_new_cache(cache_dict, sm_id)
        return record

    @staticmethod
    async def create(
        session: AsyncSession,
        m_id: str,
        sm: SubmenuIn,
    ) -> MainSubmenu:
        new_record = MainSubmenu(
            title=sm.title,
            description=sm.description,
        )

        new_submenu = Submenu(
            id=new_record.id,
            title=new_record.title,
            description=new_record.description,
            menu_id=m_id,
        )

        session.add(new_submenu)
        await session.flush()

        await create_new_cache(new_record.dict())
        await delete_cache(m_id)
        return new_record

    async def patch(
        self,
        session: AsyncSession,
        m_id: str,
        sm_id: str,
        sm: SubmenuUpdate,
    ) -> MainSubmenu | dict:
        stmt = (
            update(
                Submenu,
            )
            .where(
                Submenu.id == sm_id,
            )
            .where(
                Submenu.menu_id == m_id,
            )
            .values(
                **sm.dict(),
            )
        )

        await session.execute(stmt)

        await delete_cache(sm_id)

        patch_record = await self.get_by_id(
            session=session,
            m_id=m_id,
            sm_id=sm_id,
        )

        cache_dict = MainSubmenu.parse_obj(patch_record).dict()
        await create_new_cache(cache_dict, sm_id)
        await delete_cache(m_id)

        return patch_record

    async def delete(
        self,
        session: AsyncSession,
        m_id: str,
        sm_id: str,
    ) -> dict:
        record = await self.__get_by_id(
            session=session,
            m_id=m_id,
            sm_id=sm_id,
        )

        await session.delete(record)

        await delete_cache(m_id)
        await delete_cache(sm_id)
        return {"status": True, "message": "The submenu has been deleted"}

    @staticmethod
    async def __get_by_id(session: AsyncSession, m_id: str, sm_id: str):
        stmt = (
            select(
                Submenu,
            )
            .where(
                Submenu.menu_id == m_id,
            )
            .where(
                Submenu.id == sm_id,
            )
        )

        result = await session.scalar(stmt)

        if result is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="submenu not found",
            )

        return result
