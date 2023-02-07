from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from cache_redis.events import create_new_cache, delete_cache, get_cache_response
from models.submenu import MainSubmenu, SubmenuIn, SubmenuUpdate
from repositories.submenu import SubmenuRepository

from .depends import get_session


class SubmenuService:
    def __init__(
        self,
        submenu_rep: SubmenuRepository = Depends(),
        session: AsyncSession = Depends(get_session),
    ):
        self.submenu_rep = submenu_rep
        self.session = session

    async def get_all(self, m_id: str) -> list:
        submenus = await self.submenu_rep.get_all(session=self.session, m_id=m_id)
        return submenus

    async def create(
        self,
        m_id: str,
        sm: SubmenuIn,
    ) -> MainSubmenu:
        submenu = await self.submenu_rep.create(
            session=self.session,
            m_id=m_id,
            sm=sm,
        )

        await create_new_cache(dictionary=submenu.dict())
        await delete_cache(name=m_id)
        return submenu

    async def get_by_id(
        self,
        m_id: str,
        sm_id: str,
    ) -> MainSubmenu | dict:
        cache = await get_cache_response(name=sm_id)

        if cache:
            return cache

        submenu, cache_dict = await self.submenu_rep.get_by_id(
            session=self.session,
            m_id=m_id,
            sm_id=sm_id,
        )

        if not submenu:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="submenu not found",
            )

        await create_new_cache(dictionary=cache_dict, name=sm_id)
        return submenu

    async def patch(
        self,
        m_id: str,
        sm_id: str,
        sm: SubmenuUpdate,
    ) -> MainSubmenu | dict:
        cache = await get_cache_response(name=sm_id)

        if not cache:
            check = await self.submenu_rep.check_by_id(
                session=self.session,
                m_id=m_id,
                sm_id=sm_id,
            )
            if not check:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="submenu not found",
                )

        await self.submenu_rep.patch(
            session=self.session,
            m_id=m_id,
            sm_id=sm_id,
            sm=sm,
        )

        await delete_cache(name=sm_id)
        await delete_cache(name=m_id)

        submenu, cache_dict = await self.submenu_rep.get_by_id(
            session=self.session,
            m_id=m_id,
            sm_id=sm_id,
        )

        if not submenu:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="submenu not found",
            )

        await create_new_cache(dictionary=cache_dict, name=sm_id)
        return submenu

    async def delete(self, m_id: str, sm_id: str) -> dict:
        cache = await get_cache_response(name=sm_id)

        if cache:
            await delete_cache(name=sm_id)

        check = await self.submenu_rep.check_by_id(
            session=self.session,
            m_id=m_id,
            sm_id=sm_id,
        )
        if not check:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="submenu not found",
            )

        await self.submenu_rep.delete(session=self.session, record=check)

        await delete_cache(name=m_id)
        return {"status": True, "message": "The submenu has been deleted"}
