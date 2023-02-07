import asyncio

import xlsxwriter
from sqlalchemy import func, select

from core.config import PROD
from db.base import async_session
from db.tables import Dish, Menu, Submenu

from .worker import worker

loop = asyncio.get_event_loop()


@worker.task
def create_menu_excel():
    restaurant_menu = loop.run_until_complete(get_restaurant_menu())
    task_id = worker.current_task.request.id

    if PROD:
        workbook = xlsxwriter.Workbook(rf"../\media/{task_id}.xlsx")
    else:
        workbook = xlsxwriter.Workbook(f"./files/{task_id}.xlsx")

    text_wrap = workbook.add_format({"text_wrap": True})

    worksheet = workbook.add_worksheet("Меню")

    worksheet.set_column(1, 1, 10)
    worksheet.set_column(2, 2, 30)
    worksheet.set_column(3, 3, 35)
    worksheet.set_column(4, 4, 72)

    row = 0
    index_menu = 1
    index_submenu = 1
    index_dish = 1

    for menu in restaurant_menu:
        worksheet.write(row, 0, index_menu)
        worksheet.write(row, 1, menu["title"])
        worksheet.write(row, 2, menu["description"])
        index_menu += 1
        row += 1

        for submenu in menu["submenus"]:
            worksheet.write(row, 1, index_submenu)
            worksheet.write(row, 2, submenu["title"])
            worksheet.write(row, 3, submenu["description"])
            index_submenu += 1
            row += 1

            for dish in submenu["dishes"]:
                worksheet.write(row, 2, index_dish)
                worksheet.write(row, 3, dish["title"])
                worksheet.write(row, 4, dish["description"], text_wrap)
                worksheet.write(row, 5, dish["price"])
                index_dish += 1
                row += 1

            index_dish = 1

        index_submenu = 1

    workbook.close()
    return "SUCCESS"


async def get_restaurant_menu():
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
        .order_by(Submenu.id.desc())
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
        .order_by(Menu.id.desc())
        .group_by(Menu.id)
    ).cte("sub_submenu")

    stmt = (
        select(Menu.title, Menu.description, submenu_groups.c.submenus)
        .select_from(Menu)
        .join(submenu_groups, Menu.id == submenu_groups.c.id)
        .order_by(Menu.id.desc())
    )

    async with async_session() as session:
        async with session.begin():
            result = await session.execute(stmt)

    restaurant_menu = []

    for m in result.all():
        restaurant_menu.append(dict(m))

    return restaurant_menu
