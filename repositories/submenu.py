from sqlalchemy import distinct, func, select, update
from sqlalchemy.engine.row import Row
from sqlalchemy.ext.asyncio import AsyncSession

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
    ) -> tuple[Row | None, dict | None]:
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

        if not record:
            return None, None

        cache_dict = MainSubmenu.parse_obj(record).dict()

        return record, cache_dict

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
        return new_record

    @staticmethod
    async def patch(
        session: AsyncSession,
        m_id: str,
        sm_id: str,
        sm: SubmenuUpdate,
    ) -> None:
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

    @staticmethod
    async def delete(
        session: AsyncSession,
        record,
    ) -> None:
        await session.delete(record)

    @staticmethod
    async def check_by_id(session: AsyncSession, m_id: str, sm_id: str):
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
        return result
