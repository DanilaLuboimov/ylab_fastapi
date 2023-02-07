import http

from fastapi import APIRouter, Depends

from services.test_data import TestDataService

router = APIRouter()


@router.post(
    path="/test_data",
    summary="Создать тестовые данные",
    status_code=http.HTTPStatus.CREATED,
)
async def create_test_data(
    test_data: TestDataService = Depends(),
) -> dict:
    """
    Создает записи в базе данных из заранее подготовленного json
    :param test_data: репозиторий для обработки test_data.json.
    """
    return await test_data.create()
