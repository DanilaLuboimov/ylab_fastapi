import xlsxwriter

from core.config import PROD

from .worker import worker


@worker.task
def create_menu_excel(restaurant_menu: list):
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

    row: int = 0
    index_menu: int = 1
    index_submenu: int = 1
    index_dish: int = 1

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
