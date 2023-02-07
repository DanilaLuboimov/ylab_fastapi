import http

from celery.result import AsyncResult
from fastapi import APIRouter
from fastapi.responses import FileResponse, JSONResponse

from core.config import PROD
from tasks.tasks import create_menu_excel

router = APIRouter()


@router.post(
    path="/excel_restaurant_menu",
    summary="Создать excel файл",
    status_code=http.HTTPStatus.ACCEPTED,
)
async def create_excel_restaurant_menu() -> JSONResponse:
    """
    Создает task для формирования xlsx файла с общим меню.
    :param files: репозиторий для подготовки данных и обращения к celery.
    :param session: сессия с бд.
    """
    task_id = create_menu_excel.delay()
    return {
        "task_id": str(task_id),
        "task_status": "Processing",
    }


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
) -> FileResponse:
    """
    Позволяет скачать меню ресторана в виде сформированного
    xlsx файла по id задачи, вернувшейся из post-запроса excel_restaurant_menu
    :param task_id: id задачи
    """
    task = AsyncResult(task_id)

    if not task.ready():
        return {
            "task_id": task_id,
            "message": task.status,
        }

    if PROD:
        path = rf"../\media/{task_id}.xlsx"
    else:
        path = f"./files/{task_id}.xlsx"

    return FileResponse(
        path=path,
        filename="Меню ресторана.xlsx",
        media_type="application/xlsx",
    )
