import http

from fastapi import APIRouter, Depends

from models.dish import Dish, DishIn
from repositories.dish import DishRepository

from .depends import get_dishes_repository

router = APIRouter()


@router.get(
    path='/{m_id}/submenus/{sm_id}/dishes/',
    response_model=list[Dish],
    summary='Список блюд',
    status_code=http.HTTPStatus.OK,
)
async def read_dishes(
        m_id: str,
        sm_id: str,
        dishes: DishRepository = Depends(get_dishes_repository),
) -> list[Dish]:
    """
    Возвращает список всех блюд, принадлежащих подменю.
    :param m_id: id меню, связанного с блюдом и подменю.
    :param sm_id: id подменю, связанного с блюдом.
    :param dishes: репозиторий для работы с логикой.
    """
    return await dishes.get_all(sm_id)


@router.get(
    path='/{m_id}/submenus/{sm_id}/dishes/{d_id}',
    response_model=Dish,
    summary='Конкретное блюдо',
    status_code=http.HTTPStatus.OK,
)
async def read_dish(
        m_id: str,
        sm_id: str,
        d_id: str,
        dishes: DishRepository = Depends(get_dishes_repository),
) -> Dish:
    """
    Возвращает  блюдо, принадлежащего подменю.
    :param m_id: id меню, связанного с блюдом и подменю.
    :param sm_id: id подменю, связанного с блюдом.
    :param d_id: id блюда.
    :param dishes: репозиторий для работы с логикой.
    """
    return await dishes.get_by_id(d_id)


@router.post(
    path='/{m_id}/submenus/{sm_id}/dishes/',
    response_model=Dish,
    summary='Создать блюдо',
    status_code=http.HTTPStatus.CREATED,
)
async def create_dish(
        m_id: str,
        sm_id: str,
        d: DishIn,
        dishes: DishRepository = Depends(get_dishes_repository),
) -> Dish:
    """
    Создает новое блюдо, принадлежащее подменю и возвращает его.
    :param m_id: id меню, связанного с блюдом и подменю.
    :param sm_id: id подменю, связанного с блюдом.
    :param d: поля с информацией о блюде.
    :param dishes: репозиторий для работы с логикой.
    """
    return await dishes.create(m_id, sm_id, d)


@router.patch(
    path='/{m_id}/submenus/{sm_id}/dishes/{d_id}',
    response_model=Dish,
    summary='Обновить блюдо',
    status_code=http.HTTPStatus.OK,
)
async def update_dish(
        m_id: str,
        sm_id: str,
        d_id: str,
        d: DishIn,
        dish: DishRepository = Depends(get_dishes_repository),
) -> Dish:
    """
    Обновляет  блюдо, принадлежащее подменю и возвращает его.
    :param m_id: id меню, связанного с блюдом и подменю.
    :param sm_id: id подменю, связанного с блюдом.
    :param d_id: id блюда.
    :param d: поля с информацией о блюде для обновления.
    :param dish: репозиторий для работы с логикой.
    """
    return await dish.patch(m_id, sm_id, d_id, d)


@router.delete(
    path='/{m_id}/submenus/{sm_id}/dishes/{d_id}',
    summary='Удалить блюдо',
    status_code=http.HTTPStatus.OK,
)
async def delete_dish(
        m_id: str,
        sm_id: str,
        d_id: str,
        dishes: DishRepository = Depends(get_dishes_repository),
) -> dict:
    """
    Удаляет блюдо.
    :param m_id: id меню, связанного с блюдом и подменю.
    :param sm_id: id подменю, связанного с блюдом.
    :param d_id: id блюда.
    :param dishes: репозиторий для работы с логикой.
    """
    return await dishes.delete(m_id, sm_id, d_id)
