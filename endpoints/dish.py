import http

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from models.dish import DishIn, MainDish
from repositories.dish import DishRepository

from .depends import get_dishes_repository, get_session

router = APIRouter()


@router.get(
    path="/{m_id}/submenus/{sm_id}/dishes/",
    response_model=list[MainDish],
    summary="Список блюд",
    status_code=http.HTTPStatus.OK,
)
async def read_dishes(
    m_id: str,
    sm_id: str,
    dishes: DishRepository = Depends(get_dishes_repository),
    session: AsyncSession = Depends(get_session),
) -> list[MainDish]:
    """
    Возвращает список всех блюд, принадлежащих подменю.
    :param m_id: id меню, связанного с блюдом и подменю.
    :param sm_id: id подменю, связанного с блюдом.
    :param dishes: репозиторий для работы с логикой.
    :param session: сессия с бд.
    """
    return await dishes.get_all(session=session, sm_id=sm_id)


@router.get(
    path="/{m_id}/submenus/{sm_id}/dishes/{d_id}",
    response_model=MainDish,
    summary="Конкретное блюдо",
    status_code=http.HTTPStatus.OK,
)
async def read_dish(
    m_id: str,
    sm_id: str,
    d_id: str,
    dishes: DishRepository = Depends(get_dishes_repository),
    session: AsyncSession = Depends(get_session),
) -> MainDish | dict:
    """
    Возвращает  блюдо, принадлежащего подменю.
    :param m_id: id меню, связанного с блюдом и подменю.
    :param sm_id: id подменю, связанного с блюдом.
    :param d_id: id блюда.
    :param dishes: репозиторий для работы с логикой.
    :param session: сессия с бд.
    """
    return await dishes.get_by_id(session=session, d_id=d_id)


@router.post(
    path="/{m_id}/submenus/{sm_id}/dishes/",
    response_model=MainDish,
    summary="Создать блюдо",
    status_code=http.HTTPStatus.CREATED,
)
async def create_dish(
    m_id: str,
    sm_id: str,
    d: DishIn,
    dishes: DishRepository = Depends(get_dishes_repository),
    session: AsyncSession = Depends(get_session),
) -> MainDish:
    """
    Создает новое блюдо, принадлежащее подменю и возвращает его.
    :param m_id: id меню, связанного с блюдом и подменю.
    :param sm_id: id подменю, связанного с блюдом.
    :param d: поля с информацией о блюде.
    :param dishes: репозиторий для работы с логикой.
    :param session: сессия с бд.
    """
    return await dishes.create(
        session=session,
        m_id=m_id,
        sm_id=sm_id,
        d=d,
    )


@router.patch(
    path="/{m_id}/submenus/{sm_id}/dishes/{d_id}",
    response_model=MainDish,
    summary="Обновить блюдо",
    status_code=http.HTTPStatus.OK,
)
async def update_dish(
    m_id: str,
    sm_id: str,
    d_id: str,
    d: DishIn,
    dish: DishRepository = Depends(get_dishes_repository),
    session: AsyncSession = Depends(get_session),
) -> MainDish | dict:
    """
    Обновляет  блюдо, принадлежащее подменю и возвращает его.
    :param m_id: id меню, связанного с блюдом и подменю.
    :param sm_id: id подменю, связанного с блюдом.
    :param d_id: id блюда.
    :param d: поля с информацией о блюде для обновления.
    :param dish: репозиторий для работы с логикой.
    :param session: сессия с бд.
    """
    return await dish.patch(
        session=session,
        m_id=m_id,
        sm_id=sm_id,
        d_id=d_id,
        d=d,
    )


@router.delete(
    path="/{m_id}/submenus/{sm_id}/dishes/{d_id}",
    summary="Удалить блюдо",
    status_code=http.HTTPStatus.OK,
)
async def delete_dish(
    m_id: str,
    sm_id: str,
    d_id: str,
    dishes: DishRepository = Depends(get_dishes_repository),
    session: AsyncSession = Depends(get_session),
) -> dict:
    """
    Удаляет блюдо.
    :param m_id: id меню, связанного с блюдом и подменю.
    :param sm_id: id подменю, связанного с блюдом.
    :param d_id: id блюда.
    :param dishes: репозиторий для работы с логикой.
    :param session: сессия с бд.
    """
    return await dishes.delete(
        session=session,
        m_id=m_id,
        sm_id=sm_id,
        d_id=d_id,
    )
