from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from db.tables import Dish, Menu, Submenu
from tasks.tasks import create_menu_excel


class FileRepository:
    @staticmethod
    async def create_file(session: AsyncSession) -> dict:
        dishes_group = (
            select(
                Submenu.id,
                func.json_agg(
                    func.json_build_object(
                        "title",
                        Dish.title,
                        "description",
                        Dish.description,
                        "price",
                        Dish.price,
                    )
                ).label("dishes"),
            )
            .select_from(Dish)
            .join(Submenu)
            .group_by(Submenu.id)
        ).cte("sub_dish")

        submenu_groups = (
            select(
                Menu.id,
                func.json_agg(
                    func.json_build_object(
                        "title",
                        Submenu.title,
                        "description",
                        Submenu.description,
                        "dishes",
                        dishes_group.c.dishes,
                    )
                ).label("submenus"),
            )
            .select_from(Submenu)
            .join(Menu)
            .join(
                dishes_group,
                Submenu.id == dishes_group.c.id,
            )
            .group_by(Menu.id)
        ).cte("sub_submenu")

        stmt = (
            select(Menu.title, Menu.description, submenu_groups.c.submenus)
            .select_from(Menu)
            .join(submenu_groups, Menu.id == submenu_groups.c.id)
        )

        result = await session.execute(stmt)

        menu_list = []

        for m in result.all():
            menu_list.append(dict(m))

        task_id = create_menu_excel.delay(menu_list)

        return {
            "task_id": str(task_id),
            "task_status": "Processing",
        }
