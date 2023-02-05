import http

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.test_data import TestDataRepository

from .depends import get_session, get_test_data_repository

router = APIRouter()


@router.post(
    path="/test_data",
    summary="Создать тестовые данные",
    status_code=http.HTTPStatus.CREATED,
)
async def create_test_data(
    test_data: TestDataRepository = Depends(get_test_data_repository),
    session: AsyncSession = Depends(get_session),
) -> dict:
    """
    Создает записи в базе данных из заранее подготовленного json
    :param test_data: репозиторий для обработки test_data.json.
    :param session: сессия с бд.
    """
    return await test_data.create(session=session)
