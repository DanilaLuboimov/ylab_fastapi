from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from cache_redis.events import create_new_cache, delete_cache, \
    get_cache_response
from models.menu import MainMenu, MenuIn, MenuUpdate
from repositories.menu import MenuRepository

from .depends import get_session


class MenuService:
    def __init__(
        self,
        menu_rep: MenuRepository = Depends(),
        session: AsyncSession = Depends(get_session),
    ):
        self.menu_rep = menu_rep
        self.session = session

    async def get_all(self) -> list:
        menus = await self.menu_rep.get_all(session=self.session)
        return menus

    async def create(self, m: MenuIn) -> MainMenu:
        menus = await self.menu_rep.create(
            session=self.session,
            m=m,
        )
        await create_new_cache(dictionary=menus.dict())
        return menus

    async def get_by_id(self, m_id: str) -> MainMenu | dict:
        cache = await get_cache_response(name=m_id)

        if cache:
            return cache

        menu, cache_dict = await self.menu_rep.get_by_id(
            session=self.session, m_id=m_id
        )

        if not menu:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="menu not found",
            )

        await create_new_cache(dictionary=cache_dict)

        return menu

    async def patch(
        self,
        m_id: str,
        m: MenuUpdate,
    ) -> MainMenu | dict:
        cache = await get_cache_response(name=m_id)

        if not cache:
            check = await self.menu_rep.check_by_id(
                session=self.session,
                m_id=m_id,
            )

            if not check:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="menu not found",
                )

        await self.menu_rep.patch(
            session=self.session,
            m_id=m_id,
            m=m,
        )

        await delete_cache(name=m_id)

        menus, cache_dict = await self.menu_rep.get_by_id(
            session=self.session, m_id=m_id
        )

        if not menus:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="menu not found",
            )

        await create_new_cache(dictionary=cache_dict, name=m_id)
        return menus

    async def delete(self, m_id: str) -> dict:
        cache = await get_cache_response(name=m_id)

        if cache:
            await delete_cache(m_id)

        check = await self.menu_rep.check_by_id(
            session=self.session, m_id=m_id
        )

        if check is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="menu not found",
            )

        await self.menu_rep.delete(session=self.session, record=check)
        return {"status": True, "message": "The menu has been deleted"}
