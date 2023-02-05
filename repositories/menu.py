from fastapi import HTTPException
from sqlalchemy import distinct, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from cache_redis.events import create_new_cache, delete_cache, get_cache_response
from db.tables import Dish, Menu, Submenu
from models.menu import MainMenu, MenuIn, MenuUpdate


class MenuRepository:
    @staticmethod
    async def get_all(session: AsyncSession) -> list:
        stmt = (
            select(
                Menu.id,
                Menu.title,
                Menu.description,
                func.count(distinct(Submenu.id)).label("submenus_count"),
                func.count(distinct(Dish.id)).label("dishes_count"),
            )
            .outerjoin(
                Submenu,
                Submenu.menu_id == Menu.id,
            )
            .outerjoin(
                Dish.id,
                Dish.submenu_id == Submenu.id,
            )
            .group_by(Menu.id)
        )

        result = await session.execute(stmt)

        answer = result.all()
        return answer

    @staticmethod
    async def create(session: AsyncSession, m: MenuIn) -> MainMenu:
        new_record = MainMenu(
            title=m.title,
            description=m.description,
        )

        new_menu = Menu(
            id=new_record.id,
            title=new_record.title,
            description=new_record.description,
        )

        session.add(new_menu)
        await session.flush()

        await create_new_cache(new_record.dict())
        return new_record

    async def patch(
        self,
        session: AsyncSession,
        m_id: str,
        m: MenuUpdate,
    ) -> MainMenu | dict:
        await self.__get_by_id(session=session, m_id=m_id)

        stmt = (
            update(
                Menu,
            )
            .where(
                Menu.id == m_id,
            )
            .values(
                **m.dict(),
            )
        )

        await session.execute(stmt)

        await delete_cache(m_id)

        patch_record = await self.get_by_id(session=session, m_id=m_id)

        cache_dict = MainMenu.parse_obj(patch_record).dict()
        await create_new_cache(cache_dict, m_id)

        return patch_record

    async def delete(self, session: AsyncSession, m_id: str) -> dict:
        record = await self.__get_by_id(session, m_id)

        await session.delete(record)

        await delete_cache(m_id)
        return {"status": True, "message": "The menu has been deleted"}

    @staticmethod
    async def get_by_id(
        session: AsyncSession,
        m_id: str,
    ) -> MainMenu | dict:
        cache = await get_cache_response(m_id)

        if cache:
            return cache

        stmt = (
            select(
                Menu.id,
                Menu.title,
                Menu.description,
                func.count(distinct(Submenu.id)).label("submenus_count"),
                func.count(distinct(Dish.id)).label("dishes_count"),
            )
            .outerjoin(
                Submenu,
                Submenu.menu_id == Menu.id,
            )
            .outerjoin(
                Dish.id,
                Dish.submenu_id == Submenu.id,
            )
            .where(
                Menu.id == m_id,
            )
            .group_by(Menu.id)
        )

        result = await session.execute(stmt)

        record = result.one_or_none()

        if record is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="menu not found",
            )

        cache_dict = MainMenu.parse_obj(record).dict()
        await create_new_cache(cache_dict, m_id)
        return record

    @staticmethod
    async def __get_by_id(session: AsyncSession, m_id: str) -> Menu:
        stmt = select(
            Menu,
        ).where(
            Menu.id == m_id,
        )

        result = await session.scalar(stmt)

        if result is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="menu not found",
            )

        return result
