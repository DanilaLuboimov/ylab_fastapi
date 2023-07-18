from sqlalchemy import distinct, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

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

        return new_record

    async def patch(
        self,
        session: AsyncSession,
        m_id: str,
        m: MenuUpdate,
    ) -> None:
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

    async def delete(self, session: AsyncSession, record) -> None:
        await session.delete(record)

    @staticmethod
    async def get_by_id(
        session: AsyncSession,
        m_id: str,
    ) -> tuple[MainMenu | None, dict | None]:
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

        if not record:
            return None, None

        cache_dict = MainMenu.parse_obj(record).dict()
        return record, cache_dict

    @staticmethod
    async def check_by_id(session: AsyncSession, m_id: str) -> Menu:
        stmt = select(
            Menu,
        ).where(
            Menu.id == m_id,
        )

        result = await session.scalar(stmt)
        return result
