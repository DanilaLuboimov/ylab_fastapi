import http

from celery.result import AsyncResult
from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import PROD
from repositories.files import FileRepository

from .depends import get_files_repository, get_session

router = APIRouter()


@router.post(
    path="/excel_restaurant_menu",
    summary="Создать excel файл",
    status_code=http.HTTPStatus.ACCEPTED,
)
async def create_excel_restaurant_menu(
    files: FileRepository = Depends(get_files_repository),
    session: AsyncSession = Depends(get_session),
) -> dict:
    """
    Создает task для формирования xlsx файла с общим меню.
    :param files: репозиторий для подготовки данных и обращения к celery.
    :param session: сессия с бд.
    """
    return await files.create_file(session)


@router.get(
    path="/excel_restaurant_menu/{task_id}",
    summary="Скачать excel файл",
    status_code=http.HTTPStatus.OK,
)
async def get_excel_restaurant_menu(
    task_id: str,
) -> FileResponse:
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
        media_type="multipart/form-data",
    )
