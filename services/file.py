from celery.result import AsyncResult
from fastapi.responses import FileResponse, JSONResponse

from core.config import PROD
from tasks.tasks import create_menu_excel


class FileServices:
    @staticmethod
    async def create_file() -> JSONResponse:
        task_id = create_menu_excel.delay()
        return {
            "task_id": str(task_id),
            "task_status": "Processing",
        }

    @staticmethod
    async def get_file(task_id: str) -> FileResponse:
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
