import http

from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse, JSONResponse

from services.file import FileServices

router = APIRouter()


@router.post(
    path="/excel_restaurant_menu",
    summary="Создать excel файл",
    status_code=http.HTTPStatus.ACCEPTED,
)
async def create_excel_restaurant_menu(
    file: FileServices = Depends(),
) -> JSONResponse:
    """
    Создает task для формирования xlsx файла с общим меню.
    :param file: сервис для создания файла через celery.
    """
    return await file.create_file()


@router.get(
    path="/excel_restaurant_menu/{task_id}",
    summary="Скачать excel файл",
    status_code=http.HTTPStatus.OK,
    responses={
        200: {
            "content": {"application/xlsx": {}},
            "description": "Return the JSON item or an file.xlsx",
        }
    },
)
async def get_excel_restaurant_menu(
    task_id: str,
    file: FileServices = Depends(),
) -> FileResponse:
    """
    Позволяет скачать меню ресторана в виде сформированного
    xlsx файла по id задачи, вернувшейся из post-запроса excel_restaurant_menu
    :param file: сервис для получения файла.
    :param task_id: id задачи.
    """
    return await file.get_file(task_id=task_id)
